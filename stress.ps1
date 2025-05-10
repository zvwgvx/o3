# script.ps1
# Bật strict mode để catch lỗi
Set-StrictMode –Version Latest
$ErrorActionPreference = 'Stop'

# 1) Đọc prompt từ file prompt.txt (giữ nguyên xuống dòng)
$USER_PROMPT = Get-Content -Raw -Path 'prompt.txt'

# 2) Chuẩn bị body JSON
$body = @{
    model = 'o3-mini'
    messages = @(
        @{
            role    = 'system'
            content = 'Bạn là competitive programmer cực giỏi, khi code bạn không bao giờ thêm comment vào code và bạn luôn đặt tên biến theo chuẩn join_case và ngắn gọn. Khi trả lời tôi thì bạn chỉ trả lời code không nói thêm gì nhưng phải đúng format code tránh output tất cả nằm trên 1 dòng và dùng tab. Đặc biệt bạn code rất clean'
        }
        @{
            role    = 'user'
            content = $USER_PROMPT
        }
    )
    temperature = 0.2
} | ConvertTo-Json -Depth 5

# 3) Gửi request đến proxyvn.top và nhận response
$response = Invoke-RestMethod `
    -Method Post `
    -Uri 'https://proxyvn.top/v1/chat/completions' `
    -Headers @{
        'Content-Type'  = 'application/json'
        'Authorization' = 'Bearer sk-lDVNmbyUstXtvFc0pikfr7pTejJ'
    } `
    -Body $body

# 4) Trích code raw, bỏ fence ``` nếu có, và ghi vào main.cpp
$code = $response.choices[0].message.content

# Nếu có ```cpp … ```, loại bỏ chúng
$code = $code -replace '```[a-z]*', '' -replace '```$', ''

# Ghi file với encoding UTF8 no BOM
[IO.File]::WriteAllText('main.cpp', $code, [Text.Encoding]::UTF8)

Write-Host 'Đã tạo thành công file main.cpp'
