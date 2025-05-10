import subprocess
import json

# Đọc nội dung từ prompt.txt
with open('prompt.txt', 'r', encoding='utf-8') as f:
    user_prompt = f.read()

# Tạo payload JSON
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": (
                "Bạn là competitive programmer cực giỏi, khi code bạn không bao giờ thêm comment vào code "
                "và bạn luôn đặt tên biến theo chuẩn join_case và ngắn gọn. Khi trả lời tôi thì bạn chỉ trả lời code "
                "không nói thêm gì nhưng phải đúng format code tránh output tất cả nằm trên 1 dòng và dùng tab. "
                "Đặc biệt bạn code rất clean"
            )
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    "temperature": 0.2
}

# Chuyển payload thành chuỗi JSON
payload_str = json.dumps(payload, ensure_ascii=False)

# Gọi lệnh curl thông qua subprocess
result = subprocess.run(
    [
        "curl",
        "-s",
        "-X", "POST",
        "https://proxyvn.top/v1/chat/completions",
        "-H", "Content-Type: application/json",
        "-H", "Authorization: Bearer sk-lDVNmbyUstXtvFc0pikfr7pTejJ",
        "-d", payload_str
    ],
    capture_output=True,
    text=True
)

# Kiểm tra xem lệnh curl có thành công không
if result.returncode != 0:
    print("Lỗi khi gọi curl:")
    print(result.stderr)
    exit(1)

# Phân tích kết quả JSON
try:
    response_json = json.loads(result.stdout)
    content = response_json['choices'][0]['message']['content']
except (json.JSONDecodeError, KeyError) as e:
    print("Lỗi khi phân tích kết quả JSON:")
    print(e)
    exit(1)

# Loại bỏ các dấu ``` nếu có
if content.startswith("```"):
    lines = content.splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    content = "\n".join(lines)

# Ghi kết quả vào tệp main.cpp
with open('main.cpp', 'w', encoding='utf-8') as f:
    f.write(content)

print("Đã tạo thành công file main.cpp")
