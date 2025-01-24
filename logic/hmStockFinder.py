import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from util.pageSource import fetch_page_source

def checkStockHM(url, size):
    soup = fetch_page_source(url, wait_time=random.randint(5, 10))

    if not soup:
        return "Sayfa yüklenemedi."

    # Kullanıcıdan alınan bedenle eşleşen label'i bul
    size_label = soup.find('label', attrs={'for': size})

    if not size_label:
        return f"{size} bedeni bulunamadı."
    
    # Eğer label içinde class="fb3bce" varsa, stokta yok demek
    if 'fb3bce' in size_label.get('class', []):
        return f"{size} bedeni için stokta yok."
    
    # Stokta varsa
    return f"{size} bedeni için stokta bulundu."