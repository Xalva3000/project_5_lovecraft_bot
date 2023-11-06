from environs import Env


class Settings:
    """трафарет сбора данных под строку
    # postgresql: // [user[:password] @][netloc][:port][ / dbname][?param1 = value1 & ...]
    """

    def __init__(self, path):
        env = Env()
        env.read_env(path)
        self.DB_NETLOC = env("DB_NETLOC")
        self.DB_USER = env("DB_USER")
        self.DB_NAME = env("DB_NAME")
        self.DB_PASS = env("DB_PASS")
        self.DB_PORT = env("DB_PORT")

    def load_driver_url(self, *, dbs: str = "postgresql", driver: str = "asyncpg"):
        url = f'{dbs}{"+" + driver if driver else ""}://{self.DB_USER}:{self.DB_PASS}@{self.DB_NETLOC}:{self.DB_PORT}/{self.DB_NAME}'
        return url


settings = Settings("C:\i\project_5_kabbot\.env")

# Settings("/home/kabbot/kabbot/project_5_kabbot/.env")
