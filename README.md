# IT Job Crawler (Browser-Use)

Project này dùng **browser-use** để tự động mở trình duyệt, crawl dữ liệu tuyển dụng IT từ **TopCV** và xuất ra file CSV.

---

## 🎯 Chức năng

* Truy cập trang TopCV (việc làm IT phần mềm)
* Tự động scroll và thu thập **10 job listings**
* Lấy các thông tin:

  * Job title
  * Company name
  * Salary
  * Job detail link
* Xuất kết quả ra file **`it_jobs.csv`**

---

## 📂 Cấu trúc thư mục

```
it_job_crawler/
│
├─ crawl_jobs.py        # File chính để crawl dữ liệu
├─ .env                # Chứa API key
├─ it_jobs.csv         # File kết quả (sinh ra sau khi chạy)
├─ venv/               # Virtual environment (khuyến nghị)
```

---

## ⚙️ Yêu cầu môi trường

* Python **3.10+** (khuyến nghị 3.11)
* Có API key của **Browser-Use**

---

## 🔑 Cấu hình API key

Tạo file **`.env`** trong thư mục project:

```env
BROWSER_USE_API_KEY=sk-xxxxxxxxxxxxxxxx
```

⚠️ Lưu ý:

* Không để dấu ngoặc kép
* Sau khi sửa `.env`, hãy **restart terminal**

---

## 📦 Cài đặt thư viện

Kích hoạt virtual environment rồi chạy:

```bash
pip install browser-use python-dotenv
```

---

## ▶️ Cách chạy chương trình

```bash
python crawl_jobs.py
```

Sau khi chạy thành công, terminal sẽ hiển thị:

```
✅ Đã lưu it_jobs.csv
```

---

## 📄 Kết quả

File **`it_jobs.csv`** gồm các cột:
| job_title | company_name | salary | job_detail_link |

File được lưu với encoding **UTF-8-SIG**, mở tốt bằng:

* Excel
* Google Sheets

---

## 🛠️ Ghi chú kỹ thuật

* Agent **chỉ trả JSON**, không trực tiếp ghi file
* Việc ghi CSV được xử lý bằng Python để đảm bảo ổn định
* Không dùng `history[-1]` (không hỗ trợ trong browser-use)

---

## 🚀 Hướng mở rộng

* Crawl nhiều hơn 10 jobs
* Crawl nhiều trang (pagination)
* Truy cập trang chi tiết job để lấy mô tả
* Chuẩn hóa mức lương (min / max)
* Crawl thêm các nền tảng khác (ITviec, VietnamWorks)

---

## 👤 Tác giả

Nguyễn Hữu Minh

---

## 📜 License

Project phục vụ mục đích học tập và nghiên cứu.
