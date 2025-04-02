@echo off
chcp 65001 >nul

:: Lấy ngày hiện tại dạng dd/mm (ví dụ: 28/03)
for /f "tokens=1-3 delims=/" %%a in ("%date%") do (
    set current_date=%%a/%%b
)

:: Kiểm tra file log
if exist check_log.txt (
    for /f "delims=" %%i in (check_log.txt) do set log_date=%%i
    if "%log_date%" == "%current_date%" (
        echo ĐÃ CHẠY SCRIPT TRONG NGÀY %current_date%. DỪNG LẠI!
        pause
        exit /b
    )
)

:: Ghi ngày mới vào file log
echo %current_date% > check_log.txt

:: Phần chính của script
echo ĐANG CHẠY LẦN ĐẦU TRONG NGÀY %current_date%
echo Thực hiện các tác vụ chính...

:: Thêm các lệnh của bạn ở đây
cd /d D:\vieon
python get_channels.py
python convert_m3u8.py
git add channels_updated.txt
git commit -m "Cập nhật tự động"
git push

echo HOÀN THÀNH TẤT CẢ TÁC VỤ!
pause