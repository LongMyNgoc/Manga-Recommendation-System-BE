import httpx
from fastapi import HTTPException

async def fetch_chapter_pages(chapter_id: str):
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch chapter pages")

        data = response.json()
        base_url = data["baseUrl"]
        chapter_info = data["chapter"]
        hash_val = chapter_info["hash"]
        data_files = chapter_info["data"]  # danh sách các tệp ảnh

        # Tạo URL đầy đủ cho từng trang ảnh
        image_urls = [f"{base_url}/data/{hash_val}/{filename}" for filename in data_files]

        return image_urls
