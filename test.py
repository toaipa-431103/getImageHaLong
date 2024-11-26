import os
import requests

# Tạo thư mục lưu ảnh, dang chay do thi sua dong 34 den trang do
os.makedirs("downloaded_images", exist_ok=True)

# Cấu hình API
base_url = "https://api.timanh.vn/api/web/GetPhotosByEventCode"
params = {
    "eventCode": "hbhm2024",
    "query": "",
    "currentPage": 1,  # Bắt đầu từ trang đầu tiên
    "pageSize": 60  # Số ảnh mỗi trang
}

total_pages = 2499  # Số trang tổng cộng (lấy từ phản hồi API)


def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=5)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Đã tải: {save_path}")
        else:
            print(f"Lỗi khi tải ảnh: {url}")
    except Exception as e:
        print(f"Lỗi: {e}")


# Duyệt qua các trang API
for page in range(1, total_pages + 1):
    params["currentPage"] = page
    print(f"Đang xử lý trang {page}/{total_pages}...")

    # Gửi yêu cầu đến API
    response = requests.get(base_url, params=params, timeout=5)
    if response.status_code == 200:
        data = response.json()
        photo_items = data.get("photoItems", [])

        # Tải xuống từng ảnh
        for item in photo_items:
            image_url = item["publicUrl"]
            image_id = item["id"]
            image_key = item["finalKey"]
            image_key_final = image_key.replace("halong-international-heritage-marathon-2024-241113/", "").replace("/","-")
            save_path = os.path.join("downloaded_images_final", f"{image_key_final}")
            download_image(image_url, save_path)
    else:
        print(f"Lỗi API tại trang {page}: {response.status_code}")
        break
