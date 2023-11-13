from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str

@dataclass
class WebHookSettings:
    bot_token: str
    ngrok_url: str

    def __post_init__(self):
        self.webhook_path = f"/bot/{self.bot_token}"
        self.webhook_url = f"{self.ngrok_url}{self.webhook_path}"

    def __repr__(self):
        return "<'class WebHookSettings'>"


@dataclass
class Config:
    tg_bot: TgBot

def load_webhook_settings(path: str | None = None) -> WebHookSettings:
    env = Env()
    env.read_env(path)
    return WebHookSettings(bot_token=env("BOT_TOKEN"),
                           ngrok_url=env("NGROK_URL"))



def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")))
