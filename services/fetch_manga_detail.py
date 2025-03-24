import httpx
from fastapi import HTTPException

MANGADEX_API = "https://api.mangadex.org/manga"

async def fetch_manga_detail(manga_id: str):
    url = f"{MANGADEX_API}/{manga_id}?includes[]=cover_art"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Manga not found")

        manga = response.json()["data"]

        title = manga["attributes"]["title"].get("en", "No title available")
        status = manga["attributes"].get("status", "Unknown")
        tags = [tag["attributes"]["name"]["en"] for tag in manga["attributes"]["tags"]]

        cover_rel = next((rel for rel in manga["relationships"] if rel["type"] == "cover_art"), None)
        cover_url = (
            f"https://uploads.mangadex.org/covers/{manga_id}/{cover_rel['attributes']['fileName']}.256.jpg"
            if cover_rel else "https://via.placeholder.com/100x150"
        )

        return {
            "id": manga_id,
            "title": title,
            "status": status,
            "tags": tags,
            "coverUrl": cover_url
        }
