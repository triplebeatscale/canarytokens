import os
from distutils.util import strtobool
from typing import Any, Literal, Optional

from pydantic import BaseSettings, EmailStr, HttpUrl, SecretStr

from canarytokens.models import Port


class SwitchboardSettings(BaseSettings):
    PUBLIC_DOMAIN: str = os.getenv("PUBLIC_DOMAIN")
    CHANNEL_DNS_IP: str = ""
    CHANNEL_DNS_PORT: Port = Port(53)
    CHANNEL_HTTP_PORT: Port = Port(80)
    CHANNEL_SMTP_PORT: Port = Port(25)
    CHANNEL_MYSQL_PORT: Port = Port(3306)
    CHANNEL_MTLS_KUBECONFIG_PORT: Port = Port(6443)
    CHANNEL_WIREGUARD_PORT: Port = Port(51820)
    SWITCHBOARD_SCHEME: str = "https"
    FORCE_HTTPS: bool = False
    # TODO: Remove this default here and added it where it's used. This is too opinionated.
    REDIS_HOST: str = os.getenv("REDIS_HOST","localhost")
    REDIS_PORT: Port = Port(6379)
    REDIS_DB: str = os.getenv("REDIS_DB","0")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "auth_disabled")

    REAL_IP_HEADER: str = "x-real-ip"

    WG_PRIVATE_KEY_SEED: str = os.getenv("WG_PRIVATE_KEY_SEED")
    WG_PRIVATE_KEY_N: str = "1000"

    FRONTEND_SETTINGS_PATH: str = "../frontend/frontend.env"
    USING_NGINX: bool = True
    TEMPLATES_PATH: str = "../templates"

    ALERT_EMAIL_FROM_ADDRESS: EmailStr = EmailStr("illegal@email.com")
    ALERT_EMAIL_FROM_DISPLAY: str = "Canarytokens-Test"
    ALERT_EMAIL_SUBJECT: str = "Canarytokens Alert"
    MAX_ALERTS_PER_MINUTE: int = 1
    # Maximum number of alert failures before a mechanism is disabled
    MAX_ALERT_FAILURES: int = 5

    IPINFO_API_KEY: Optional[SecretStr] = None
    # Mailgun Required Settings
    MAILGUN_API_KEY: Optional[SecretStr] = None
    MAILGUN_BASE_URL: Optional[HttpUrl] = HttpUrl(
        "https://api.mailgun.net", scheme="https"
    )
    MAILGUN_DOMAIN_NAME: Optional[str]
    # Sendgrid Required Settings
    SENDGRID_API_KEY: Optional[SecretStr] = None
    SENDGRID_SANDBOX_MODE: bool = True
    # SMTP Required Settings
    SMTP_USERNAME: Optional[str]
    SMTP_PASSWORD: Optional[str]
    SMTP_SERVER: Optional[str]
    SMTP_PORT: Optional[Port] = Port(587)

    SENTRY_DSN: Optional[HttpUrl] = None
    SENTRY_ENVIRONMENT: Literal["prod", "staging", "dev", "ci", "local"] = "local"
    SENTRY_ENABLE: bool = True

    SWITCHBOARD_LOG_SIZE: Optional[int] = 500000000
    SWITCHBOARD_LOG_COUNT: Optional[int] = 20

    TOKEN_RETURN: Literal["gif", "fortune"] = "gif"

    class Config:
        allow_mutation = False
        env_file = "../switchboard/switchboard.env"
        env_file_encoding = "utf-8"
        env_prefix = "CANARY_"


class FrontendSettings(BaseSettings):
    API_APP_TITLE: str = "Canarytokens"
    API_VERSION_STR: str = "v1"
    PUBLIC_IP: str = os.getenv("CANARY_PUBLIC_IP")
    DOMAINS: list[str] = os.getenv("CANARY_DOMAINS").split(",")
    NXDOMAINS: list[str] = os.getenv("CANARY_NXDOMAINS").split(",")
    SWITCHBOARD_SETTINGS_PATH: str = "../switchboard/switchboard.env"

    SENTRY_DSN: Optional[HttpUrl] = None
    SENTRY_ENVIRONMENT: Literal["prod", "staging", "dev", "ci", "local"] = "local"
    SENTRY_ENABLE: bool = True

    TEMPLATES_PATH: str = "../templates"
    STATIC_FILES_PATH: str = "../templates/static"
    STATIC_FILES_APPLICATION_SUB_PATH: str = "/resources"
    STATIC_FILES_APPLICATION_INTERNAL_NAME: str = "resources"

    # if None the API docs won't load. Loads at /API_HASH/{your_url}. Must start with a /
    API_REDOC_URL: Optional[str]

    # upload settings
    MAX_UPLOAD_SIZE: int = 1024 * 1024 * 1
    WEB_IMAGE_UPLOAD_PATH: str = "/uploads"

    # ! UNUSED ! TODO: figure out why
    # log settings

    FRONTEND_LOG_SIZE: Optional[int] = 500000000
    FRONTEND_LOG_COUNT: Optional[int] = 20

    DEV_BUILD_ID: Optional[str]

    # 3rd party settings
    AWSID_URL: Optional[HttpUrl]
    TESTING_AWS_ACCESS_KEY_ID: Optional[str] = ""
    TESTING_AWS_SECRET_ACCESS_KEY: Optional[str] = ""
    TESTING_AWS_REGION: Optional[str] = "us-east-2"
    TESTING_AWS_OUTPUT: Optional[str] = "json"
    AZURE_ID_TOKEN_URL: Optional[HttpUrl]
    AZURE_ID_TOKEN_AUTH: Optional[str]
    GOOGLE_API_KEY: Optional[str]
    EXTEND_EMAIL: Optional[str]
    EXTEND_PASSWORD: Optional[SecretStr] = SecretStr("NoExtendPasswordFound")
    EXTEND_CARD_NAME: Optional[str]
    CLOUDFRONT_URL: Optional[HttpUrl]
    AZUREAPP_ID: Optional[str]
    AZUREAPP_SECRET: Optional[str]  # TODO: Figure out SecretStr with Azure secrets
    ST_OAUTH_TOKEN: str = os.getenv("ST_OAUTH_TOKEN")

    class Config:
        allow_mutation = False
        env_file = "../frontend/frontend.env"
        env_file_encoding = "utf-8"
        env_prefix = "CANARY_"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name in ["DOMAINS", "NXDOMAINS"]:
                return [x for x in raw_val.split(",")]
            return cls.json_loads(raw_val)
