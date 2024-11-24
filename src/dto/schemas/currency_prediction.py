"""Machine learning model signs dto"""

from fastapi import Query
from pydantic import BaseModel, Field

from src.utils.enums import CurrencyPair, Message


class SignsDTO(BaseModel):
    currency_pair: CurrencyPair = Field(example=CurrencyPair.usd_rub)
    last_values: list[float] = Field(Query(
        min_length=5,
        example=[99.3, 99.8, 98.9, 99.5, 100.3, 102.6],
        description="Last values of currency pair. The more values, the better the forecast."
    ))
    day_of_week: int | None = Field(default=0, ge=0, le=6, example=0)
    retrograde_mercury: bool = Field(
        default=False, example=False, description="Is there a period of retrograde mercury now?"
    )


class PredictionResponse(BaseModel):
    currency_pair: CurrencyPair
    predicted_value: float
    msg: Message
