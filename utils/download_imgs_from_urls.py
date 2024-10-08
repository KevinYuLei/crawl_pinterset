import os
import requests


# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'DNT': '1',
}

# 代理配置（根据需要替换为实际代理地址和端口）
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}


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
                response = requests.get(
                    url, stream=True, headers=headers, proxies=proxies)
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
