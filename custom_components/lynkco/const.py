"""Constants for the Lynk & Co integration."""

DOMAIN = "lynkco"
COORDINATOR = "coordinator"
STORAGE_VERSION = 1
STORAGE_TOKEN_KEY = "token_storage"
STORAGE_CCC_TOKEN_KEY = "ccc_token"
STORAGE_USER_ID_KEY = "user_id"
STORAGE_REFRESH_TOKEN_KEY = "refresh_token"
DATA_UPDATE_COORDINATOR = "data_update_coordinator"

# Config keys
CONFIG_LOGIN_METHOD = "login_method"
CONFIG_LOGIN_METHOD_DIRECT = "direct_login"
CONFIG_LOGIN_METHOD_REDIRECT = "redirect_login"
CONFIG_EMAIL_KEY = "email"
CONFIG_PASSWORD_KEY = "password"
CONFIG_VIN_KEY = "vin"
CONFIG_2FA_KEY = "2fa"
CONFIG_REDIRECT_URI_KEY = "redirect_uri"
CONFIG_EXPERIMENTAL_KEY = "experimental"
CONFIG_SCAN_INTERVAL_KEY = "scan_interval"
CONFIG_DARK_HOURS_START = "dark_hours_start"
CONFIG_DARK_HOURS_END = "dark_hours_end"

# Hass data constants
DATA_EXPECTED_STATE = "expected_state_monitor"
DATA_IS_FORCE_UPDATE = "is_force_update"
DATA_STORED_DATA = "stored_data"

# Service keys
SERVICE_REFRESH_TOKENS_KEY = "refresh_tokens"
SERVICE_START_CLIMATE_KEY = "start_climate"
SERVICE_STOP_CLIMATE_KEY = "stop_climate"
SERVICE_LOCK_DOORS_KEY = "lock_doors"
SERVICE_UNLOCK_DOORS_KEY = "unlock_doors"
SERVICE_START_FLASHLIGHT_KEY = "start_flash_lights"
SERVICE_STOP_FLASHLIGHT_KEY = "stop_flash_lights"
SERVICE_START_HONK_KEY = "start_honk"
SERVICE_START_HONK_FLASH_KEY = "start_honk_flash"
SERVICE_STOP_HONK_KEY = "stop_honk"
SERVICE_FORCE_UPDATE_KEY = "force_update_data"
SERVICE_START_ENGINE_KEY = "start_engine"
SERVICE_STOP_ENGINE_KEY = "stop_engine"

# Expected states
EXPECTED_STATE_CLIMATE_ON = "climate_on"
EXPECTED_STATE_CLIMATE_OFF = "climate_off"
EXPECTED_STATE_ENGINE_ON = "engine_on"
EXPECTED_STATE_ENGINE_OFF = "engine_off"
EXPECTED_STATE_UNLOCKED = "unlocked"
EXPECTED_STATE_LOCKED = "locked"
