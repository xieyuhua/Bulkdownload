import requests
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 指定文本文件的路径
txt_file_path = 'images.txt'
# 指定下载图片的保存目录
save_directory = 'downloaded_images'

# 确保保存目录存在
os.makedirs(save_directory, exist_ok=True)

# 读取文本文件
with open(txt_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 提取图片名字和URL的列表
image_urls = [(line.strip().split()[0], line.strip().split()[1]) for line in lines if len(line.strip().split()) == 2]

def download_image(image_info):
    image_name, image_url = image_info
    
    # 尝试从URL中提取文件后缀
    parsed_url = urlparse(image_url)
    path = parsed_url.path
    _, file_extension = os.path.splitext(path)
    
    # 如果没有提取到后缀，则默认使用.jpg
    if not file_extension:
        file_extension = '.jpg'
    else:
        file_extension = file_extension.lower()  # 转换为小写
    
    # 构造完整的保存路径和文件名
    save_path = os.path.join(save_directory, f"{image_name}{file_extension}")
    
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # 如果请求出错，抛出HTTPError异常
        
        # 以二进制模式打开文件准备写入
        with open(save_path, 'wb') as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤掉空的chunk
                    image_file.write(chunk)
        
        # print(f'Successfully downloaded {image_name} as {save_path}')
    except requests.RequestException as e:
        print(f'Failed to download {image_name} from {image_url}: {e}')
    except Exception as e:
        print(f'An error occurred while saving {image_name} to {save_path}: {e}')

# 使用ThreadPoolExecutor来管理线程池
with ThreadPoolExecutor(max_workers=10) as executor:  # 可以根据需要调整max_workers的数量
    future_to_image = {executor.submit(download_image, image_info): image_info for image_info in image_urls}
    
    for future in as_completed(future_to_image):
        image_info = future_to_image[future]
        try:
            future.result()  # 这将阻塞直到线程完成，除非抛出了异常
        except Exception as exc:
            print(f'{image_info[0]} generated an exception: {exc}')
