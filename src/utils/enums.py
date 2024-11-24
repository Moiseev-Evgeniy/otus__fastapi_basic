from enum import StrEnum


class CurrencyPair(StrEnum):
    usd_rub = "USD/RUB"
    eur_rub = "EUR/RUB"
    eur_usd = "EUR/USD"
    gbr_usd = "GBP/USD"
    usd_jpy = "USD/JPY"


class Message(StrEnum):
    ok = "Just do it!"
    not_ok = "Be careful!"
