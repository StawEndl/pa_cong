from bs4 import BeautifulSoup
import requests
import time
import os


def get_photo(key):
    num = 0
    url = "https://desk.zol.com.cn/fengjing/" + str(key) + ".html"
    resp = requests.get(url)
    resp.encoding = "gb2312"
    main_page = BeautifulSoup(resp.text, "html.parser")
    ul = main_page.find("ul", class_="pic-list2")
    a = ul.find_all("a", class_="pic")

    for i in a:
        #https://file.cdn.cqttech.com/xzdesktop/XZDesktop_4020_2.0.11.12.exe
        if str(i.get('href').strip("/")).find("https://file.cdn.cqttech.com/") != -1:
            continue
        url_detail = "https://desk.zol.com.cn/" + str(i.get('href').strip("/"))

        # headers = UserAgent.get_headers()
        child_resp = requests.get(url_detail, "html.parser")

        child_page = BeautifulSoup(child_resp.text, "html.parser")

        child_a_all = child_page.find("ul", id="showImg").find_all("a")
        # print(child_a_all)
        for child_a_all_part in child_a_all:
            # print("https://desk.zol.com.cn" + child_a_all_part.get('href'))
            child_a_all_part_respone = requests.get("https://desk.zol.com.cn" + child_a_all_part.get('href'), "html.parser")
            # child_resp = requests.get(url_detail, "html.parser")

            child_page_part = BeautifulSoup(child_a_all_part_respone.text, "html.parser")
            # print(child_a_all_part_respone)

            child_dd = child_page_part.find("dd", id="tagfbl")

            child_a = child_dd.find_all("a", class_="")

            # for i in child_a:
            #     child_url = "https://desk.zol.com.cn" + str(i.get('href'))
            #     child_name = child_url.strip('https://desk.zol.com.cn/showpic/') + str('.jpg')
            #     child_html = requests.get(child_url)
            #     child_img = BeautifulSoup(child_html.text, "html.parser").find("img").get('src')
            #     child_requests = requests.get(child_img)
            #     if (num == 0):
            #         if not os.path.exists('爬取高清图片'):
            #             os.mkdir('爬取高清图片')
            #         with open("D:/paCong/background_new/fengjing/" + child_name, mode="wb") as f:
            #             f.write(child_requests.content)
            #         print("sucessful!!!" + child_name)
            #     num += 1
            #     time.sleep(1)
            # print(child_a)
            for child_a_part in child_a:
                if child_a_part.get('href').find("1920x1080") == -1:
                    continue
                i = child_a_part
                child_url = "https://desk.zol.com.cn" + str(i.get('href'))
                child_name = child_url.strip('https://desk.zol.com.cn/showpic/') + str('.jpg')
                child_html = requests.get(child_url)
                child_img = BeautifulSoup(child_html.text, "html.parser").find("img").get('src')
                child_requests = requests.get(child_img)
                # if (num == 0):
                #     if not os.path.exists('爬取高清图片'):
                #         os.mkdir('爬取高清图片')

                with open("D:/paCong/background_new/fengjing/" + str(key) + "-" + str(num) + "-" + child_name, mode="wb") as f:
                    f.write(child_requests.content)
                print("sucessful!!!" + child_name)
                num = num + 1
                time.sleep(1)


def start():
    for i in range(81):
        get_photo(i + 1)

if __name__ == "__main__":
    start()