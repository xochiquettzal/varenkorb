import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from util.createDriver import create_driver

def checkStockBershka(url, size):
    try:
        driver = create_driver()
        driver.get(url)

        # Dinamik içerik için sayfanın tam yüklenmesini bekleme (örneğin 5 saniye)
        time.sleep(random.randint(5, 10))

        # Sayfa kaynağını al
        page_source = driver.page_source
        
        # Sayfa içeriğini BeautifulSoup ile parse et
        soup = BeautifulSoup(page_source, 'html.parser')
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

    finally:
        driver.quit()  # WebDriver'ı kapat

    if not soup:
        return "Sayfa yüklenemedi."
    if not soup:
        return "Sayfa yüklenemedi."
    
    # Hedef div'i bul
    size_selector_div = soup.find('div', class_='size-selector-desktop-pdp__sizes')
    if not size_selector_div:
        return "Beden seçici bulunamadı."
    
    # Butonları bul
    buttons = size_selector_div.find_all('button')
    
    for button in buttons:
        # Span içindeki beden text'ini bul
        span = button.find('span', class_='text__label')
        if span and span.text.strip() == size:  # Beden eşleşiyorsa
            button_class = button.get('class', [])
            # Stok durumuna göre döndür
            if 'cursor-default' in button_class and 'is-disabled' in button_class:
                return f"{size} bedeni için stok bulunamadı."
            elif 'ui--dot-item' in button_class and 'is-dot' in button_class:
                return f"{size} bedeni için stokta bulundu."
    
    return f"{size} bedeni bulunamadı."