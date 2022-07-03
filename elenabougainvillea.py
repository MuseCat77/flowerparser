from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests, random, time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def pic_dl(img_url, picname):
    with open("pics_elenabougainvillea/" + picname + ".jpg", 'wb') as handle:
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
    driver.get("https://elenabougainvillea.ru/katalog?tfc_query[269739354]=" + flower_name + "&tfc_div=:::")
    imgs = driver.find_elements_by_class_name('js-product-img')
    names = driver.find_elements_by_class_name('js-store-prod-name')
    if len(imgs) > 1:
        print("[*] Сорт '" + flower_name.replace('+', ' ') + "' имеет больше одного совпадения")
        if len(imgs) == len(names)-1:
            for i in range(len(imgs)):
                pic_dl(
                    imgs[i].get_attribute("data-original"),
                    "[" + str(flower_num) + " " + str(i+1) + "] " + names[i].text + " (по запросу " + flower_name + ")"
                )
        elif len(imgs) != len(names):
            print('длина имен и картинок не совпадает')
            print(len(imgs), len(names))
            for i in range(len(names)):
                print(i, names[i].text)
            exit()
    elif len(imgs) != 0:
        if flower_name.lower().replace("+", " ") != names[0].text.lower():
            print("[*] Текст запроса не совпадает с названием. Запрос: '" + flower_name,
                  "' Название: '" + names[0].text)
            pic_dl(
                imgs[0].get_attribute("data-original"),
                "[" + str(flower_num) + "] " + names[0].text + " (по запросу " + flower_name + ")"
            )
        else:
            print("[+] Сорт '" + flower_name + "' найден")
            pic_dl(
                imgs[0].get_attribute("data-original"),
                "[" + str(flower_num) + "] " + names[0].text
            )
    elif len(imgs) == 0 :
        print("[-] Сорт '" + flower_name.replace('+', ' ') + "' не найден")


def main():
    f = open('names.txt', 'r')
    breeds_amount = sum(1 for line in f)
    f.seek(0)
    for i in range(breeds_amount):
        flower_name = f.readline()[0:-1].replace(' ', '+')
        get_elems_array(flower_name, i+1)
        time.sleep(1)
    f.close()


main()
