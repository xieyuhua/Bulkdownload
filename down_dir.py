import os
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 指定文本文件的路径
txt_file_path = 'image_urls.txt'
# 指定下载图片的根保存目录
root_save_directory = 'downloaded_images'

# 确保根保存目录存在
os.makedirs(root_save_directory, exist_ok=True)

# 读取文本文件
with open(txt_file_path, 'r', encoding='utf-8') as file:
    image_urls = [line.strip() for line in file.readlines()]

def parse_url_for_directory(url):
    """
    根据URL解析出目录层级。
    这里假设URL的某个部分（如路径）可以用来构建目录结构。
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    # 去除开头的斜杠并分割路径为层级
    directories = [d for d in path.strip('/').split('/') if d]
    return directories

def create_directories(base_dir, directories):
    """
    根据给定的基目录和目录层级创建目录。
    """
    full_path = base_dir
    for directory in directories:
        full_path = os.path.join(full_path, directory)
        os.makedirs(full_path, exist_ok=True)
    return full_path

def download_image(url):
    """
    下载图片并保存到相应的目录中。
    """
    # 解析URL以获取目录层级
    directories = parse_url_for_directory(url)
    
    # 从URL中提取文件名（不带扩展名）和扩展名
    parsed_url = urlparse(url)
    filename_with_ext = os.path.basename(parsed_url.path)
    filename, ext = os.path.splitext(filename_with_ext)
    
    # 构建完整的保存路径
    save_path = create_directories(root_save_directory, directories)
    save_file_path = os.path.join(save_path, f"{filename}{ext}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果请求出错，抛出HTTPError异常
        
        with open(save_file_path, 'wb') as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤掉空的chunk
                    image_file.write(chunk)
        
        # print(f'Successfully downloaded {url} to {save_file_path}')
    except requests.RequestException as e:
        print(f'Failed to download {url}: {e}')

# 使用ThreadPoolExecutor来管理线程池
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(download_image, url): url for url in image_urls}
    
    for future in as_completed(futures):
        url = futures[future]
        try:
            future.result()  # 这将阻塞直到线程完成，除非抛出了异常
        except Exception as exc:
            print(f'Failed to download {url}: {exc}')