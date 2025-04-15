from .reports import router as report_router
from .uploads import router as upload_router

routers = [upload_router, report_router]
