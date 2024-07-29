from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Admin:
    admin_id: str


@dataclass
class Config:
    tg_bot: TgBot
    admin: Admin

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")),
                  admin=Admin(admin_id=env("ADMIN_ID")))
