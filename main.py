from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MANGADEX_API = "https://api.mangadex.org/manga"

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Manga API!"}

@app.get("/mangas")
async def get_mangas(limit: int = 10, offset: int = 0):
    params = {
        "limit": limit,
        "offset": offset,
        "includes[]": "cover_art"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(MANGADEX_API, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch mangas")

        data = response.json()
        mangas = []

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

        return {"mangas": mangas}

# ✅ API để lấy chi tiết 1 Manga theo ID
@app.get("/mangas/{manga_id}")
async def get_manga_detail(manga_id: str):
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
