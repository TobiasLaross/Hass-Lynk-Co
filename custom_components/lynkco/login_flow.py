import json
import logging
import urllib.parse
from urllib.parse import quote_plus

import pkce

# TODO: Try new login flow
_LOGGER = logging.getLogger(__name__)
login_b2c_url = "https://login.lynkco.com/lynkcoprod.onmicrosoft.com/b2c_1a_signin_mfa/"
client_id = "813902c0-0579-43f3-a767-6601c2f5fdbe"
scope_base_url = "https://lynkcoprod.onmicrosoft.com/mobile-app-web-api/mobile"


async def login(email, password, session):
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    page_view_id = await authorize(code_challenge, session)

    if page_view_id is None:
        _LOGGER.error("Authorization failed, page_view_id missing.")
        return None, None, None, None, None

    cookie = session.cookie_jar.filter_cookies("https://login.lynkco.com").get(
        "x-ms-cpim-trans"
    )
    x_ms_cpim_trans_value = cookie.value if cookie else None
    cookie = session.cookie_jar.filter_cookies("https://login.lynkco.com").get(
        "x-ms-cpim-csrf"
    )
    x_ms_cpim_csrf_token = cookie.value if cookie else None
    if None in (x_ms_cpim_csrf_token, x_ms_cpim_csrf_token):
        _LOGGER.error("Authorization failed, missing cookies")
        return None, None, None, None, None
    _LOGGER.info("Authorization successful.")

    success = await postLogin(
        email, password, x_ms_cpim_trans_value, x_ms_cpim_csrf_token, session
    )
    if success is False:
        _LOGGER.error("Login failed. Exiting...")
        return None, None, None, None, None
    _LOGGER.info("Credentials accepted.")

    page_view_id, referer_url = await getCombinedSigninAndSignup(
        x_ms_cpim_csrf_token,
        x_ms_cpim_trans_value,
        page_view_id,
        code_challenge,
        session,
    )
    return (
        x_ms_cpim_trans_value,
        x_ms_cpim_csrf_token,
        page_view_id,
        referer_url,
        code_verifier,
    )


async def two_factor_authentication(
    verification_code,
    x_ms_cpim_trans_value,
    x_ms_cpim_csrf_token,
    page_view_id,
    referer_url,
    code_verifier,
    session,
):
    success = await postVerification(
        verification_code, x_ms_cpim_trans_value, x_ms_cpim_csrf_token, session
    )
    if success is False:
        _LOGGER.error("Verification failed. Exiting...")
        return None, None
    _LOGGER.info("Verification successful.")

    code = await getRedirect(x_ms_cpim_trans_value, page_view_id, referer_url, session)
    if code is None:
        _LOGGER.error("Failed to get redirect code. Exiting...")
        return None, None

    access_token, refresh_token = await getTokens(
        code,
        code_verifier,
        session,
    )

    if access_token is None or refresh_token is None:
        _LOGGER.error("Failed to get tokens. Exiting...")
        return None, None
    return access_token, refresh_token


