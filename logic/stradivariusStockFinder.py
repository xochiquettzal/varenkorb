import os
import random
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.createDriver import create_driver

def check_stockStradivarius(url, size):
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

""" # Örnek kullanım
url = "https://www.stradivarius.com/tr/z%C4%B1mbal%C4%B1-babet-l19616470?colorId=040&style=12&pelement=436141585"
size = "41"  # Kullanıcıdan alınan beden

# Stok durumu kontrol et
stock_status = check_stock(url, size)
print(stock_status) """



""" def scrape_website(url):
    try:
        driver = create_driver()
        driver.get(url)

        # Dinamik içerik için sayfanın tam yüklenmesini bekleme (örneğin 5 saniye)
        time.sleep(random.randint(5, 10))

        # Sayfa kaynağını al
        page_source = driver.page_source
        
        # Sayfa içeriğini BeautifulSoup ile parse et
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

    finally:
        driver.quit()  # WebDriver'ı kapat """