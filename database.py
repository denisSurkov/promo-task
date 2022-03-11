from typing import Optional, List, Dict

from models import PromoFullData, PromoShort, ParticipantModel, PrizeModel


class PromoNotFound(Exception):
    ...


class ParticipantNotFound(Exception):
    ...


class PrizeNotFound(Exception):
    ...


class Database(dict, Dict[int, PromoFullData]):
    """
        Класс для работы с "базой данных".

        Служит оберткой до словаря.

        Поскольку нет требований к подключению базы данных,
        я принял решение хранить данные в рамках одного рантайма.
    """

    def __init__(self):
        super().__init__()

        self._created_promo_count = 0
        self._created_participants = 0
        self._created_prizes_count = 0

    def add_promo(self, name: str, description: Optional[str]) -> int:
        self._created_promo_count += 1

        new_promo_model = PromoFullData(
                id=self._created_promo_count,
                name=name,
                description=description,
                prizes=[],
                participants=[],
        )

        self[self._created_promo_count] = new_promo_model

        return self._created_promo_count

    def update_promo(self, promo_id: int, name: str, description: Optional[str]):
        self._check_if_promo_exists(promo_id)

        promo_in_db: PromoFullData = self.get(promo_id)
        promo_in_db.name = name
        promo_in_db.description = description

    def delete_promo(self, promo_id: int):
        self._check_if_promo_exists(promo_id)

        del self[promo_id]

    def get_promo_full_data_by_id(self, promo_id: int) -> PromoFullData:
        self._check_if_promo_exists(promo_id)

        return self[promo_id]

    def get_all_promo_short_data(self) -> List[PromoShort]:
        answer = []

        for _, full_data in self.items():
            full_data: PromoFullData

            answer.append(
                    PromoShort(**full_data.dict())
            )

        return answer

    def add_participant_to_promo(self, promo_id: int, name: str) -> int:
        self._check_if_promo_exists(promo_id)

        self._created_participants += 1
        participant_model = ParticipantModel(
                id=self._created_participants,
                name=name,
        )

        self[promo_id].participants.append(participant_model)

        return self._created_participants

    def delete_participant_from_promo(self, promo_id: int, participant_id: int):
        self._check_if_promo_exists(promo_id)

        all_participants = self[promo_id].participants

        for i, participant in enumerate(all_participants, 0):
            if participant.id == participant_id:
                index_to_delete = i
                break
        else:
            raise ParticipantNotFound()

        del all_participants[index_to_delete]

    def add_prize(self, promo_id: int, description: str) -> int:
        self._check_if_promo_exists(promo_id)

        self._created_prizes_count += 1
        new_prize_model = PrizeModel(
                id=self._created_prizes_count,
                description=description,
        )

        prizes = self[promo_id].prizes
        prizes.append(new_prize_model)

        return self._created_prizes_count

    def delete_prize(self, promo_id: int, prize_id: int):
        self._check_if_promo_exists(promo_id)

        all_prizes = self[promo_id].prizes

        for i, prize in enumerate(all_prizes, 0):
            if prize.id == prize_id:
                index_to_delete = i
                break
        else:
            raise PrizeNotFound()

        del all_prizes[index_to_delete]

    def _check_if_promo_exists(self, promo_id):
        if promo_id not in self:
            raise PromoNotFound()
