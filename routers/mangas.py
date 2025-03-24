from fastapi import APIRouter
from services.mangadex_service import fetch_mangas, fetch_manga_detail

router = APIRouter()

@router.get("/mangas")
async def get_mangas():
    return await fetch_mangas()  # Không cần truyền limit, offset

@router.get("/mangas/{manga_id}")
async def get_manga_detail(manga_id: str):
    return await fetch_manga_detail(manga_id)
