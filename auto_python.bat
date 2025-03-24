@echo off
chcp 65001 >nul
cd /d "C:\xampp\htdocs\vieon"
:: Chạy file Python convert_m3u8.py
echo Đang chạy convert_m3u8.py...
python convert_m3u8.py
echo Đã hoàn thành!
pause