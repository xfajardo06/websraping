from flask import Flask, render_template
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
app = Flask(__name__)

@app.route("/", methods = ['GET'])
def get_dato():
    url_computers = urlopen("https://webscraper.io/test-sites/e-commerce/scroll/computers")
    url_phones = urlopen("https://webscraper.io/test-sites/e-commerce/scroll/phones")
    datoC = list()
    computerObj = BeautifulSoup(url_computers, 'html.parser')
    datosComputer = computerObj.findAll("div", {"class":"caption"})
    for datoComputer in datosComputer:
        datoC.append({
            "nombre": datoComputer.find("a", {"class":"title"}).text,
            "caracteristicas": datoComputer.find("p", {"class":"description"}).text,
            "valor":datoComputer.find("h4", {"class":"price"}).text
         })
    datoP = list()
    phonesObj = BeautifulSoup(url_phones, 'html.parser')
    datosPhone = phonesObj.findAll("div", {"class":"caption"})
    for datoPhone in datosPhone:
        datoP.append({
            "nombre": datoPhone.find("a", {"class":"title"}).text,
            "caracteristicas": datoPhone.find("p", {"class":"description"}).text,
            "valor":datoPhone.find("h4", {"class":"price"}).text
         })

    with open('phones.json', 'w') as file:
        json.dump(datoP, file, indent=4, sort_keys=True)
    with open('computers.json', 'w') as file:
        json.dump(datoC, file, indent=4, sort_keys=True)


    return render_template('index.html', datoP=datoP, datoC=datoC)
