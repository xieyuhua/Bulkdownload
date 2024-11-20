import os
import json
import re

def parse_filename(filename):
    # 使用正则表达式匹配文件名中的名字和版本号
    match = re.match(r'(?P<name>[^_]+)_(?P<version>[\d.]+)\.', filename)
    if match:
        return match.groupdict()
    else:
        # 如果不匹配，返回 None
        return None

def generate_json_from_directory(directory_path, output_json_path, path_json):
    file_data_list = []
    data_list = []
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory_path):
        # 构建文件的完整路径
        full_path = os.path.join(directory_path, filename)
        # 检查是否为文件（而不是目录）
        if os.path.isfile(full_path):
             # 构建文件的完整路径
            if path_json != "" :
                full_path = path_json+filename
            print(f'Failed {full_path}')

            # 解析文件名
            file_info = parse_filename(filename)
            if file_info:
                # 创建一个包含所需信息的字典
                file_data = {
                    'name': file_info['name'],
                    'version': file_info['version'],
                    'url': full_path
                }
                # 添加到列表中
                file_data_list.append(file_data)
    
                data_list = {
                    'plugins':file_data_list
                }

    # 将列表写入 JSON 文件
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)



# 指定要扫描的目录（当前目录下的 'json' 文件夹）
directory_to_scan = os.path.join(os.getcwd(), 'json')
# 指定输出的 JSON 文件路径
output_json = os.path.join(os.getcwd(), 'output.json')
# 指定输出的 JSON 文件路径
path_json = "https://gitee.com/maotoumao/"
# 生成 JSON 文件
generate_json_from_directory(directory_to_scan, output_json, path_json)