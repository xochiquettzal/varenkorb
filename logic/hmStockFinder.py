import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from util.createDriver import create_driver

""" def scrape_website(url):
    try:
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

def checkStockHM(url, size):
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
    
    # Kullanıcıdan alınan bedenle eşleşen label'i bul
    size_label = soup.find('label', attrs={'for': size})

    if not size_label:
        return f"{size} bedeni bulunamadı."
    
    # Eğer label içinde class="fb3bce" varsa, stokta yok demek
    if 'fb3bce' in size_label.get('class', []):
        return f"{size} bedeni için stokta yok."
    
    # Stokta varsa
    return f"{size} bedeni için stokta bulundu."




""" # Örnek kullanım
url = "https://www2.hm.com/tr_tr/productpage.0941666068.html"
size = "48"  # Kullanıcıdan alınan beden

# Sayfa içeriğini al
soup = scrape_website(url)

# Stok durumu kontrol et
stock_status = check_stock(soup, size)
print(stock_status)
 """