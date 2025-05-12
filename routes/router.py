from fastapi import APIRouter

from views import upload, query

# Add route with prefix /api/v1 to manage v1 APIs.
router = APIRouter(prefix="/api/v1")

# Route for upload and query.
router.include_router(upload.router, tags=["Upload Endpoints"])
router.include_router(query.router, tags=["Query Endpoints"])
