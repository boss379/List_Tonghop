import requests
import re
import os

# Lấy thông tin đăng nhập từ GitHub Secrets
VIEON_USERNAME = os.getenv("VIEON_USERNAME")
VIEON_PASSWORD = os.getenv("VIEON_PASSWORD")

if not VIEON_USERNAME or not VIEON_PASSWORD:
    print("❌ Lỗi: Chưa có thông tin đăng nhập VieON. Hãy thêm vào GitHub Secrets!")
    exit(1)

# Login để lấy access token
login_url = "https://api.vieon.vn/backend/user/v2/login?platform=web&ui=012021"
login_data = {
    "username": VIEON_USERNAME,
    "password": VIEON_PASSWORD,
    "country_code": "VN",
    "model": "Windows 10",
    "device_id": "83178e7b4ef31f27e0e43ff8c3ec822a",
    "device_name": "Chrome/122",
    "device_type": "desktop",
    "platform": "web",
    "ui": "012021"
}

login_headers = {
    'Content-Type': 'application/json; charset=UTF-8'
}

try:
    login_response = requests.post(login_url, json=login_data, headers=login_headers)
    login_response.raise_for_status()
    
    # Lấy access token
    token_match = re.search(r'"access_token":"(.*?)"', login_response.text)
    if not token_match:
        print("❌ Lỗi: Không lấy được access token!")
        exit(1)

    access_token = token_match.group(1)

    # Danh sách kênh
    channels = [
        "vtv1-hd", "vtv2-hd", "vtv3-hd", "vtv4-hd", "vtv5-hd",
        "vtv5-tay-nguyen", "vtv5-tay-nam-bo", "vtv-can-tho",
        "vtv7-hd", "vtv8-hd", "vtv9-hd", "an-ninh-hd",
        "quoc-phong-hd", "ha-noi-1", "ha-noi-2-2021",
        "htv-the-thao", "kbs-world", "nhk-world",
        "htvc-du-lich-cuoc-song", "vie-channel-htv2-hd",
        "htv-key", "thvl1-hd", "thvl2-hd", "thvl3-hd", "thvl4-hd", "htv7-hd", "htv1", "htv3", "htv9-hd", "htv-the-thao", "htvc-plus", 
        "htvc-ca-nhac", "htvc-phim", "htvc-gia-dinh", "dw-hd", "france-24-english-hd", "htvc-phu-nu", "htvc-thuan-viet-hd", "bac-giang-hd", 
        "bac-ninh-1", "bac-kan-1", "da-nang-1", "da-nang-2", "dong-nai-1", "dong-nai-2", "dong-nai-3", "channel-news-asia-hd"
    ]

    api_url = 'https://api.vieon.vn/backend/cm/v5/slug/livetv/detail?platform=web&ui=012021'
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://vieon.vn/truyen-hinh-truc-tuyen'
    }

    txt_content = ""
    success_count = 0

    # Lấy link từng kênh
    for channel in channels:
        post_data = f"livetv_slug=/truyen-hinh-truc-tuyen/{channel}/&platform=web&ui=012021"
        try:
            response = requests.post(api_url, headers=headers, data=post_data, timeout=10)
            response.raise_for_status()
            
            # Tìm link HLS
            match = re.search(r'hls_link_play":"(.*?)"', response.text)
            if match:
                channel_name = channel.replace('-hd', '').upper()
                hls_link = match.group(1)
                txt_content += f"{channel_name}: {hls_link}\n"
                success_count += 1
        except requests.RequestException as e:
            print(f"⚠️ Không lấy được link {channel}: {e}")

    # Lưu vào file trong repo
    txt_file = "channels.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(txt_content)

    print(f"✅ Đã lấy thành công {success_count}/{len(channels)} kênh!")
    print(f"📁 File đã được lưu: {txt_file}")

except requests.RequestException as e:
    print(f"❌ Lỗi đăng nhập: {e}")
