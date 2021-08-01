from flask import Flask, render_template
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)


@app.route("/", methods = ['GET'])
def get_dato():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    urls = ["https://webscraper.io/test-sites/e-commerce/scroll/computers/laptops", "https://webscraper.io/test-sites/e-commerce/scroll/computers/tablets", "https://webscraper.io/test-sites/e-commerce/scroll/phones/touch"]

    for url in urls:
        driver.get(url)
        print('url', url)
        time.sleep(2)
        screen_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            print('height',scroll_height)
            if scroll_height == screen_height:
                print('break while')
                break
            screen_height = scroll_height


            allObj = BeautifulSoup(driver.page_source, 'html.parser')
            dataProducts = allObj.findAll("div", {"class":"caption"})
            if(url=="https://webscraper.io/test-sites/e-commerce/scroll/computers/laptops"):

                datoL = list()
                for dataProduct in dataProducts:
                    datoL.append({
                        "nombre": dataProduct.find("a", {"class":"title"}).text,
                        "caracteristicas": dataProduct.find("p", {"class":"description"}).text,
                        "valor":dataProduct.find("h4", {"class":"price"}).text
                     })
                with open('laptops.json', 'w') as file:
                    json.dump(datoL, file, indent=4, sort_keys=True)


            if(url=="https://webscraper.io/test-sites/e-commerce/scroll/phones/touch"):
                datoP = list()
                for dataProduct in dataProducts:
                    datoP.append({
                        "nombre": dataProduct.find("a", {"class":"title"}).text,
                        "caracteristicas": dataProduct.find("p", {"class":"description"}).text,
                        "valor":dataProduct.find("h4", {"class":"price"}).text
                     })
                with open('phones.json', 'w') as file:
                    json.dump(datoP, file, indent=4, sort_keys=True)

            if(url=="https://webscraper.io/test-sites/e-commerce/scroll/computers/tablets"):

                datoT = list()
                for dataProduct in dataProducts:
                    datoT.append({
                        "nombre": dataProduct.find("a", {"class":"title"}).text,
                        "caracteristicas": dataProduct.find("p", {"class":"description"}).text,
                        "valor":dataProduct.find("h4", {"class":"price"}).text
                     })
                with open('tablets.json', 'w') as file:
                    json.dump(datoT, file, indent=4, sort_keys=True)


    return render_template('index.html', datoP=datoP, datoL=datoL, datoT=datoT)
