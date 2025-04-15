import logging
from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from application.routes.dependencies import JWTBearer
from application.schemas import Message, UploadZipResponse
from application.tasks import process_archive
from domain.services import ReportService

router = APIRouter(prefix="/upload", tags=["Загрузки"])


@router.post(
    "",
    description="Отправка ZIP-архива на проверку",
    response_model=UploadZipResponse,
    responses={400: {"model": Message}},
    status_code=201,
)
async def upload_zip(
    background_tasks: BackgroundTasks,
    user_id: UUID = Depends(JWTBearer()),
    file: UploadFile = File(description="ZIP архив для проверки"),
):
    if file.headers.get("content-type") != "application/zip":
        return JSONResponse(
            content=Message(error="Uploaded file should be zip").model_dump(),
            status_code=400,
        )
    content = await file.read()

    task_id = uuid4()
    await ReportService.create(task_id)

    background_tasks.add_task(
        process_archive,
        task_id=task_id,
        user_id=user_id,
        data=content,
        filename=file.filename,
    )
    return JSONResponse(
        content=jsonable_encoder(UploadZipResponse(task_id=task_id)),
        status_code=201,
    )
