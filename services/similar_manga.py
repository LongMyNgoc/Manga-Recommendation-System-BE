from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(target_manga, all_mangas, top_n=5):
    # Gộp các đặc điểm thành một chuỗi văn bản
    def manga_to_text(manga):
        features = manga.get("tags", [])  # Lấy danh sách tags nếu có, nếu không có thì dùng danh sách rỗng
        # Lấy các trường khác và thay thế None bằng chuỗi rỗng
        features += [
            str(manga.get("status", "")),  # Chuyển `None` thành chuỗi rỗng
            str(manga.get("publicationDemographic", "")),  # Chuyển `None` thành chuỗi rỗng
            str(manga.get("originalLanguage", ""))  # Chuyển `None` thành chuỗi rỗng
        ]
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

    # Lấy top N manga có độ tương đồng cao nhất
    similar_indices = cosine_similarities.argsort()[::-1][:top_n]
    similar_mangas = [all_mangas[i] for i in similar_indices]

    return similar_mangas
