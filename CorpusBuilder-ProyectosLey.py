from bs4 import BeautifulSoup
from bs4.element import Declaration
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import re
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import operator
import math

def Limpiar(arreglo):
    numeros = []
    textos = []
    for i in arreglo:
        if not i.isnumeric():
            aux = i.split("-")
            for j in aux:
                if j.isnumeric():
                    numeros.append(j)
                else:
                    textos.append(j)
        else:
            numeros.append(i)
    return(numeros)

def Preprocessing_Especial(cadena, stop_words):
    cadena_minuscula = cadena.lower()
    pattern = re.compile('[,.\"!@#$%^&*(){}?/;`~:<>+=°]')
    cadena_minuscula = pattern.sub('', cadena_minuscula)
    arreglo_cadena = word_tokenize(cadena_minuscula)
    arreglo_cadena_sin_stopwords = [w for w in arreglo_cadena if not w in stop_words]
    leyes = []
    articulos = []
    urgencias = []
    legislativos = []
    supremos = []
    for i in range(len(arreglo_cadena_sin_stopwords)-1):
        if arreglo_cadena_sin_stopwords[i] == "ley" or arreglo_cadena_sin_stopwords[i] == "leyes":
            k=i
            while(arreglo_cadena_sin_stopwords[k+1][0].isnumeric()):
                if k < len(arreglo_cadena_sin_stopwords)-2:
                    k+=1
                    leyes.append(arreglo_cadena_sin_stopwords[k])
                else:
                    leyes.append(arreglo_cadena_sin_stopwords[k+1])
                    break
                    
        elif arreglo_cadena_sin_stopwords[i] == "articulo" or arreglo_cadena_sin_stopwords[i] == "artículo" or arreglo_cadena_sin_stopwords[i] == "articulos" or arreglo_cadena_sin_stopwords[i] == "artículos":
            k=i
            while(arreglo_cadena_sin_stopwords[k+1][0].isnumeric()):
                if k < len(arreglo_cadena_sin_stopwords)-2:
                    k+=1
                    articulos.append(arreglo_cadena_sin_stopwords[k])
                else:
                    articulos.append(arreglo_cadena_sin_stopwords[k+1])
                    break
                
        elif arreglo_cadena_sin_stopwords[i] == "urgencia":
            k=i
            while(arreglo_cadena_sin_stopwords[k+1][0].isnumeric()):
                if k < len(arreglo_cadena_sin_stopwords)-2:
                    k+=1
                    urgencias.append(arreglo_cadena_sin_stopwords[k])
                else:
                    urgencias.append(arreglo_cadena_sin_stopwords[k+1])
                    break
                
        elif arreglo_cadena_sin_stopwords[i] == "legislativo":
            k=i
            while(arreglo_cadena_sin_stopwords[k+1][0].isnumeric()):
                if k < len(arreglo_cadena_sin_stopwords)-2:
                    k+=1
                    legislativos.append(arreglo_cadena_sin_stopwords[k])
                else:
                    legislativos.append(arreglo_cadena_sin_stopwords[k+1])
                    break
                
        elif arreglo_cadena_sin_stopwords[i] == "supremo":
            k=i
            while(arreglo_cadena_sin_stopwords[k+1][0].isnumeric()):
                if k < len(arreglo_cadena_sin_stopwords)-2:
                    k+=1
                    supremos.append(arreglo_cadena_sin_stopwords[k])
                else:
                    supremos.append(arreglo_cadena_sin_stopwords[k+1])
                    break
    return(Limpiar(leyes),articulos,Limpiar(urgencias),Limpiar(legislativos),Limpiar(supremos))

