#完成：2023-3.3 调试运行通过
import os
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


def timeit(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f'time consuming: {(end-start):.4f} seconds. ({func})')

    return wrapper

def download_pic(img_url):
    r = requests.get(img_url, stream=True)
    image_name = img_url.split('/')[-1]
    print(image_name)
    cur_dir = os.path.abspath(os.curdir)
    print(cur_dir)
    img_dir = os.path.join(cur_dir, 'img\\')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        print(img_dir)
        print("File or directory has been created.")
    else:
        print("File or directory already exists.")


    imgfile = img_dir + image_name
    print(imgfile)
    # 下列方式适合较大文件下载
    with open(imgfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
    print(f'{image_name} is saved.')



@timeit
def main():
    url_base = 'https://jandan.net/ooxx'
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 30)
    browser.get(url_base)

    ls = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'previous-comment-page')))
    page_url = url_base


    while page_url is not None:
        browser.get(page_url)
        print("xxm"+ page_url)

        try:
            imglist = browser.find_elements(by=By.PARTIAL_LINK_TEXT, value='[查看原图]')
            img_urls = []
            for idx, ele in enumerate(imglist):
                img_url = ele.get_attribute("href")
                img_urls.append(img_url)
                print(f'ls_{idx}: {ele.get_attribute("href")}')  # ele.text: [查看原图]
                download_pic(img_url)

            page_url = browser.find_element(By.CLASS_NAME,'previous-comment-page').get_attribute("href")
            print("next page: "+ page_url)

        except  StaleElementReferenceException:
            print("xxm")
            time.sleep(10)


        time.sleep(5)

    browser.get_screenshot_as_file("capture.png")
    browser.close()


if __name__ =="__main__":
    main()