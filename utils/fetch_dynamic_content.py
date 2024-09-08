from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def fetch_dynamic_content():
    # 设置Chrome浏览器的选项，确保浏览器不会显示自动化工具控制的提示信息
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')  # 禁用GPU加速（可选）
    options.add_argument('--start-maximized')  # 启动时最大化窗口

    # 启动Chrome浏览器，使用上述配置
    driver = webdriver.Chrome(options=options)

    # 通过Chrome DevTools Protocol (CDP) 禁用webdriver特征检测，使浏览器看起来像是由人操作的
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    # 访问Pinterest的登录页面
    driver.get("https://www.pinterest.com/login/")

    # 等待30秒以手动完成登录过程（或调整为自动化登录）
    time.sleep(30)

    # 登录完成后，访问目标Pinterest页面
    driver.get(
        "https://www.pinterest.jp/search/pins/?q=playing%20smart%20phone%20realistic&rs=typed")

    # 定位Pinterest页面中用于展示图片的动态元素的CSS选择器
    element_selector = "div.vbI.XiG"

    # 等待页面的初始加载，直到目标元素出现在页面中
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
    )

    # 初始化一个列表，用于保存每次获取的动态HTML内容
    collected_html_content = []
    scroll_count = 1

    # 获取页面视窗高度
    windows_height = driver.execute_script("return window.innerHeight")
    # 设置页面滚动的距离倍数
    scroll_ratio = 1.0
    # 滚动页面高度的倍数距离，避免跳过内容
    scroll_distance = windows_height * scroll_ratio

    # 通过模拟滚动操作，逐步加载页面内容，直到内容加载完毕
    while True:
        # 等待3秒，确保新内容加载完毕
        time.sleep(3)

        # 获取当前页面中目标元素的动态HTML内容
        dynamic_elements = driver.find_elements(
            By.CSS_SELECTOR, element_selector)
        dynamic_html_content = "\n".join(
            [element.get_attribute('innerHTML') for element in dynamic_elements])

        # 保存获取到的HTML内容到列表中
        collected_html_content.append(dynamic_html_content)

        # 获取当前滚动后的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")
        current_position = driver.execute_script(
            "return window.pageYOffset + window.innerHeight")

        # 如果当前页面高度等于document.body.scrollHeight，说明到达页面底部，退出循环
        if abs(new_height - current_position) < 10:  # 允许10像素的误差范围
            break

        print(f"已获取{scroll_count}次网页内容！")
        scroll_count += 1
        # 滚动视窗
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

    # 关闭浏览器，释放资源
    driver.quit()
    print(f"网页内容获取完毕，关闭浏览器!")

    # 返回收集的所有动态HTML内容
    return collected_html_content


if __name__ == '__main__':
    # 调用函数，获取页面滚动过程中收集的所有HTML内容
    content_list = fetch_dynamic_content()

    cwd = os.getcwd()
    file_name = 'collected_content.txt'
    file_path = os.path.join(cwd, file_name)
    print(file_path)

    # 将收集的HTML内容保存到txt文件中
    with open(file_path, 'w', encoding='utf-8') as file:
        for i, content in enumerate(content_list):
            file.write(content)
            file.write('\n\n')  # 添加空行以区分不同的内容块
            print(f"已写入{i}次网页内容！")

    print("HTML内容已保存到 collected_content.txt 文件中。")
