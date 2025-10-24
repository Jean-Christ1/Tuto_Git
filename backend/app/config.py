"""
Application Configuration Module.

This module handles all configuration settings for the Natural Language to SQL
application using Pydantic Settings for environment variable management.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    This class uses Pydantic Settings to load and validate configuration
    from environment variables and .env files.

    Attributes
    ----------
    api_host : str
        Host address for the API server.
    api_port : int
        Port number for the API server.
    api_title : str
        Title of the API for documentation.
    api_version : str
        Version of the API.
    debug : bool
        Enable debug mode.
    llm_provider : str
        LLM provider to use (openai or anthropic).
    llm_model : str
        Model identifier for the LLM.
    llm_temperature : float
        Temperature setting for LLM responses.
    llm_max_tokens : int
        Maximum tokens for LLM responses.
    openai_api_key : Optional[str]
        API key for OpenAI.
    anthropic_api_key : Optional[str]
        API key for Anthropic.
    database_url : str
        Database connection URL.
    database_echo : bool
        Enable SQLAlchemy echo for debugging.
    secret_key : str
        Secret key for JWT token encoding.
    algorithm : str
        Algorithm for JWT token encoding.
    access_token_expire_minutes : int
        Expiration time for access tokens in minutes.
    cors_origins : List[str]
        List of allowed CORS origins.
    cors_allow_credentials : bool
        Allow credentials in CORS requests.
    cors_allow_methods : str
        Allowed HTTP methods for CORS.
    cors_allow_headers : str
        Allowed headers for CORS.
    max_query_results : int
        Maximum number of results to return from queries.
    query_timeout : int
        Timeout for query execution in seconds.
    enable_query_caching : bool
        Enable caching of query results.
    cache_ttl : int
        Time to live for cached results in seconds.
    log_level : str
        Logging level.
    log_file : str
        Path to log file.
    rate_limit_per_minute : int
        Rate limit per minute per IP.
    rate_limit_per_hour : int
        Rate limit per hour per IP.

    Examples
    --------
    >>> settings = Settings()
    >>> print(settings.api_host)
    '0.0.0.0'
    >>> print(settings.llm_provider)
    'openai'
    """

    # API Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_title: str = Field(default="Natural Language to SQL API", alias="API_TITLE")
    api_version: str = Field(default="1.0.0", alias="API_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    # LLM Configuration
    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gpt-4-turbo-preview", alias="LLM_MODEL")
    llm_temperature: float = Field(default=0.0, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=2000, alias="LLM_MAX_TOKENS")

    # API Keys
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///../database/chinook.db", alias="DATABASE_URL"
    )
    database_echo: bool = Field(default=False, alias="DATABASE_ECHO")

    # Security
    secret_key: str = Field(
        default="your-super-secret-key-change-this", alias="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # CORS Settings
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:3001", alias="CORS_ORIGINS"
    )
    cors_allow_credentials: bool = Field(
        default=True, alias="CORS_ALLOW_CREDENTIALS"
    )
    cors_allow_methods: str = Field(default="*", alias="CORS_ALLOW_METHODS")
    cors_allow_headers: str = Field(default="*", alias="CORS_ALLOW_HEADERS")

    # Query Settings
    max_query_results: int = Field(default=1000, alias="MAX_QUERY_RESULTS")
    query_timeout: int = Field(default=30, alias="QUERY_TIMEOUT")
    enable_query_caching: bool = Field(default=True, alias="ENABLE_QUERY_CACHING")
    cache_ttl: int = Field(default=300, alias="CACHE_TTL")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", alias="LOG_FILE")

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, alias="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, alias="RATE_LIMIT_PER_HOUR")

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """
        Parse CORS origins from string to list.

        Parameters
        ----------
        v : str or list
            CORS origins as string or list.

        Returns
        -------
        list
            List of CORS origin strings.

        Examples
        --------
        >>> Settings.parse_cors_origins("http://localhost:3000,http://localhost:3001")
        ['http://localhost:3000', 'http://localhost:3001']
        """
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("llm_provider")
    def validate_llm_provider(cls, v):
        """
        Validate LLM provider selection.

        Parameters
        ----------
        v : str
            LLM provider name.

        Returns
        -------
        str
            Validated LLM provider name.

        Raises
        ------
        ValueError
            If provider is not supported.

        Examples
        --------
        >>> Settings.validate_llm_provider("openai")
        'openai'
        """
        allowed_providers = ["openai", "anthropic"]
        if v.lower() not in allowed_providers:
            raise ValueError(
                f"LLM provider must be one of {allowed_providers}, got {v}"
            )
        return v.lower()

    class Config:
        """Pydantic configuration class."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings instance.

    Returns
    -------
    Settings
        Application settings object.

    Examples
    --------
    >>> settings = get_settings()
    >>> print(settings.api_port)
    8000
    """
    return settings
