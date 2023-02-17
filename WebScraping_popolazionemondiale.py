# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import numpy as np
import pandas as pd
import datetime
import math
from bs4 import BeautifulSoup as bs
from html.parser import HTMLParser
import urllib
import re
url="https://it.wikipedia.org/wiki/Popolazione_mondiale"
pagina=requests.get(url).text
soup=bs(pagina,"html.parser")
tables=soup.find_all("table")

population_data = pd.DataFrame(columns=["Anno", "Mondo", "Africa", "Asia", "Europa","America Latina","Nord America","Oceania"])

def floatilize(amo):
    #essendo le strings prese da html vengono riconosciute solamente come string ed è
    #impossibile convertirle in float se non utilizzato il package re
    if (amo != []):
        amo=amo.replace("a.C.","")
        amo=amo.replace("\n","")
        amo=amo.replace(" ","")
        amo=amo.replace(";","")
        amo=amo.replace(" ","")
        amo=amo.replace("<","")
            
        amo=re.findall(r'\d+', amo)
        anno_assemblato=""
        
        
        for k, pezzo in enumerate(amo):
            anno_assemblato = anno_assemblato + pezzo
        anno_assemblato=float(anno_assemblato)
       
        return anno_assemblato

#metodo zappa per recuperare dati direttamente dal file html
#più laborioso del metodo successivo che sfrutta la gerarchia html
for j,row in enumerate(tables[2].tbody.find_all("tr")):
    cells=row.find_all("td")
    cells_1=row.find_all("th")
    if (cells != []):
        anno=cells_1[0].text
        anno=floatilize(anno)
        #gli if giungono per far funzionare floatilize anche quando il dato è NaN
        #che da html non è possibile tradurlo in float
        if j<13:
            anno=-anno
        mondo=cells[0].text.strip()
        mondo=floatilize(mondo)
        if j>10:
            africa=cells[1].text.strip()
            africa=floatilize(africa)
            asia=cells[2].text.strip()
            asia=floatilize(asia)
            europa=cells[3].text.strip()
            europa=floatilize(europa)
        else:
            africa=float("NaN")
            asia=float("NaN")
            europa=float("NaN")
        if j>13:
            am_lat=cells[4].text.strip()
            am_lat=floatilize(am_lat)
            am_nord=cells[5].text.strip()
            am_nord=floatilize(am_nord)
            oceania=cells[6].text.strip()
            oceania=floatilize(oceania)
        else:
            am_lat=float("NaN")
            am_nord=float("NaN")
            oceania=float("NaN")
        population_data = population_data.append({"Anno":anno,"Mondo":mondo, "Africa":africa, "Asia":asia,"Europa":europa, "America Latina":am_lat,"Nord America":am_nord,"Oceania":oceania}, ignore_index=True)
population_data["Mondo"][0]=population_data["Mondo"][0]/1000
population_data["Oceania"][21::]=population_data["Oceania"][21::]/10

#giocare coi dati e matplot
import matplotlib.pyplot as plt
plt.plot(population_data["Anno"][15::],population_data["Mondo"][15::])
plt.ylabel('Popolazione mondiale')
plt.xlabel("Anno")
plt.show()

#easy_way 
dataframe_list = pd.read_html(url, flavor='bs4')
df=pd.read_html(str(tables[8]), flavor='bs4')[0]
df2=pd.read_html(url, match="Nazione/Territorio con statuto speciale", flavor='bs4')[0]
#match ti recupera direttamente la table che vuoi
#read_html ti da una lista con tutte le tables


