import re
import os


def extract_largest_image_urls(file_path):
    # 读取txt文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式查找所有img标签的内容
    img_tags = re.findall(r'<img[^>]+>', content)

    largest_image_urls = []

    # 遍历所有img标签
    for img_tag in img_tags:
        # 查找srcset属性中的所有.jpg链接
        srcset_match = re.search(r'srcset="([^"]+)"', img_tag)

        if srcset_match:
            # 获取srcset的内容并分割成多个URL
            srcset_content = srcset_match.group(1)
            image_urls = srcset_content.split(',')

            # 选择最大的图片URL
            largest_url = max(image_urls, key=lambda url: int(
                re.search(r'(\d+)x', url).group(1)))
            largest_image_urls.append(largest_url.split()[0].strip())
        else:
            # 如果没有srcset，则选择src属性中的URL
            src_match = re.search(r'src="([^"]+)"', img_tag)
            if src_match:
                largest_image_urls.append(src_match.group(1).strip())

    return largest_image_urls


if __name__ == '__main__':
    file_path = r'G:\Project\MyUtils\collected_content.txt'  # 您的txt文件路径
    largest_urls = extract_largest_image_urls(file_path)

    cwd = os.getcwd()
    save_filename = 'largest_image_urls.txt'
    save_file_path = os.path.join(cwd, save_filename)
    # 将提取的最大图片URL保存到文件或打印
    with open(save_file_path, 'w', encoding='utf-8') as output_file:
        for url in largest_urls:
            output_file.write(url + '\n')

    print("最大尺寸的图片URL已提取并保存到 largest_image_urls.txt 文件中。")
