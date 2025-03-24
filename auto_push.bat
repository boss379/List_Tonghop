@echo off
cd /d C:\xampp\htdocs\vieon

REM Gọi script PHP qua web server thay vì chạy trực tiếp
curl -s http://localhost/vieon/get_link.php > nul

REM Kiểm tra lỗi khi chạy PHP
if %errorlevel% neq 0 (
    echo ❌ Lỗi khi gọi get_link.php qua localhost!
    exit /b %errorlevel%
)

REM Lưu thay đổi hiện tại trước khi pull
git stash
git pull --rebase origin main || (echo ❌ Lỗi khi pull! && exit /b 1)
git stash pop

REM Kiểm tra xem file có thay đổi không
git add vtv_playlist.m3u channels_updated.txt
git diff --quiet vtv_playlist.m3u channels_updated.txt && (echo ✅ Không có thay đổi, thoát. && exit /b 0)

REM Nếu có thay đổi thì commit và push
echo 🚀 Đang push thay đổi lên GitHub...
git commit -m "Auto-update vtv_playlist.m3u và channels_updated.txt" && git push origin main
