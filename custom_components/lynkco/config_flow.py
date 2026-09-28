"""Config flow for Lynk & Co integration."""

import logging
import re

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONFIG_2FA_KEY,
    CONFIG_DARK_HOURS_END,
    CONFIG_DARK_HOURS_START,
    CONFIG_EMAIL_KEY,
    CONFIG_EXPERIMENTAL_KEY,
    CONFIG_LOGIN_METHOD_DIRECT,
    CONFIG_LOGIN_METHOD_REDIRECT,
    CONFIG_PASSWORD_KEY,
    CONFIG_REDIRECT_URI_KEY,
    CONFIG_SCAN_INTERVAL_KEY,
    CONFIG_VIN_KEY,
    DOMAIN,
    STORAGE_REFRESH_TOKEN_KEY,
)
from .login_flow import (
    get_auth_uri,
    get_tokens_from_redirect_uri,
    get_user_vins,
    login,
    two_factor_authentication,
)
from .token_manager import (
    STORAGE_CCC_TOKEN_KEY,
    decode_jwt_token,
    get_token_storage,
    send_device_login,
)

_LOGGER = logging.getLogger(__name__)

STEP_DIRECT_LOGIN_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONFIG_EMAIL_KEY): str,
        vol.Required(CONFIG_PASSWORD_KEY): str,
    }
)

STEP_DIRECT_LOGIN_2FA_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONFIG_2FA_KEY): str,
    }
)

STEP_REDIRECT_LOGIN_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONFIG_REDIRECT_URI_KEY): str,
    }
)


def is_valid_email(email: str) -> bool:
    """Validate the email format using a regex pattern."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_redirect_uri(redirect_uri: str) -> bool:
    """Basic validation for redirect URI format."""
    return redirect_uri.startswith("msauth://prod.lynkco.app.crisp.prod/")


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lynk & Co."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return OptionsFlowHandler()

    async def _finalize_with_tokens(
        self, access_token: str, refresh_token: str, id_token: str
    ) -> config_entries.ConfigFlowResult:
        token_storage = get_token_storage(self.hass)
        tokens = await token_storage.async_load() or {}
        tokens[STORAGE_REFRESH_TOKEN_KEY] = refresh_token
        ccc_token = await send_device_login(access_token)
        if ccc_token:
            tokens[STORAGE_CCC_TOKEN_KEY] = ccc_token
        else:
            _LOGGER.error("New ccc token is none")
        await token_storage.async_save(tokens)

        # Decode User ID from ID Token (the JWT payload)
        claims = decode_jwt_token(id_token)
        user_id = claims.get("snowflakeId")

        # Retrieve VINs by querying the API
        vins = await get_user_vins(ccc_token, user_id) if ccc_token and user_id else []
        # For simplicity, we take the first VIN
        vin = vins[0] if vins else None
        if not vin:
            _LOGGER.error("No VINs found for the user")
            return self.async_abort(reason="no_vins_found")

        if hasattr(self, "_reauth_entry"):
            # Update the existing config entry
            self.hass.config_entries.async_update_entry(
                self._reauth_entry,
                data={CONFIG_VIN_KEY: vin},
            )
            await self.hass.config_entries.async_reload(self._reauth_entry.entry_id)
            return self.async_abort(reason="reauth_successful")

        # Create new entry
        return self.async_create_entry(
            title="Lynk & Co",
            data={CONFIG_VIN_KEY: vin},
            description_placeholders={
                "additional_configuration": "Please use the configuration to enable experimental features."
            },
        )

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""

        return self.async_show_menu(
            step_id="user",
            menu_options=[CONFIG_LOGIN_METHOD_DIRECT, CONFIG_LOGIN_METHOD_REDIRECT],
        )

    async def async_step_redirect_login(self, user_input=None):
        """Handle the redirect login flow."""
        errors = {}

        if user_input:
            redirect_uri = user_input.get(CONFIG_REDIRECT_URI_KEY)
            login_code_verifier = self.context.get("login_code_verifier")

            if redirect_uri and login_code_verifier:
                if not is_valid_redirect_uri(redirect_uri):
                    errors["redirect_uri"] = "invalid_redirect_uri"
                else:
                    async with aiohttp.ClientSession() as session:
                        (
                            access_token,
                            refresh_token,
                            id_token,
                        ) = await get_tokens_from_redirect_uri(
                            redirect_uri, login_code_verifier, session
                        )

                    if access_token and refresh_token and id_token:
                        return await self._finalize_with_tokens(
                            access_token, refresh_token, id_token
                        )
                    errors["missing_details"] = "missing_details"
            else:
                errors["missing_details"] = "missing_details"

        auth_url, code_verifier, _ = get_auth_uri()
        self.context["login_code_verifier"] = code_verifier

        return self.async_show_form(
            step_id="redirect_login",
            data_schema=STEP_REDIRECT_LOGIN_DATA_SCHEMA,
            description_placeholders={"auth_url": auth_url},
            errors=errors,
        )

    async def async_step_direct_login(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        jar = aiohttp.CookieJar(quote_cookie=False)
        session = aiohttp.ClientSession(cookie_jar=jar)
        self.context["session"] = session

        if user_input:
            email = user_input.get("email")
            password = user_input.get("password")

            if not email or not password:
                errors["missing_details"] = "missing_details"
            elif not is_valid_email(email):
                errors["email"] = "invalid_email"

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
                    return await self.async_step_direct_login_2fa()
                # Handle the case where any of the required items are None
                errors["base"] = "login_failed"
            else:
                # Re-show the form with errors if validation fails
                return self.async_show_form(
                    step_id="direct_login",
                    data_schema=STEP_DIRECT_LOGIN_DATA_SCHEMA,
                    errors=errors,
                )
        return self.async_show_form(
            step_id="direct_login",
            data_schema=STEP_DIRECT_LOGIN_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_direct_login_2fa(self, user_input=None):
        """Handle the second step for inputting the 2FA code."""
        errors = {}
        session = self.context.get("session")

        if user_input is not None:
            two_fa_code = user_input.get("2fa")
            login_details = self.context.get("login_details", {})

            try:
                access_token, refresh_token, id_token = await two_factor_authentication(
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

                if access_token and refresh_token and id_token:
                    return await self._finalize_with_tokens(
                        access_token, refresh_token, id_token
                    )
                errors["base"] = "invalid_2fa_code"
            except Exception as e:
                _LOGGER.error(
                    "Error during two-factor authentication: %s", e, exc_info=True
                )
                errors["base"] = "two_factor_auth_failed"

        # Show the form again with any errors
        return self.async_show_form(
            step_id="direct_login_2fa",
            data_schema=STEP_DIRECT_LOGIN_2FA_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reauth(self, user_input=None):
        """Handle the re-authentication flow."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )

        return await self.async_step_user(user_input)


class OptionsFlowHandler(config_entries.OptionsFlow):
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
