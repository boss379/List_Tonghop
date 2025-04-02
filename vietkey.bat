@echo off
chcp 65001 >nul

:: Kiểm tra Python có sẵn không
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python chưa được cài đặt hoặc không có trong PATH!
    pause
    exit /b
)

:: Chuyển đến thư mục D:\vieon
cd /d D:\vieon
if errorlevel 1 (
    echo Không thể chuyển đến D:\vieon. Kiểm tra thư mục có tồn tại và quyền truy cập không!
    pause
    exit /b
)

:: Chạy file Python convert_m3u8.py
echo Đang chạy convert_m3u8.py...
if exist convert_m3u8.py (
    python convert_m3u8.py
    if errorlevel 1 (
        echo Lỗi khi chạy convert_m3u8.py!
        pause
        exit /b
    ) else (
        echo Đã chạy convert_m3u8.py thành công!
    )
) else (
    echo Không tìm thấy file convert_m3u8.py trong D:\vieon!
    pause
    exit /b
)

echo Hoàn thành tất cả công việc!
pause