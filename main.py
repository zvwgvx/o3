import openai
import os
import PyPDF2

openai.api_base = "https://proxyvn.top"
openai.api_key = "sk-IhAhB9F5dl0qbp1CRGU6ZejnUNx"

with open("input.txt", "r") as f:
    inp = f.read().strip()

if os.path.exists("problem.pdf"):
	with open("problem.pdf", "rb") as f:
		r = PyPDF2.PdfReader(f)
		txt = ""
		for p in r.pages:
			txt += p.extract_text()
else:
	txt = inp

msg = (inp if inp else "Hãy suy nghĩ thật kĩ và giải bài tập với c++") + txt

response = openai.ChatCompletion.create(
    model="o3-mini",
    messages=[
        {"role": "system", "content": "Bạn là competitive programmer cực giỏi, khi code bạn không bao giờ thêm comment vào code và bạn luôn đặt tên biến theo chuẩn join_case và ngắn gọn. Khi trả lời tôi thì bạn chỉ trả lời code không nói thêm gì nhưng phải đúng format code tránh output tất cả nằm trên 1 dòng và dùng tab"},
		
        {"role": "user", "content": msg}
    ],
    temperature=0.2
)

with open("solution.cpp", "w") as f:
    f.write(response['choices'][0]['message']['content'])
