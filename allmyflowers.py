from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def url_chek(pic_url):
    if pic_url[-9:-7] == '0x':
        return pic_url[0:58] + pic_url[66:-10] + '.jpg'
    else:
        return pic_url[0:58] + pic_url[66:-4] + '.jpg'

def pic_dl(img_url, picname):
    with open("pics_allmyflowers/" + picname + ".jpg", 'wb') as handle:
        response = requests.get(img_url, stream=True)
        if not response.ok:
            print(response)
            print("     Ошибка. Файл '" + picname + ".jpg' не сохранен")
            print("     url: " + img_url)
        elif response.ok:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            print("     Файл '" + picname + ".jpg' сохранен")


def get_elems_array(flower_name, flower_num):
    driver.get(
        "https://allmyflowers.ru/component/virtuemart/results,1-50?virtuemart_category_id+=0&limitstart=0&option=com_virtuemart&view=category&keyword="
        + flower_name
    )
    imgs = driver.find_elements_by_xpath(
        '//*[@id="vm-products-category"]/div[2]/div/div/div/div/div/div/a/span[1]/img')
    names = driver.find_elements_by_xpath(
        '//*[@id="vm-products-category"]/div[2]/div/div/div/div/div[2]/h3/a')
    # for i in range(len(imgs)):
    #     print("+ " + imgs[i].get_attribute('src')[0:58] + imgs[i].get_attribute('src')[66:-10] + '.jpg')
    #     print(imgs[i].get_attribute('src')[-9:-7])
    #     print("+" + imgs[i].get_attribute('src')[0:58] + imgs[i].get_attribute('src')[66:-4] + '.jpg')
    # for i in range(len(names)):
    #     print(i, names[i].text)
    # print()

    if len(imgs) > 1:
        print("[*] Сорт '" + flower_name + "' имеет больше одного совпадения")
        if len(imgs) == len(names):
            for i in range(len(imgs)):
                pic_dl(
                    url_chek(imgs[i].get_attribute('src')),
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
                url_chek(imgs[0].get_attribute('src')),
                "[" + str(flower_num) + "] " + names[0].text + " (по запросу " + flower_name + ")"
            )
        else:
            print("[+] Сорт '" + flower_name + "' найден")
            pic_dl(
                url_chek(imgs[0].get_attribute('src')),
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
        time.sleep(0.5)
    f.close()


main()
