#bliotecas necessarias 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
#biblioteca de funcionalidades no teclado
from selenium.webdriver.common.action_chains import ActionChains
#biblioteca de expessão de linguagem
import re
from googletrans import Translator
import os

# Carrega o WhatsApp com o login sem QR Code ****AJUDA DE FORUM****
dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir={}".format(profile))


service = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=service, options=options)
nav.get('https://web.whatsapp.com/')
time.sleep(15)


temporizador = 120 
start_time = time.time()

while len(nav.find_elements("id", "side")) < 1:
    print("Carregando QR code")
    if time.time() - start_time > temporizador:
        print("Tempo limite de espera atingido. Fechando o navegador.")
        nav.quit()  
        exit()
    time.sleep(10)
print("Carregamento concluido")

time.sleep(1)
nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/button/div[2]/span').click()
nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys("11973809701")
nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.ENTER)


def scrapywhats():
    url = 'https://appsumo.com/software/?sort=latest'
    requisição = requests.get(url)
    site = BeautifulSoup(requisição.text, 'html.parser')
    Nome = site.find_all('span', class_='overflow-hidden text-ellipsis whitespace-nowrap font-bold max-md:text-xs')
    descrição = site.find_all('div', class_='my-1 line-clamp-3 max-md:text-xs md:text-center')
    preco = site.find_all('div', class_='font-medium md:text-2xl')  
    Produto = [item.text for item in Nome] #separação de cada item por vez 
    descri = [desc.text for desc in descrição]
    precos_texto = [item.text for item in preco]
    #filtagrem do valor do ltd devido a separação de divs e classes
    precos_filtrados = [re.findall(r"\$\d+", item)[0] for item in precos_texto if re.findall(r"\$\d+", item)] #ajuda gpt
    descri_traduzida = []
    translator = Translator()

    for traduz in descri:
        traducao = translator.translate(traduz, src='en', dest='pt')
        descri_traduzida.append(traducao.text)

    caixa_de_mensagem = nav.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    
    for texto, desc, ltd, in zip(Produto[:10], descri_traduzida[:10], precos_filtrados[:10]):
        caixa_de_mensagem.send_keys(f"Nome: {texto}")
        ActionChains(nav).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        caixa_de_mensagem.send_keys(f"Descrição: {desc}")
        ActionChains(nav).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        caixa_de_mensagem.send_keys(f"Valor LTD: {ltd}")
        ActionChains(nav).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        caixa_de_mensagem.send_keys("---------")
        ActionChains(nav).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        
    caixa_de_mensagem.send_keys(Keys.ENTER)

scrapywhats()
time.sleep(5)
print("Concluido") 