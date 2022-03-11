from typing import List

from database import Database
from models import PromoFullData, RaffleResult


class RaffleNotPossible(Exception):
    ...


class RaffleService:
    def __init__(self, promo_to_raffle: PromoFullData, db: Database):
        self._promo_to_raffle = promo_to_raffle
        self._db = db

    def act(self) -> List[RaffleResult]:
        self._check_if_prize_count_equals_participant_count()

        results: List[RaffleResult] = []

        for participant, prize in zip(self._promo_to_raffle.participants, self._promo_to_raffle.prizes):
            results.append(RaffleResult(
                    winner=participant,
                    prize=prize,
            ))

        return results

    def _check_if_prize_count_equals_participant_count(self):
        if len(self._promo_to_raffle.prizes) != len(self._promo_to_raffle.participants):
            raise RaffleNotPossible()
