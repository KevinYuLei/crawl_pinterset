import os
from utils.create_next_exp_folder import create_next_exp_folder
from utils.fetch_dynamic_content import fetch_dynamic_content
from utils.extract_img_urls import extract_largest_image_urls
from utils.remove_duplicate_urls import remove_duplicate_urls
from utils.download_imgs_from_urls import download_images_from_urls


if __name__ == '__main__':
    # 需要爬取的pinterest网址
    pinterest_url = "https://www.pinterest.jp/search/pins/?q=playing%20smart%20phone%20realistic&rs=typed"

    cwd = os.getcwd()
    imgs_folder = os.path.join(cwd, 'downloaded_imgs')
    runs_folder = os.path.join(cwd, 'runs')
    
    # imgs_exp_folder 用于保存每次运行时爬取url所下载的图片
    imgs_exp_folder = create_next_exp_folder(imgs_folder)
    # runs_exp_folder 用于保存每次运行时所爬取的html_content文件与largest_image_urls文件
    runs_exp_folder = create_next_exp_folder(runs_folder)
    
    # 调用函数，获取页面滚动过程中收集的所有HTML内容
    html_content_list = fetch_dynamic_content(pinterest_url)
    
    html_content_filename = 'html_content.txt'
    html_content_path = os.path.join(runs_folder, html_content_filename)
    
    # 将收集的HTML内容保存到txt文件中
    with open(html_content_path, 'w', encoding='utf-8') as file:
        for i, content in enumerate(html_content_list):
            file.write(content)
            file.write('\n\n')  # 添加空行以区分不同的内容块
            print(f"已写入{i}次网页内容！")
    
    # 调用函数解析txt文件，获取各图像最大清晰度版本的url
    largest_urls = extract_largest_image_urls(html_content_path)
    
    imgs_url_filename = 'largest_image_urls.txt'
    imgs_url_path = os.path.join(runs_exp_folder, imgs_url_filename)
    # 将提取的最大图片URL保存到文件或打印
    with open(imgs_url_path, 'w', encoding='utf-8') as output_file:
        for url in largest_urls:
            output_file.write(url + '\n')
    print("最大尺寸的图片URL已提取并保存到 largest_image_urls.txt 文件中。")
    
    # 调用函数去除重复的URL
    remove_duplicate_urls(imgs_url_path)
    
    # 调用函数下载图片
    download_images_from_urls(imgs_url_path, imgs_exp_folder)