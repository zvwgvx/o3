from pathlib import Path
import tempfile
import shutil
import os
import PyPDF2
from openai import OpenAI

client = OpenAI(
    api_key="sk-lDVNmbyUstXtvFc0pikfr7pTejJ",
    base_url="https://proxyvn.top/"
)


with open("input.txt", "r", encoding="utf-8") as f:
    inp = f.read().strip()


if os.path.exists("problem.pdf"):
    with open("problem.pdf", "rb") as f:
        reader = PyPDF2.PdfReader(f)
        txt = "".join(page.extract_text() or "" for page in reader.pages)
else:
    txt = inp

prompt = inp if inp else "Hãy suy nghĩ thật kĩ và giải bài tập với c++"
msg = prompt + txt


response = client.chat.completions.create(
    model="o3-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "Bạn là competitive programmer cực giỏi, khi code bạn không "
                "bao giờ thêm comment vào code và bạn luôn đặt tên biến theo "
                "chuẩn join_case và ngắn gọn. Khi trả lời tôi thì bạn chỉ trả "
                "lời code không nói thêm gì nhưng phải đúng format code tránh "
                "output tất cả nằm trên 1 dòng và dùng tab. Đặc biệt bạn code rất clean"
            )
        },
        {"role": "user", "content": msg}
    ],
    temperature=0.2,
)

content = response.choices[0].message.content

out_path = Path.cwd() / "solution.cpp"

with tempfile.NamedTemporaryFile(
    mode="w",
    delete=False,
    encoding="utf-8-sig",
    newline="\n",
    dir=out_path.parent,
    suffix=".cpp"
) as tmp:
    tmp.write(content)
    tmp.flush()

shutil.move(tmp.name, out_path)
