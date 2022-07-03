from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def pic_dl(img_url, picname):
    with open("pics_petunia23/" + picname + ".jpg", 'wb') as handle:
        response = requests.get(img_url, stream=True)
        if not response.ok:
            print(response)
            print("     Ошибка. Файл '" + picname + ".jpg' не сохранен")
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        if response.ok:
            print("     Файл '" + picname + ".jpg' сохранен")


def get_elems_array(flower_name, flower_num):
    driver.get("https://www.petunia23.ru/index.php?route=product/search&search=" + flower_name)
    imgs = driver.find_elements_by_xpath(
        '//*[@id="content"]/div[3]/div/div/div/a/img')
    names = driver.find_elements_by_xpath(
        '//*[@id="content"]/div[3]/div/div/div/div[1]/h4/a')
    # for i in range(len(imgs)):
    #     print(i, imgs[i].get_attribute('src')[0:-11] + '500x500.jpg')
    # for i in range(len(names)):
    #     print(i, names[i].text)
    # print()
    if len(imgs) > 1:
        print("[*] Сорт '" + flower_name + "' имеет больше одного совпадения")
        if len(imgs) == len(names):
            for i in range(len(imgs)):
                pic_dl(
                    imgs[i].get_attribute('src')[0:-11] + '500x500.jpg',
                    "[" + str(flower_num) + " " + str(i + 1) + "] " + names[
                        i].text + " (по запросу " + flower_name + ")"
                )
        elif len(imgs) != len(names):
            print('длина имен и картинок не совпадает')
            print(len(imgs), len(names))
            for i in range(len(names)):
                print(i, names[i].text)
            exit()
    elif len(imgs) != 0:
        if flower_name.lower() != names[0].text.lower():
            print("[*] Текст запроса не совпадает с названием. Запрос: '" + flower_name,
                  "' Название: '" + names[0].text)
            pic_dl(
                imgs[0].get_attribute('src')[0:-11] + '500x500.jpg',
                "[" + str(flower_num) + "] " + names[0].text + " (по запросу " + flower_name + ")"
            )
        else:
            print("[+] Сорт '" + flower_name + "' найден")
            pic_dl(
                imgs[0].get_attribute('src')[0:-11] + '500x500.jpg',
                "[" + str(flower_num) + "] " + names[0].text
            )
    elif len(imgs) == 0:
        print("[-] Сорт '" + flower_name + "' не найден")


def main():
    f = open('names.txt', 'r')
    breeds_amount = sum(1 for _ in f)
    f.seek(0)
    for i in range(breeds_amount):
        flower_name = f.readline()[0:-1]
        get_elems_array(flower_name, i + 1)
        time.sleep(1)
    f.close()


main()
