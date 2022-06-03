from prettyconf import config


class Settings:
    APP_NAME = "aquarela-users-api"
    LOG_LEVEL = config("LOG_LEVEL", default="INFO")
    ENVIRONMENT = config("FLASK_ENV")
    POSTGRES_URL = config('POSTGRES_URL')
    POSTGRES_USER = config('POSTGRES_USER')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
    POSTGRES_DB = config('POSTGRES_DB')
    POSTGRES_DB_TEST = config('POSTGRES_DB_TEST')


settings = Settings()


class Config(object):
    DEBUG = False
    TESTING = False

    # SQLAlchemy
    uri_template = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = uri_template.format(
        user=settings.POSTGRES_USER,
        pw=settings.POSTGRES_PASSWORD,
        url=settings.POSTGRES_URL,
        db=settings.POSTGRES_DB)

    # Silence the deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API settings
    API_PAGINATION_PER_PAGE = 10


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    uri_template = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = uri_template.format(
        user=settings.POSTGRES_USER,
        pw=settings.POSTGRES_PASSWORD,
        url=settings.POSTGRES_URL,
        db=settings.POSTGRES_DB_TEST)


class ProductionConfig(Config):
    # production config
    pass


def get_config(env=None):
    if env is None:
        try:
            env = settings.ENVIRONMENT
        except Exception:
            env = 'development'
            print('env is not set, using env:', env)

    if env == 'production':
        return ProductionConfig()
    elif env == 'test':
        return TestConfig()

    return DevelopmentConfig()
