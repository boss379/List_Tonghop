<?php
$ip = $_SERVER['REMOTE_ADDR'];
$ip_check = ["222.252.125.20", "127.0.0.1", "::1"];
if (in_array($ip, $ip_check)) {
    // Lấy access token
    $url = "https://api.vieon.vn/backend/user/v2/login?platform=web&ui=012021";
    $data = '{"username": "0359197328","password": "Trung@1987","country_code": "VN","model": "Windows 10","device_id": "83178e7b4ef31f27e0e43ff8c3ec822a","device_name": "Chrome/122","device_type": "desktop","platform": "web","ui": "012021"}';
    $mr = curl_init();
    curl_setopt_array($mr, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => $url,
        CURLOPT_ENCODING => "",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_CUSTOMREQUEST => "POST",
        CURLOPT_POSTFIELDS => $data,
        CURLOPT_HTTPHEADER => array(
            'Content-Type: application/json; charset=UTF-8',
        ),
    ));
    $mr2 = curl_exec($mr);
    curl_close($mr);
    preg_match('/"access_token":"(.*?)"/', $mr2, $matches);
    $kq = $matches[1];

    // Danh sách các slug kênh
    $channels = [
        "vtv1-hd",
        "vtv2-hd",
        "vtv3-hd",
        "vtv4-hd",
        "vtv5-hd",
        "vtv5-tay-nguyen",
        "vtv5-tay-nam-bo",
        "vtv-can-tho",
        "vtv7-hd",
        "vtv8-hd",
        "vtv9-hd",
        "an-ninh-hd",
        "quoc-phong-hd",
        "channel-news-asia-hd"
    ];

    $url = 'https://api.vieon.vn/backend/cm/v5/slug/livetv/detail?platform=web&ui=012021';
    $headers = [
        'Host: api.vieon.vn',
        'Authorization: ' . $kq,
        'Content-Type: application/x-www-form-urlencoded',
        'Referer: https://vieon.vn/truyen-hinh-truc-tuyen'
    ];

    // Khởi tạo nội dung cho các file
    $m3u_content = "#EXTM3U\n";
    $txt_content = "";
    $channel_links = [];
    $success_count = 0;
    $total_channels = count($channels);

    // Lặp qua từng kênh để lấy link
    foreach ($channels as $channel) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POSTFIELDS, "livetv_slug=/truyen-hinh-truc-tuyen/{$channel}/&platform=web&ui=012021");

        $response = curl_exec($ch);
        curl_close($ch);

        // Lấy link HLS từ response
        if (preg_match('/hls_link_play":"(.*?)"/', $response, $match) && isset($match[1])) {
            $channel_name = strtoupper(str_replace('-hd', '', $channel));
            $hls_link = $match[1];
            $m3u_content .= "#EXTINF:-1,{$channel_name}\n{$hls_link}\n";
            $txt_content .= "{$channel_name}: {$hls_link}\n";
            $channel_links[$channel_name] = $hls_link;
            $success_count++;
        }
    }

    // Xác định trạng thái get link
    $get_link_status = ($success_count > 0) ? 
        "<p><i class='fas fa-check-circle'></i> Get link thành công: {$success_count}/{$total_channels} kênh</p>" : 
        "<p><i class='fas fa-times-circle'></i> Get link thất bại: Không lấy được link nào</p>";

    // Kiểm tra và ghi đè file M3U
    $m3u_file = 'vtv_playlist.m3u';
    $m3u_status = file_exists($m3u_file) ? "Ghi đè file M3U cũ" : "Tạo mới file M3U";
    file_put_contents($m3u_file, $m3u_content);

    // Kiểm tra và ghi đè file TXT
    $txt_file = 'vtv_links.txt';
    $txt_status = file_exists($txt_file) ? "Ghi đè file TXT cũ" : "Tạo mới file TXT";
    file_put_contents($txt_file, $txt_content);

    // Tạo và ghi đè file HTML
    $html_file = 'vtv_live.html';
    $html_status = file_exists($html_file) ? "Ghi đè file HTML cũ" : "Tạo mới file HTML";
    $html_content = "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>VTV Live Stream</title>
    <script src='https://cdn.jsdelivr.net/npm/hls.js@latest'></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .channel-list { margin-bottom: 20px; }
        video { width: 100%; max-width: 800px; height: auto; }
    </style>
</head>
<body>
    <h1>VTV Live Stream</h1>
    <div class='channel-list'>
        <label for='channel-select'>Chọn kênh:</label>
        <select id='channel-select' onchange='playChannel()'>
";

    foreach ($channel_links as $name => $link) {
        $html_content .= "            <option value='{$link}'>{$name}</option>\n";
    }

    $html_content .= "        </select>
    </div>
    <video id='video' controls autoplay></video>
    <script>
        const video = document.getElementById('video');
        const channelSelect = document.getElementById('channel-select');

        function playChannel() {
            const hlsUrl = channelSelect.value;
            if (Hls.isSupported()) {
                const hls = new Hls();
                hls.loadSource(hlsUrl);
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = hlsUrl;
                video.play();
            }
        }

        playChannel();
    </script>
</body>
</html>";
    file_put_contents($html_file, $html_content);

    // Trả về giao diện với thông báo get link
    header('Content-Type: text/html');
    echo "<!DOCTYPE html>
<html lang='vi'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Kết quả xử lý</title>
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f4f4f9;
        }
        h2 {
            color: #2c3e50;
            text-align: center;
        }
        .status-box {
            background-color: #fff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .status-box p {
            margin: 5px 0;
            color: #34495e;
        }
        .status-box p i {
            margin-right: 8px;
        }
        .status-box p i.fa-check-circle {
            color: #27ae60;
        }
        .status-box p i.fa-times-circle {
            color: #e74c3c;
        }
        .status-box p i.fa-file-alt {
            color: #3498db;
        }
        .links {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .links a {
            display: inline-block;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .links a:hover {
            background-color: #2980b9;
        }
        .links a i {
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <h2>🔥 Kết quả xử lý file</h2>
    <div class='status-box'>
        {$get_link_status}
        <p><i class='fas fa-file-alt'></i> {$m3u_status}</p>
        <p><i class='fas fa-file-alt'></i> {$txt_status}</p>
        <p><i class='fas fa-file-alt'></i> {$html_status}</p>
    </div>
    <div class='links'>
        <a href='{$m3u_file}' download><i class='fas fa-download'></i> Tải file M3U</a>
        <a href='{$txt_file}' download><i class='fas fa-download'></i> Tải file TXT</a>
        <a href='{$html_file}' target='_blank'><i class='fas fa-tv'></i> Xem trực tiếp trên web</a>
    </div>
</body>
</html>";
    exit();
} else {
    echo "403 Forbidden!";
}
?>