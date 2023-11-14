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
        self.webhook_path = f"/{self.bot_token}"
        self.webhook_url = f"{self.ngrok_url}{self.webhook_path}"
        self.set_webhook_url = f"https://api.telegram.org/bot{self.bot_token}/setwebhook?url=https://3e97-81-23-183-47.ngrok-free.app"
        self.delete_webhook_url = f"https://api.telegram.org/bot{self.bot_token}/deletewebhook?url=https://3e97-81-23-183-47.ngrok-free.app"
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
