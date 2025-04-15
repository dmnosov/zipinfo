from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from application.routes.dependencies import JWTBearer
from application.schemas import GetResultByIdResponse, Message
from domain.services.report_service import ReportService

router = APIRouter(prefix="/report", tags=["Результат"])


@router.get(
    "/{id}",
    description="Получение результатов проверки",
    response_model=GetResultByIdResponse,
    responses={404: {"model": Message}},
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
async def get_result(id: Annotated[UUID, Path(title="ID задачи")]):
    result = await ReportService.find(id)
    if result is None:
        return JSONResponse(
            content=Message(error="Задача не найдена"),
            status_code=404,
        )
    return JSONResponse(
        content=jsonable_encoder(
            GetResultByIdResponse(
                status=result.status,
                results=GetResultByIdResponse.Result(
                    sonarqube=result.data,
                )
                if result.data is not None
                else None,
            )
        ),
        status_code=200,
    )
