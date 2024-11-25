"""Currency prediction service"""

from random import uniform

from dto.schemas.currency_prediction import SignsDTO
from utils.enums import Message


class CurrencyPredictionService:

    @staticmethod
    async def get_prediction(signs: SignsDTO):
        """Get currency prediction"""

        factor = 1 + signs.day_of_week / (30 if signs.retrograde_mercury else 60)
        return {
            "currency_pair": signs.currency_pair,
            "predicted_value": round(uniform(min(signs.last_values) / factor, max(signs.last_values) * factor), 1),
            "msg": Message.not_ok if signs.retrograde_mercury else Message.ok,
        }
