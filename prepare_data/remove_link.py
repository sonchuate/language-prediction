import re

def remove_links_from_file(input_file, output_file):
    # Đọc nội dung từ file đầu vào
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Sử dụng regex để tìm và loại bỏ các liên kết
    # Regex này sẽ tìm các chuỗi bắt đầu bằng 'http://' hoặc 'https://' và kết thúc bằng dấu cách hoặc hết dòng
    cleaned_content = re.sub(r'http[s]?://\S+', '', content)

    # Ghi nội dung đã được làm sạch vào file đầu ra
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

# Đường dẫn tới file văn bản của bạn
input_file_path = 'english_raw.txt'
output_file_path = 'english_raw_remove_link.txt'

# Gọi hàm để xoá liên kết
remove_links_from_file(input_file_path, output_file_path)

print(f"Đã xoá các liên kết và lưu kết quả vào {output_file_path}")
