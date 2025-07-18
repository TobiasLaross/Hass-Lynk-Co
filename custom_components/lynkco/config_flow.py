import logging
import re

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import aiohttp

from .const import (
    CONFIG_2FA_KEY,
    CONFIG_DARK_HOURS_END,
    CONFIG_DARK_HOURS_START,
    CONFIG_EMAIL_KEY,
    CONFIG_EXPERIMENTAL_KEY,
    CONFIG_PASSWORD_KEY,
    CONFIG_SCAN_INTERVAL_KEY,
    CONFIG_VIN_KEY,
    DOMAIN,
    STORAGE_REFRESH_TOKEN_KEY,
)
from .login_flow import login, two_factor_authentication
from .token_manager import STORAGE_CCC_TOKEN_KEY, get_token_storage, send_device_login

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONFIG_EMAIL_KEY): str,
        vol.Required(CONFIG_PASSWORD_KEY): str,
        vol.Required(CONFIG_VIN_KEY): str,
    }
)

STEP_TWO_FA_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONFIG_2FA_KEY): str,
    }
)


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_vin(vin: str) -> bool:
    """Validate the VIN based on length and allowed characters."""
    vin_regex = r"^[A-HJ-NPR-Z0-9]{17}$"
    return bool(re.match(vin_regex, vin))


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lynk & Co."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        
        jar = aiohttp.CookieJar(quote_cookie=False)
        session = aiohttp.ClientSession(cookie_jar=jar)
        self.context['session'] = session

        if user_input:
            email = user_input.get("email")
            password = user_input.get("password")
            vin = user_input.get("vin")

            if not email or not password or not vin:
                errors["missing_details"] = "missing_details"
            else:
                if not is_valid_email(email):
                    errors["email"] = "invalid_email"

                if not is_valid_vin(vin):
                    errors["vin"] = "invalid_vin"

            if not errors:
                (
                    x_ms_cpim_trans_value,
                    x_ms_cpim_csrf_token,
                    page_view_id,
                    referer_url,
                    code_verifier,
                ) = await login(email, password, session)

                if None not in (x_ms_cpim_trans_value, x_ms_cpim_csrf_token):
                    self.context["login_details"] = {
                        "x_ms_cpim_trans_value": x_ms_cpim_trans_value,
                        "x_ms_cpim_csrf_token": x_ms_cpim_csrf_token,
                        "page_view_id": page_view_id,
                        "referer_url": referer_url,
                        "code_verifier": code_verifier,
                    }
                    self.context["vin"] = vin
                    return await self.async_step_two_factor()
                else:
                    # Handle the case where any of the required items are None
                    errors["base"] = "login_failed"
            else:
                # Re-show the form with errors if validation fails
                return self.async_show_form(
                    step_id="user",
                    data_schema=STEP_USER_DATA_SCHEMA,
                    errors=errors,
                )
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_two_factor(self, user_input=None):
        """Handle the second step for inputting the 2FA code."""
        errors = {}
        session = self.context.get('session')

        if user_input is not None:
            two_fa_code = user_input.get("2fa")
            login_details = self.context.get("login_details", {})

            try:
                access_token, refresh_token = await two_factor_authentication(
                    two_fa_code,
                    login_details.get("x_ms_cpim_trans_value"),
                    login_details.get("x_ms_cpim_csrf_token"),
                    login_details.get("page_view_id"),
                    login_details.get("referer_url"),
                    login_details.get("code_verifier"),
                    session,
                )
                
                # Close the session
                await session.close()

                if access_token and refresh_token:
                    token_storage = get_token_storage(self.hass)
                    tokens = await token_storage.async_load() or {}
                    tokens[STORAGE_REFRESH_TOKEN_KEY] = refresh_token
                    ccc_token = await send_device_login(access_token)
                    if ccc_token:
                        tokens[STORAGE_CCC_TOKEN_KEY] = ccc_token
                    else:
                        _LOGGER.error("New ccc token is none")
                    await token_storage.async_save(tokens)
                    vin = self.context.get("vin", "")
                    if hasattr(self, "_reauth_entry"):
                        # Update the existing config entry
                        self.hass.config_entries.async_update_entry(
                            self._reauth_entry,
                            data={"vin": vin},
                        )
                        await self.hass.config_entries.async_reload(
                            self._reauth_entry.entry_id
                        )
                        return self.async_abort(reason="reauth_successful")
                    else:
                        # Create new entry
                        return self.async_create_entry(
                            title="Lynk & Co",
                            data={"vin": vin},
                            description_placeholders={
                                "additional_configuration": "Please use the configuration to enable experimental features."
                            },
                        )
                else:
                    errors["base"] = "invalid_2fa_code"
            except Exception as e:
                _LOGGER.error(
                    "Error during two-factor authentication: %s", e, exc_info=True
                )
                errors["base"] = "two_factor_auth_failed"
        
        # Show the form again with any errors
        return self.async_show_form(
            step_id="two_factor",
            data_schema=STEP_TWO_FA_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reauth(self, user_input=None):
        """Handle the re-authentication flow."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )

        if user_input is not None:
            return await self.async_step_user(user_input)

        return self.async_show_form(
            step_id="reauth",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors={},
            description_placeholders={
                "message": "Please re-enter your credentials to re-authenticate."
            },
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            # Save the options and conclude the options flow
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONFIG_EXPERIMENTAL_KEY,
                    default=self.config_entry.options.get(
                        CONFIG_EXPERIMENTAL_KEY, False
                    ),
                ): bool,
                vol.Required(
                    CONFIG_SCAN_INTERVAL_KEY,
                    default=self.config_entry.options.get(
                        CONFIG_SCAN_INTERVAL_KEY, 120
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=1440)),
                vol.Required(
                    CONFIG_DARK_HOURS_START,
                    default=self.config_entry.options.get(CONFIG_DARK_HOURS_START, 1),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
                vol.Required(
                    CONFIG_DARK_HOURS_END,
                    default=self.config_entry.options.get(CONFIG_DARK_HOURS_END, 5),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
            }
        )

        # Display or re-display the form with the current options as defaults
        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
