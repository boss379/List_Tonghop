@echo off
chcp 65001 >nul

:: Chuyển đến thư mục D:\vieon
cd /d D:\vieon
if %ERRORLEVEL% neq 0 (
    echo Không thể chuyển đến D:\vieon. Kiểm tra thư mục có tồn tại không!
    pause
    exit /b
)

:: Chạy file Python get_channels.py
echo Đang chạy get_channels.py...
if exist get_channels.py (
    python get_channels.py
    if %ERRORLEVEL% neq 0 (
        echo Lỗi khi chạy get_channels.py!
        pause
        exit /b
    ) else (
        echo Đã chạy get_channels.py thành công!
    )
) else (
    echo Không tìm thấy file get_channels.py trong D:\vieon!
    pause
    exit /b
)

:: Chạy file Python convert_m3u8.py
echo Đang chạy convert_m3u8.py...
if exist convert_m3u8.py (
    python convert_m3u8.py
    if %ERRORLEVEL% neq 0 (
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

:: Đẩy file channels_updated.txt lên GitHub
echo Đang đẩy file channels_updated.txt lên GitHub...
if exist channels_updated.txt (
    git add channels_updated.txt
    git commit -m "Cập nhật file channels_updated.txt"
    git push
    if %ERRORLEVEL% neq 0 (
        echo Lỗi khi đẩy file lên GitHub!
        pause
        exit /b
    ) else (
        echo Đã đẩy file lên GitHub thành công!
    )
) else (
    echo Không tìm thấy file channels_updated.txt!
    pause
    exit /b
)

echo Đã hoàn thành!
pause