async def authorize(code_challenge, session):
    base_url = f"{login_b2c_url}oauth2/v2.0/authorize"

    params = {
        "response_type": "code",
        "scope": f"{scope_base_url}.read {scope_base_url}.write profile offline_access",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "redirect_uri": "msauth.com.lynkco.prod.lynkco-app://auth",
        "client_id": client_id,
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    async with session.get(base_url, params=params, headers=headers) as response:
        if response.status == 200:
            page_view_id = response.headers.get("x-ms-gateway-requestid", "")
            _LOGGER.info("GET request for authorization successful.")
            return page_view_id
        else:
            _LOGGER.error(
                "GET request for authorization failed with status code:",
                response.status,
            )
    return None


async def postLogin(
    email, password, x_ms_cpim_trans_value, x_ms_cpim_csrf_token, session
):
    tx_value = f"StateProperties={x_ms_cpim_trans_value}"
    encoded_tx_value = urllib.parse.quote(tx_value)
    query_params = f"p=B2C_1A_signin_mfa&tx={encoded_tx_value}"
    data = {
        "request_type": "RESPONSE",
        "signInName": email,
        "password": password,
    }
    base_url = f"{login_b2c_url}SelfAsserted"
    headers = {
        "x-csrf-token": x_ms_cpim_csrf_token,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    url_with_params = f"{base_url}?{query_params}"
    async with session.post(url_with_params, headers=headers, data=data) as response:
        if response.status == 200:
            _LOGGER.info("POST request for login successful.")
            return True
        else:
            _LOGGER.error(
                f"POST request for login failed with status code: {response.status}"
            )
    return False


async def getCombinedSigninAndSignup(
    csrf_token, tx_value, page_view_id, code_challenge, session
):
    url = f"{login_b2c_url}api/CombinedSigninAndSignup/confirmed"
    referer_base_url = f"{login_b2c_url}v2.0/authorize"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "sec-fetch-site": "same-origin",
        "sec-fetch-dest": "document",
        "accept-language": "en-GB,en;q=0.9",
        "sec-fetch-mode": "navigate",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "referer": f"{referer_base_url}?x-client-Ver=1.2.22&state=ABC&client_info=1&prompt=select_account&response_type=code&x-app-name=Lynk%20%26%20Co&code_challenge_method=S256&x-app-ver=2.12.0&scope=https%3A%2F%2Flynkcoprod.onmicrosoft.com%2Fmobile-app-web-api%2Fmobile.read%20https%3A%2F%2Flynkcoprod.onmicrosoft.com%2Fmobile-app-web-api%2Fmobile.write%20openid%20profile%20offline_access&x-client-SKU=MSAL.iOS&x-client-OS=17.4.1&code_challenge={code_challenge}&x-client-CPU=64&redirect_uri=msauth.com.lynkco.prod.lynkco-app%3A%2F%2Fauth&client-request-id=0207E18F-1598-4BD7-AC0F-705414D8B0F7&client_id={client_id}&x-client-DM=iPhone&return-client-request-id=true&haschrome=1",
        "accept-encoding": "gzip, deflate, br",
    }
    # NDE0ODRGNTctM0VENi00NjBFLTlCQjItN0UyNjZBQTVEQjhB
    # TODO: referer state could maybe be removed
    params = {
        "rememberMe": "false",
        "csrf_token": csrf_token,
        "tx": f"StateProperties={tx_value}",
        "p": "B2C_1A_signin_mfa",
        "diags": json.dumps(
            {
                "pageViewId": page_view_id,
                "pageId": "CombinedSigninAndSignup",
                "trace": [],
            }
        ),
    }

    async with session.get(url, params=params, headers=headers) as response:
        if response.status == 200:
            new_page_view_id = response.headers.get("x-ms-gateway-requestid")
            if new_page_view_id:
                constructed_url = f"{url}?{'&'.join([f'{key}={value}' for key, value in params.items() if key != 'diags'])}"
                diags_dict = json.loads(params["diags"])
                encoded_diags = quote_plus(json.dumps(diags_dict))
                constructed_url_with_diags = f"{constructed_url}&diags={encoded_diags}"
                return new_page_view_id, constructed_url_with_diags
            else:
                _LOGGER.error("New pageViewId not found in the response headers.")
                return None, None
        else:
            _LOGGER.error(
                f"GET request for CombinedSigninAndSignup failed with status code: {response.status}"
            )
    return None, None


async def postVerification(
    verification_code, x_ms_cpim_trans_value, x_ms_cpim_csrf_token, session
):
    tx_value = f"StateProperties={x_ms_cpim_trans_value}"
    query_params = f"p=B2C_1A_signin_mfa&tx={urllib.parse.quote(tx_value)}"
    data = {"verificationCode": verification_code, "request_type": "RESPONSE"}
    url = f"{login_b2c_url}SelfAsserted?{query_params}"
    headers = {
        "x-csrf-token": x_ms_cpim_csrf_token,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    async with session.post(url, headers=headers, data=data) as response:
        if response.status == 200:
            _LOGGER.info("POST request for verification successful.")
            return True
        else:
            _LOGGER.error(
                f"POST verification failed with status code: {response.status}"
            )
    return False


async def getRedirect(tx_value, page_view_id, referer_url, session):
    url = f"{login_b2c_url}api/SelfAsserted/confirmed"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "sec-fetch-site": "same-origin",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "accept-language": "en-GB,en;q=0.9",
        "referer": referer_url,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS like Mac OS X) AppleWebKit (KHTML, like Gecko) Version Mobile Safari",
    }

    cookie = session.cookie_jar.filter_cookies("https://login.lynkco.com").get(
        "x-ms-cpim-csrf"
    )
    x_ms_cpim_csrf_token = cookie.value if cookie else None
    params = {
        "csrf_token": x_ms_cpim_csrf_token,
        "tx": f"StateProperties={tx_value}",
        "p": "B2C_1A_signin_mfa",
        "diags": json.dumps(
            {
                "pageViewId": page_view_id,
                "pageId": "SelfAsserted",
                "trace": [],
            }
        ),
    }
    async with session.get(
        url, headers=headers, params=params, allow_redirects=False
    ) as response:
        if response.status in [301, 302]:
            location_header = response.headers.get("location", "")
            code = urllib.parse.parse_qs(
                urllib.parse.urlparse(location_header).query
            ).get("code", [None])[0]
            return code
        else:
            _LOGGER.error(
                f"GET redirect request failed with status code: {response.status}"
            )
    return None


async def getTokens(code, code_verifier, session):
    redirect_uri = "msauth.com.lynkco.prod.lynkco-app://auth"
    data = {
        "client_info": "1",
        "scope": f"{scope_base_url}.read {scope_base_url}.write openid profile offline_access",
        "code": code,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
    }

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "x-ms-pkeyauth+": "1.0",
        "x-client-last-telemetry": "4|0|||",
        "x-client-ver": "1.2.22",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "LynkCo/3047 CFNetwork/1494.0.7 Darwin/23.4.0",
    }

    url = f"{login_b2c_url}oauth2/v2.0/token"

    async with session.post(url, data=data, headers=headers) as response:
        if response.status == 200:
            json_response = await response.json()
            access_token = json_response.get("access_token")
            refresh_token = json_response.get("refresh_token")

            return access_token, refresh_token
        else:
            _LOGGER.error(f"Failed to obtain tokens. Status code: {response.status}")
    return None, None
