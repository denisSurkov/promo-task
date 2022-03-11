from typing import List

import uvicorn
from fastapi import FastAPI, Depends, status
from starlette.responses import JSONResponse

from database import Database, PromoNotFound, ParticipantNotFound, PrizeNotFound
from models import (PromoCreateModel, PromoShort, PromoFullData, ErrorModel,
                    ParticipantCreateModel, PrizeCreateModel, RaffleResult)
from raffle_service import RaffleNotPossible, RaffleService

app = FastAPI(
        title='Promo',
        responses={
            status.HTTP_404_NOT_FOUND: {
                'description': "Объект не найден",
                'model': ErrorModel,
            }
        }
)

runtime_database = Database()


def get_db():
    return runtime_database


@app.exception_handler(PromoNotFound)
def handle_promo_not_found(*_, **__):
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Promo not found'},
    )


@app.exception_handler(ParticipantNotFound)
def handle_promo_not_found(*_, **__):
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Participant not found'},
    )


@app.exception_handler(PrizeNotFound)
def handle_prize_not_found(*_, **__):
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'detail': 'Prize not found'},
    )


@app.exception_handler(RaffleNotPossible)
def handle_raffle_not_possible(*_, **__):
    return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'detail': 'Not possible to raffle'},
    )


@app.post('/promo',
          status_code=status.HTTP_201_CREATED,
          response_model=int)
def create_promo(promo_create_model: PromoCreateModel, db: Database = Depends(get_db)) -> int:
    result = db.add_promo(promo_create_model.name, promo_create_model.description)
    return result


@app.get('/promo',
         status_code=status.HTTP_200_OK,
         response_model=List[PromoShort])
def get_all_promo(db: Database = Depends(get_db)) -> List[PromoShort]:
    return db.get_all_promo_short_data()


@app.get('/promo/{promo_id}',
         status_code=status.HTTP_200_OK,
         response_model=PromoFullData)
def get_promo_full_data(promo_id: int, db: Database = Depends(get_db)) -> PromoFullData:
    return db.get_promo_full_data_by_id(promo_id)


@app.put('/promo/{promo_id}',
         status_code=status.HTTP_202_ACCEPTED)
def update_promo(promo_id: int, updated_promo: PromoCreateModel, db: Database = Depends(get_db)):
    db.update_promo(promo_id, updated_promo.name, updated_promo.description)


@app.delete('/promo/{promo_id}',
            status_code=status.HTTP_200_OK)
def delete_promo(promo_id: int, db: Database = Depends(get_db)):
    db.delete_promo(promo_id)


@app.post('/promo/{promo_id}/participant',
          status_code=status.HTTP_201_CREATED,
          response_model=int)
def create_participant(promo_id: int, participant: ParticipantCreateModel, db: Database = Depends(get_db)) -> int:
    return db.add_participant_to_promo(promo_id, participant.name)


@app.delete('/promo/{promo_id}/participant/{participant_id}')
def delete_participant(promo_id: int, participant_id: int, db: Database = Depends(get_db)):
    return db.delete_participant_from_promo(promo_id, participant_id)


@app.post('/promo/{id}/prize',
          status_code=status.HTTP_201_CREATED,
          response_model=int)
def create_prize(promo_id: int, prize: PrizeCreateModel, db: Database = Depends(get_db)) -> int:
    return db.add_prize(promo_id, prize.description)


@app.delete('/promo/{promo_id}/prize/{prize_id}',
            status_code=status.HTTP_200_OK)
def delete_prize(promo_id: int, prize_id: int, db: Database = Depends(get_db)):
    db.delete_prize(promo_id, prize_id)


@app.post('/promo/{promo_id}/raffle',
          description='Проведение розыгрыша призов в промоакции по идентификатору промоакции',
          response_model=List[RaffleResult],
          status_code=status.HTTP_200_OK,
          responses={
              status.HTTP_409_CONFLICT: {
                  "model": ErrorModel,
                  "description": "Проведение розыгрыша невозможно",
              }
          })
def raffle_promo(promo_id: int, db: Database = Depends(get_db)):
    promo_to_raffle = db.get_promo_full_data_by_id(promo_id)

    raffle_service = RaffleService(promo_to_raffle, db)
    return raffle_service.act()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
