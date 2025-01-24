import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from util.pageSource import fetch_page_source

def checkStockBershka(url, size):
    soup = fetch_page_source(url, wait_time=random.randint(5, 10))

    if not soup:
        return "Sayfa yüklenemedi."
    
    # Hedef div'i bul
    size_selector_div = soup.find('div', class_='size-selector-desktop-pdp__sizes')
    if not size_selector_div:
        return "Beden seçici bulunamadı."
    
    # Butonları bul
    lis = size_selector_div.find_all('li')
    
    for li in lis:
        # Span içindeki beden text'ini bul
        span = li.find('span', class_='text__label')
        if span and span.text.strip() == size:  # Beden eşleşiyorsa
            li_class = li.get('class', [])
            # Stok durumuna göre döndür
            if 'is-csbs is-disabled ui--size-dot-list__item--last' in li_class or 'is-disabled' in li_class or 'is-disabled ui--size-dot-list__item--last' in li_class or 'is-csbs is-disabled' in li_class:
                return f"{size} bedeni için stok bulunamadı."
            elif 'is-last-units' in li_class or 'ui--size-dot-list__item--last' in li_class or 'is-last-units ui--size-dot-list__item--last' in li_class or not li_class:
                return f"{size} bedeni için stokta bulundu."
    
    return f"{size} bedeni bulunamadı."


checkStockBershka("https://www.bershka.com/tr/fitilli-%C3%B6rg%C3%BC-kazak-c0p177326330.html?colorId=251", "XS")