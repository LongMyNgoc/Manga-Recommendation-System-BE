# Manga Recommendation System (Back-End)

## Giới Thiệu
Chào mừng bạn đến với **Manga Recommendation System**! Đây là một hệ thống gợi ý manga được xây dựng để giúp người dùng khám phá các manga thú vị từ MangaDex. Dự án sử dụng thuật toán **Content-Based Filtering** để gợi ý các manga dựa trên nội dung của manga mà người dùng đang xem, giúp họ dễ dàng tìm thấy những manga tương tự và phù hợp với sở thích cá nhân.

## Tính Năng Chính
- **Hiển thị danh sách Manga**: Trang chủ sẽ hiển thị một danh sách tất cả các manga, cho phép người dùng duyệt qua các lựa chọn manga khác nhau.
- **Xem thông tin chi tiết Manga**: Người dùng có thể click vào một manga bất kỳ để xem các thông tin chi tiết về manga đó, bao gồm tên, tác giả, thể loại, tóm tắt nội dung, v.v.
- **Gợi ý truyện Manga**: Dựa trên manga người dùng vừa chọn, hệ thống sẽ tự động gợi ý các manga tương tự, giúp người dùng khám phá thêm nhiều truyện có chủ đề hoặc thể loại tương đồng.

## Công Nghệ Sử Dụng
- **FastAPI**: Đây là framework API hiện đại và mạnh mẽ giúp xây dựng các dịch vụ web với hiệu suất cao và khả năng dễ dàng phát triển. FastAPI hỗ trợ xây dựng các API RESTful và sinh tự động tài liệu API qua OpenAPI, giúp quá trình phát triển trở nên nhanh chóng và hiệu quả.
- **Render**: Được sử dụng để triển khai hệ thống lên môi trường production với khả năng tự động scale ứng dụng, dễ dàng cấu hình và triển khai các dịch vụ web.

## Yêu Cầu Hệ Thống
Trước khi bắt đầu, bạn cần cài đặt phiên bản **Python 3.10.11** (hoặc phiên bản tương thích) trên hệ thống của mình.

### Các thư viện cần thiết:
1. **FastAPI** cho việc xây dựng các endpoint API.
2. **uvicorn** để chạy ứng dụng FastAPI trên môi trường phát triển.

## Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1. Cài Đặt Dependencies
Trước tiên, bạn cần cài đặt tất cả các thư viện phụ thuộc của dự án. Mở terminal và chạy lệnh sau:
```bash
pip install -r requirements.txt
```

### 2. Khởi động server phát triển
Chạy lệnh sau để khởi động dự án:
```bash
python main.py
```

Hệ thống sẽ chạy trên **localhost**, bạn có thể truy cập bằng trình duyệt để kiểm tra giao diện và tính năng.

## Liên kết hệ thống
- **Back-End (GitHub)**: https://github.com/LongMyNgoc/Manga-Recommendation-System-BE.git
- **Back-End (Render)**: https://manga-recommendation-system-be.onrender.com/
- **Front-End (GitHub)**: https://github.com/LongMyNgoc/Manga-Recommendation-System.git
- **Front-End (Vercel)**: https://manga-recommendation-system.vercel.app/

## Đóng góp & Phát triển
Chúng tôi luôn chào đón sự đóng góp từ cộng đồng! Nếu bạn có bất kỳ ý tưởng, cải tiến hoặc báo lỗi nào, vui lòng gửi qua hệ thống quản lý mã nguồn của dự án. Bạn cũng có thể liên hệ trực tiếp với nhóm phát triển để thảo luận thêm.

## Thông tin liên hệ
📧 Email: nguyenphilong.dev@gmail.com 
