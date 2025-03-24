import re

# Đường dẫn đầy đủ đến các file
channels_path = r"C:\xampp\htdocs\vieon\channels.txt"
logo_nhom_path = r"C:\xampp\htdocs\vieon\logo_nhom.txt"
output_path = r"C:\xampp\htdocs\vieon\channels_updated.txt"

print("Bắt đầu chạy chương trình...")

# Đọc file channels.txt chứa các link (dạng "vtv1hd: <link>")
try:
    with open(channels_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines() if line.strip() and ':' in line]
        links_dict = {line.split(':')[0].strip(): line.split(':', 1)[1].strip() for line in lines}
    print(f"Đã đọc được {len(links_dict)} link từ {channels_path}")
except FileNotFoundError:
    print(f"Không tìm thấy file: {channels_path}")
    exit()
except Exception as e:
    print(f"Lỗi khi đọc file {channels_path}: {e}")
    exit()

# Đọc file logo_nhom.txt chứa các dòng EXTINF
try:
    with open(logo_nhom_path, 'r', encoding='utf-8') as file:
        extinf_lines = [line.strip() for line in file.readlines() if line.strip() and line.startswith('#EXTINF')]
    print(f"Đã đọc được {len(extinf_lines)} dòng EXTINF từ {logo_nhom_path}")
except FileNotFoundError:
    print(f"Không tìm thấy file: {logo_nhom_path}")
    exit()
except Exception as e:
    print(f"Lỗi khi đọc file {logo_nhom_path}: {e}")
    exit()

# Tạo danh sách để lưu kết quả, bắt đầu với dòng tiêu đề M3U
output_lines = ['#EXTM3U url-tvg="http://lichphatsong.xyz/schedule/epg.xml"\n']
print("Đã thêm dòng tiêu đề vào đầu danh sách")

# Hàm trích xuất tvg-id hoặc tên kênh từ EXTINF
def extract_channel_name_from_extinf(extinf):
    # Trích xuất tvg-id từ EXTINF
    tvg_id_match = re.search(r'tvg-id="([^"]+)"', extinf)
    if tvg_id_match:
        return tvg_id_match.group(1).lower()  # Ưu tiên trả về tvg-id
    # Nếu không có tvg-id, fallback về tên kênh
    name = extinf.split(',')[-1].strip().lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

# So sánh và ghép các dòng giống nhau
for channel_name, link in links_dict.items():
    print(f"Đang xử lý kênh: {channel_name}")
    channel_name_clean = re.sub(r'[^a-z0-9]', '', channel_name.lower())
    found = False
    
    for extinf in extinf_lines:
        extinf_channel = extract_channel_name_from_extinf(extinf)
        
        # Kiểm tra 4 ký tự đầu tiên trước
        if channel_name_clean[:4] == extinf_channel[:4]:
            output_lines.append(extinf + '\n')
            output_lines.append(link + '\n')
            print(f"Khớp thành công với 4 ký tự: {channel_name_clean[:4]} với {extinf_channel[:4]}")
            found = True
            break
        # Nếu không khớp 4 ký tự, kiểm tra 5 ký tự
        elif channel_name_clean[:5] == extinf_channel[:5]:
            output_lines.append(extinf + '\n')
            output_lines.append(link + '\n')
            print(f"Khớp thành công với 5 ký tự: {channel_name_clean[:5]} với {extinf_channel[:5]}")
            found = True
            break
        # Nếu không khớp 5 ký tự, kiểm tra 6 ký tự
        elif channel_name_clean[:6] == extinf_channel[:6]:
            output_lines.append(extinf + '\n')
            output_lines.append(link + '\n')
            print(f"Khớp thành công với 6 ký tự: {channel_name_clean[:6]} với {extinf_channel[:6]}")
            found = True
            break
    
    if not found:
        print(f"Không tìm thấy EXTINF khớp với kênh: {channel_name}")

# Ghi đè lên file channels_updated.txt
try:
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)
    print(f"Đã xử lý xong {len(output_lines)//2} kênh và ghi đè lên file {output_path}")
except Exception as e:
    print(f"Lỗi khi ghi file {output_path}: {e}")