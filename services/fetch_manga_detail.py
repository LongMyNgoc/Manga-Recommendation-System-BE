import httpx
from fastapi import HTTPException
from services.fetch_mangas import fetch_mangas
from services.similar_manga import compute_similarity

MANGADEX_API = "https://api.mangadex.org/manga"

async def fetch_manga_detail(manga_id: str):
    url = f"{MANGADEX_API}/{manga_id}?includes[]=cover_art&includes[]=author&includes[]=artist"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Manga not found")

        manga = response.json()["data"]

        # Fetch các thông tin chính của manga
        title = manga["attributes"]["title"].get("en", "No title available")
        description = manga["attributes"].get("description", {}).get("en", "No description available")
        status = manga["attributes"].get("status", "Unknown")
        tags = [tag["attributes"]["name"]["en"] for tag in manga["attributes"]["tags"]]
        year = manga["attributes"].get("year", "Unknown Year")
        publication_demographic = manga["attributes"].get("publicationDemographic", "Unknown")
        original_language = manga["attributes"].get("originalLanguage", "Unknown")
        created_at = manga["attributes"].get("createdAt", "Unknown")
        updated_at = manga["attributes"].get("updatedAt", "Unknown")

        # Fetch ảnh bìa (cover art)
        cover_rel = next((rel for rel in manga["relationships"] if rel["type"] == "cover_art"), None)
        cover_url = (
            f"https://uploads.mangadex.org/covers/{manga_id}/{cover_rel['attributes']['fileName']}.256.jpg"
            if cover_rel else "https://via.placeholder.com/100x150"
        )

        # Fetch tác giả và họa sĩ từ relationships
        author = next((rel["attributes"]["name"] for rel in manga["relationships"] if rel["type"] == "author"), "Unknown")
        artist = next((rel["attributes"]["name"] for rel in manga["relationships"] if rel["type"] == "artist"), "Unknown")

        # Fetch các liên kết bên ngoài (nếu có)
        external_links = []
        if "externalLinks" in manga["attributes"]:
            external_links = [link["url"] for link in manga["attributes"]["externalLinks"]]
        
        # Sau khi bạn lấy được chi tiết manga    
        all_mangas_data = await fetch_mangas(total=900)  # hoặc nhiều hơn
        all_mangas = all_mangas_data["mangas"]
        # Tìm manga gốc trong danh sách để so sánh
        target_manga = next((m for m in all_mangas if m["id"] == manga_id), None)
        if target_manga:
            similar_mangas = compute_similarity(target_manga, all_mangas)
        else:
            similar_mangas = []

        # Trả về tất cả thông tin đã fetch
        return {
            "id": manga_id,
            "title": title,
            "description": description,
            "status": status,
            "tags": tags,
            "author": author,
            "artist": artist,
            "year": year,
            "publicationDemographic": publication_demographic,
            "originalLanguage": original_language,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "coverUrl": cover_url,
            "externalLinks": external_links,
            "similar": similar_mangas
        }
