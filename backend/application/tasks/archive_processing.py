from secrets import token_hex
from uuid import UUID

from domain.services import ArchiveService, ReportService, UploadService
from infrastructure.adapters.sq import SonarqubeAdapter


async def process_archive(
    task_id: UUID,
    data: bytes,
    user_id: UUID,
    filename: str | None = None,
) -> None:
    if filename is None:
        filename = f"{token_hex(8)}.zip"
    upload_id = await UploadService.create(filename, user_id)
    await ArchiveService.save_archive(data, f"{upload_id}.zip")

    # send request to external API
    result = await SonarqubeAdapter.scan()
    await ReportService.update_data(task_id, result)
