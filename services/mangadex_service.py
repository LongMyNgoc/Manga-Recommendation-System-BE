import httpx
from fastapi import HTTPException

MANGADEX_API = "https://api.mangadex.org/manga"

async def fetch_mangas(total: int = 300):
    limit = 100  # Số lượng tối đa cho mỗi request
    mangas = []

    async with httpx.AsyncClient() as client:
        for offset in range(0, total, limit):
            params = {
                "limit": limit,
                "offset": offset,
                "includes[]": "cover_art"
            }

            response = await client.get(MANGADEX_API, params=params)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch mangas")

            data = response.json()

            for manga in data.get("data", []):
                title = manga["attributes"]["title"].get("en", "No title available")
                status = manga["attributes"].get("status", "Unknown")
                tags = [tag["attributes"]["name"]["en"] for tag in manga["attributes"]["tags"]]

                cover_rel = next((rel for rel in manga["relationships"] if rel["type"] == "cover_art"), None)
                cover_url = (
                    f"https://uploads.mangadex.org/covers/{manga['id']}/{cover_rel['attributes']['fileName']}.256.jpg"
                    if cover_rel else "https://via.placeholder.com/100x150"
                )

                mangas.append({
                    "id": manga["id"],
                    "title": title,
                    "status": status,
                    "tags": tags,
                    "coverUrl": cover_url
                })

            # Nếu số manga nhận được ít hơn limit, nghĩa là đã fetch hết
            if len(data.get("data", [])) < limit:
                break

    return {"mangas": mangas}

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
