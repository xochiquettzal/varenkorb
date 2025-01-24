import os
import random
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.pageSource import fetch_page_source

def check_stockStradivarius(url, size):
    
    soup = fetch_page_source(url, wait_time=random.randint(5, 10))

    if not soup:
        return "Sayfa yüklenemedi."

    # Beden seçici container'ını bul
    size_selector_container = soup.find('div', class_='size-selector-container')
    
    if not size_selector_container:
        return "Beden seçici bulunamadı."
    
    # Bedenleri içeren div'i bul
    size_items = size_selector_container.find_all('div', class_='size-item')
    
    # Kullanıcıdan alınan beden ile eşleşen div'i bul
    for item in size_items:
        size_name = item.find('div', class_='size-name')
        if size_name and size_name.get_text().strip() == size:
            # Stok durumu için class değerini kontrol et
            if 'size-no-stock' in item['class'] or 'size-item  size-back-soon' in item['class']:
                return f"{size} bedeni için stok bulunamadı."
            else:
                return f"{size} bedeni için stokta bulundu."
    
    return f"{size} bedeni bulunamadı."