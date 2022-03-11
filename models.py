from typing import Optional, List

from pydantic import BaseModel


class PromoCreateModel(BaseModel):
    name: str
    description: Optional[str] = None


class PromoShort(PromoCreateModel):
    id: int


class PrizeCreateModel(BaseModel):
    description: str


class PrizeModel(PrizeCreateModel):
    id: int


class ParticipantCreateModel(BaseModel):
    name: str


class ParticipantModel(ParticipantCreateModel):
    id: int


class PromoFullData(PromoShort):
    prizes: List[PrizeModel]
    participants: List[ParticipantModel]


class RaffleResult(BaseModel):
    winner: ParticipantModel
    prize: PrizeModel


class ErrorModel(BaseModel):
    detail: str
