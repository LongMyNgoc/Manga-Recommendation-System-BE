from fastapi import APIRouter
from services.fetch_mangas import fetch_mangas
from services.fetch_manga_detail import fetch_manga_detail
from services.fetch_manga_chapters import fetch_manga_chapters
from services.fetch_chapter_pages import fetch_chapter_pages

router = APIRouter()

@router.get("/mangas")
async def get_mangas():
    return await fetch_mangas()  # Không cần truyền limit, offset

@router.get("/mangas/{manga_id}")
async def get_manga_detail(manga_id: str):
    return await fetch_manga_detail(manga_id)

@router.get("/mangas/{manga_id}/chapters")
async def get_manga_chapters(manga_id: str):
    return await fetch_manga_chapters(manga_id)

@router.get("/chapter/{chapter_id}/pages")
async def get_chapter_pages(chapter_id: str):
    return await fetch_chapter_pages(chapter_id)

