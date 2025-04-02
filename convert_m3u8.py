import re
import os

base_dir = r"D:\vieon"
channels_path = os.path.join(base_dir, "channels.txt")
logo_nhom_path = os.path.join(base_dir, "logo_nhom.txt")
output_path = os.path.join(base_dir, "channels_updated.txt")

print("Bắt đầu chạy chương trình...")

# Đọc dữ liệu từ files
try:
    with open(channels_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines() if line.strip() and ':' in line]
        links_dict = {line.split(':')[0].strip(): line.split(':', 1)[1].strip() for line in lines}
    print(f"Đã đọc được {len(links_dict)} link từ {channels_path}")
except FileNotFoundError:
    print(f"Không tìm thấy file: {channels_path}")
    exit(1)
except Exception as e:
    print(f"Lỗi khi đọc file {channels_path}: {e}")
    exit(1)

try:
    with open(logo_nhom_path, 'r', encoding='utf-8') as file:
        extinf_lines = [line.strip() for line in file.readlines() if line.strip() and line.startswith('#EXTINF')]
    print(f"Đã đọc được {len(extinf_lines)} dòng EXTINF từ {logo_nhom_path}")
except FileNotFoundError:
    print(f"Không tìm thấy file: {logo_nhom_path}")
    exit(1)
except Exception as e:
    print(f"Lỗi khi đọc file {logo_nhom_path}: {e}")
    exit(1)

output_lines = ['#EXTM3U url-tvg="http://lichphatsong.xyz/schedule/epg.xml"\n']

def extract_channel_name_from_extinf(extinf):
    tvg_id_match = re.search(r'tvg-id="([^"]+)"', extinf)
    if tvg_id_match:
        return tvg_id_match.group(1).lower()
    name = extinf.split(',')[-1].strip().lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

# Tạo dict chứa tên kênh đã chuẩn hóa và EXTINF tương ứng
extinf_dict = {}
for extinf in extinf_lines:
    clean_name = extract_channel_name_from_extinf(extinf)
    extinf_dict[clean_name] = extinf

for channel_name, link in links_dict.items():
    print(f"Đang xử lý kênh: {channel_name}")
    channel_name_clean = re.sub(r'[^a-z0-9]', '', channel_name.lower())
    found = False
    
    # Ưu tiên 1: Khớp chính xác hoàn toàn
    if channel_name_clean in extinf_dict:
        output_lines.append(extinf_dict[channel_name_clean] + '\n')
        output_lines.append(link + '\n')
        print(f"Khớp chính xác: {channel_name_clean}")
        continue
    
    # Ưu tiên 2: Khớp từng phần (4-8 ký tự)
    if len(channel_name_clean) >= 4:
        best_match = None
        best_length = 0
        
        for extinf_name, extinf in extinf_dict.items():
            # Tìm độ dài khớp tối đa
            match_length = 0
            for i in range(min(8, len(channel_name_clean), len(extinf_name))):
                if channel_name_clean[i] == extinf_name[i]:
                    match_length += 1
                else:
                    break
            
            # Chỉ chấp nhận nếu khớp từ 4 ký tự trở lên
            if match_length >= 4 and match_length > best_length:
                best_length = match_length
                best_match = extinf
        
        if best_match:
            output_lines.append(best_match + '\n')
            output_lines.append(link + '\n')
            print(f"Khớp từng phần ({best_length} ký tự đầu): {channel_name_clean[:best_length]}")
            continue
    
    print(f"Không tìm thấy EXTINF khớp với kênh: {channel_name}")

try:
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)
    print(f"Đã xử lý xong {len(output_lines)//2} kênh và ghi đè lên file {output_path}")
except Exception as e:
    print(f"Lỗi khi ghi file {output_path}: {e}")
    exit(1)