import os
import requests

def download_images_from_urls(file_path, save_directory):
    # 创建保存图片的目录（如果不存在）
    os.makedirs(save_directory, exist_ok=True)

    # 读取URL文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # 遍历每个URL并下载图片
    for index, url in enumerate(urls):
        url = url.strip()  # 去掉多余的空格和换行符
        if url:  # 确保URL不为空
            try:
                # 发送GET请求获取图片
                response = requests.get(url, stream=True)
                response.raise_for_status()  # 检查请求是否成功

                # 根据索引命名文件
                file_name = f"image_{(index + 1):05d}.jpg"  # 文件名格式
                file_path = os.path.join(save_directory, file_name)

                # 保存图片
                with open(file_path, 'wb') as image_file:
                    for chunk in response.iter_content(1024):
                        image_file.write(chunk)

                print(f"Downloaded: {file_name}")

            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")

if __name__ == '__main__':
    # URL文件路径
    url_file_path = r'G:\Project\MyUtils\largest_image_urls.txt'  # 读取的URL文件
    # 图片保存目录
    save_path = r'G:\Project\MyUtils\downloaded_imgs'  # 保存图片的路径

    # 调用函数下载图片
    download_images_from_urls(url_file_path, save_path)
