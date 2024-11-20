from bs4 import BeautifulSoup

# 假设你有一个HTML文件的路径
html_file_path = 'data.txt'
# 你想要保存图片地址的TXT文件路径
output_txt_path = 'image_urls.txt'

# 读取HTML文件内容
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 提取所有的<img>标签，并获取它们的src属性
image_urls = []
for img_tag in soup.find_all('img', src=True):
    image_urls.append(img_tag['src'])

# 将图片地址写入到TXT文件中
with open(output_txt_path, 'w', encoding='utf-8') as file:
    for image_url in image_urls:
        file.write(image_url + '\n')

print(f'Successfully extracted {len(image_urls)} image URLs and saved them to {output_txt_path}')