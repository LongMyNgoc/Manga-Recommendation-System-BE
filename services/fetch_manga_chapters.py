import httpx
from fastapi import HTTPException

async def fetch_manga_chapters(manga_id: str, limit: int = 100):
    url = f"https://api.mangadex.org/chapter"
    params = {
        "manga": manga_id,
        "translatedLanguage[]": "en",
        "order[chapter]": "asc",
        "limit": limit
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch chapters")

        chapters_data = response.json()["data"]

        chapters = [
            {
                "id": chap["id"],
                "chapter": chap["attributes"].get("chapter", "Oneshot"),
                "title": chap["attributes"].get("title", ""),
                "volume": chap["attributes"].get("volume", ""),
                "createdAt": chap["attributes"].get("createdAt", ""),
            }
            for chap in chapters_data
        ]

        return chapters
