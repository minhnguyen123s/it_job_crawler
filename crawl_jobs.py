import os
import asyncio
import json
import csv
import re
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse
import unicodedata

load_dotenv()
print("API KEY =", os.getenv("BROWSER_USE_API_KEY"))

def normalize_text(text: str) -> str:
    """Normalize unicode + thay mọi dạng newline bằng space"""
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'\\?[\\r\\n]+', ' ', text)          # Xử lý \n literal và \\n escaped
    text = re.sub(r'\s+', ' ', text.strip())           # Nhiều space → 1 space
    return text

def normalize_key(key: str) -> str:
    """Chuẩn hóa key: xóa space thừa, sửa typo phổ biến"""
    clean = key.strip().lower()
    if "title" in clean or "job_t" in clean:
        return "job_title"
    if "compa" in clean or "name" in clean or "công ty" in clean:
        return "company_name"
    if "sala" in clean or "lương" in clean:
        return "salary"
    if "link" in clean or "detail" in clean or "url" in clean:
        return "job_detail_link"
    return clean  # giữ nguyên nếu không khớp

async def crawl_it_jobs():
    browser = Browser()
    llm = ChatBrowserUse()

    agent = Agent(
        task="""
Go to https://www.topcv.vn/tim-viec-lam-it-phan-mem

Extract exactly 10 job listings from the search results page.
Return ONLY a valid JSON array of objects. NOTHING else: no text, no markdown, no ```json, no explanation, no extra characters.

Each object MUST have exactly these 4 keys (exact spelling, no spaces around, no trailing spaces):
"job_title"
"company_name"
"salary"
"job_detail_link"

Rules nghiêm ngặt:
- Keys exactly as above: no extra spaces, no typos like "sala y ", "compa y_ ame ", "job_title "
- All string values use double quotes "
- Escape properly: no raw newlines inside strings (replace \\n with space if any)
- Clean company_name: remove ALL extra newlines, line breaks, multiple spaces → single space only
- Salary: giữ nguyên như trang (ví dụ: "Tới 30 triệu", "Thoả thuận", "Tới 70 triệu")
- job_detail_link: full absolute URL, bao gồm https://
- Exactly 10 items if possible, or as many as available
""",
        llm=llm,
        browser=browser,
    )

    print("Đang chạy agent...")

    history = await agent.run()

    final = history.final_result()

    if isinstance(final, dict):
        final_text = final.get("text") or final.get("content") or str(final)
    else:
        final_text = str(final)

    print("\n📄 RAW RESULT:")
    print(final_text)

    # Làm sạch toàn bộ text
    clean_text = normalize_text(final_text)

    print("\n🧹 CLEANED TEXT:")
    print(clean_text)

    # Tìm phần JSON array
    start = clean_text.find('[')
    end = clean_text.rfind(']') + 1

    if start == -1 or end <= start:
        print("❌ Không tìm thấy mảng JSON hợp lệ!")
        jobs = []
    else:
        json_str = clean_text[start:end]
        print("\n🔍 JSON string sau clean:")
        print(json_str)

        try:
            parsed_jobs = json.loads(json_str)
            print(f"✅ Parse trực tiếp thành công: {len(parsed_jobs)} jobs")

            # Normalize keys & values
            normalized_jobs = []
            expected_keys = {"job_title", "company_name", "salary", "job_detail_link"}

            for job in parsed_jobs:
                normalized = {}
                for k, v in job.items():
                    clean_key = normalize_key(k)
                    if clean_key in expected_keys:
                        normalized[clean_key] = v.strip() if isinstance(v, str) else v

                # Chỉ giữ job nếu có đủ 4 key
                if len(normalized) == 4:
                    normalized_jobs.append(normalized)
                else:
                    print(f"Bỏ qua job thiếu hoặc key không hợp lệ: {job}")

            jobs = normalized_jobs
            print(f"✅ Sau normalize & filter: {len(jobs)} jobs hợp lệ")

        except json.JSONDecodeError as e:
            print(f"❌ Lỗi json.loads: {e}")
            print("Vị trí lỗi:", e.pos)
            print("Đoạn gần lỗi:", json_str[max(0, e.pos-50):e.pos+50])
            jobs = []

    # Ghi file CSV
    if jobs:
        csv_filename = "it_jobs.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["job_title", "company_name", "salary", "job_detail_link"]
            )
            writer.writeheader()
            writer.writerows(jobs)
        print(f"✅ Đã xuất thành công {len(jobs)} jobs vào file: {csv_filename}")
    else:
        print("⚠️ Không có job nào hợp lệ để xuất file.")

if __name__ == "__main__":
    asyncio.run(crawl_it_jobs())