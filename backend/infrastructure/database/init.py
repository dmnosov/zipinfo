from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from infrastructure.adapters import MinioAdapter
from infrastructure.settings import settings

engine = create_async_engine(settings.get_postgres_dsn())
async_session_maker = async_sessionmaker(engine)

# init object storage
s3 = MinioAdapter(
    access_key=settings.object_storage.access_key_id,
    secret_key=settings.object_storage.secret_access_key,
    endpoint_url=settings.object_storage.host,
    port=settings.object_storage.port,
)
