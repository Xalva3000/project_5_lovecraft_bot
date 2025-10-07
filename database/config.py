from environs import Env
from os import name as os_name


class Settings:
    """трафарет сбора данных(переменных файла .env) под строку:
    postgresql: // [user[:password] @][netloc][:port][ / dbname][?param1 = value1 & ...]
    """

    def __init__(self, path):
        env = Env()
        env.read_env(path)
        self.DB_NETLOC = env("DB_NETLOC")
        self.DB_USER = env("DB_USER")
        self.DB_NAME = env("DB_NAME")
        self.DB_PASS = env("DB_PASS")
        self.DB_PORT = env("DB_PORT")

    #  функция подставляет значения переменных из файла .env и возвращает строку: url для соединения с БД
    #  будет использовано при инициализации sync_engine и async_engine в database.py
    def load_driver_url(self, *, dbs: str = "postgresql", driver: str = "asyncpg") -> str:
        url = f'{dbs}{"+" + driver if driver else ""}://{self.DB_USER}:{self.DB_PASS}@' \
              f'{self.DB_NETLOC}:{self.DB_PORT}/{self.DB_NAME}'
        return url


if os_name == 'nt':
    env_path = r"C:\i\project_5_kabbot\.env"
elif os_name == 'posix':
    env_path = "/home/kabbot/lovecraft_bot/.env"
else:
    raise ValueError('Unknown OS data. No path to .env file.')


settings = Settings(env_path)
