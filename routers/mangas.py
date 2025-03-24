from fastapi import APIRouter
from services.fetch_mangas import fetch_mangas
from services.fetch_manga_detail import fetch_manga_detail

router = APIRouter()

@router.get("/mangas")
async def get_mangas():
    return await fetch_mangas()  # Không cần truyền limit, offset

@router.get("/mangas/{manga_id}")
async def get_manga_detail(manga_id: str):
    return await fetch_manga_detail(manga_id)