def remove_useless_data(row, stop_words=[]):
    pattern1 = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    pattern2 = re.compile('[,.\"!@#$%^&*(){}?/;`~:<>+=-]')
    table = str.maketrans('', '', string.punctuation)

    row = row.lower()
    row = pattern1.sub('', row)
    row = pattern2.sub('', row)
    tokens = word_tokenize(row)
    row_no_punctuation = [w.translate(table) for w in tokens]
    row_no_num = [w for w in row_no_punctuation if w.isalpha()]
    row = [w for w in row_no_num if not w in stop_words]
    # row = [PorterStemmer().stem(w) for w in row_no_num if not w in stop_words]
    # row = [SnowballStemmer('spanish').stem(w) for w in row_no_num if not w in stop_words]
    row = ' '.join(row)
    return row

def modificar_a_textos(leyes,articulos,urgencias,legislativos,supremos):
    texto = " "
    for i in leyes:
        texto += "ley["+i+"] "
    for i in articulos:
        texto += "artículo["+i+"] "
    for i in urgencias:
        texto += "urgencia["+i+"] "
    for i in legislativos:
        texto += "legislativo["+i+"] "
    for i in supremos:
        texto += "supremo["+i+"] "
    return texto

ubicacion = 'chromedriver.exe'
#Ruta del driver - Selenium
driver = webdriver.Chrome(executable_path=ubicacion)

#Ruta Proyectos de Ley 2016-2021
home_link = "https://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2016.nsf/Local%20Por%20Numero%20Inverso?OpenView"
driver.get(home_link)

texto = []
pg_amount = 2 #Número de páginas visitadas
base = "https://www2.congreso.gob.pe"
page = BeautifulSoup(driver.page_source,'html.parser')
stop_words = open('spanish.txt', 'r')
special_words = ["ley","leyes","artículo","articulo","artículos","articulos","legislativo","urgencia","supremo"]
spanish_stop_words = stop_words.read().splitlines()
            
#Recorrido tablas que contienen leyes
tables = page.find_all("table")

j = 0
for i in range(1, pg_amount+1):    
    for row in tables[2].findAll("tr"):
        if(501 == j):
            print("fin 1 ")
            break
        cells = row.find_all('td')
        texto.clear()
        for cell in cells:
            if(cell.find('a')):
                a = cell.find('a')
                url = a.attrs['href']
                texto.append(url)
            if(cell.text!=''):
                texto.append(cell.text)   
        if(texto!=[]):
            #Recuperación de Metadata
            driver.get(base+str(texto[0]))
            page = BeautifulSoup(driver.page_source,'html.parser')
            Inputs = page.find_all("input")
            Titulo = ""
            Descripcion = ""
            Completo = 0
            for Input in Inputs:
                Input = str(Input)
                if Input.__contains__('<input name="TitIni"'):
                    Titulo=Input[42:-3]
                    Completo+=1
                elif Input.__contains__('<input name="SumIni"'):
                    Descripcion=Input[42:-3]
                    Completo+=1
                if(Completo == 2):
                    break
            textito = texto[1].split("/")

            #Pre procesado
            cadena = Titulo + Descripcion
            leyes,articulos,urgencias,legislativos,supremos = Preprocessing_Especial(cadena, spanish_stop_words)
            corpus_procesado = remove_useless_data(cadena,spanish_stop_words+special_words)
            adicional = modificar_a_textos(leyes,articulos,urgencias,legislativos,supremos)
            corpus_final = corpus_procesado+adicional

            #Creación archivos .txt
            if (corpus_final != " "):
                Archivo = open("./Corpus/"+textito[0]+"-"+textito[1]+".txt","w")
                Archivo.write(corpus_final)
                Archivo.close
                j += 1

    home_link = "https://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2016.nsf/Local%20Por%20Numero%20Inverso?OpenView"
    driver.get(home_link)

    #Paso a una nueva página
    for k in range(0,i):
        #Click botón siguiente
        next_btn = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/p/table/tbody/tr/td[3]/a') 
        next_btn.click()   
    page = BeautifulSoup(driver.page_source,'html.parser')
    tables = page.find_all("table")
    
    if(501 == j):
        break