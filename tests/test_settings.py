from rctl_bot.config import Settings


def test_settings_parse_comma_separated_admin_ids() -> None:
    settings = Settings(
        BOT_TOKEN="123456:token",
        ADMIN_TELEGRAM_IDS="1001, 1002,1003",
    )

    assert settings.bot_token == "123456:token"
    assert settings.admin_telegram_ids == frozenset({1001, 1002, 1003})
