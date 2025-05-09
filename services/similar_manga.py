from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(target_manga, all_mangas, top_n=8):
    # Gộp các đặc điểm thành một chuỗi văn bản
    def manga_to_text(manga):
        features = manga.get("tags", [])  # Lấy danh sách tags nếu có, nếu không có thì dùng danh sách rỗng
        author = str(manga.get("author", ""))
        artist = str(manga.get("artist", ""))
        
        # Nếu author và artist giống nhau, chỉ thêm một lần
        if author == artist:
            features += [author]
        else:
            features += [author, artist]
        # Lấy các trường khác và thay thế None bằng chuỗi rỗng
        features += [
            str(manga.get("publicationDemographic", "")),  
            str(manga.get("originalLanguage", "")),
            str(manga.get("year", ""))
        ]
        
        title = manga.get("title", "")
        title_words = title.split()[:3]  # Lấy 3 từ đầu tiên
        features += title_words
        
        # Nối các phần tử thành một chuỗi
        return " ".join(features)

    # Chuyển các manga thành các chuỗi văn bản
    all_texts = [manga_to_text(m) for m in all_mangas]
    target_text = manga_to_text(target_manga)

    # Vector hóa văn bản
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([target_text] + all_texts)

    # Tính cosine similarity (với dòng đầu tiên là manga target)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Lọc ra kết quả có độ tương đồng cao nhất
    similarities = list(enumerate(cosine_similarities))
    
    # Xác định index của manga mục tiêu
    target_index = next((index for index, manga in enumerate(all_mangas) if manga["id"] == target_manga["id"]), None)
    
    # Loại bỏ manga mục tiêu khỏi kết quả
    if target_index is not None:
        similarities = [pair for pair in similarities if pair[0] != target_index]
    
    # Sắp xếp các kết quả theo độ tương đồng giảm dần
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    # Lấy top N manga có độ tương đồng cao nhất 
    similar_indices = [index for index, _ in sorted_similarities[:top_n]]
    similar_mangas = [all_mangas[i] for i in similar_indices]

    return similar_mangas
