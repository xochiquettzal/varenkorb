import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def checkStockZara(url, size):
    try:
        # Selenium driver oluştur
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        
        # Sayfayı yükle
        driver.get(url)
        time.sleep(random.randint(5, 10))
        
        # Sayfayı yenile (cache'i tetiklemek için)
        driver.refresh()
        time.sleep(5)
        
        # Size selector'ın yüklenmesini bekle
        try:
            # Önce size selector container'ını bekle
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.size-selector-sizes"))
            )
            time.sleep(2)  # Ek bekleme süresi
        except Exception as e:
            # Eğer size selector bulunamazsa, sayfa kaynağını al ve kontrol et
            print(f"Size selector bulunamadı, sayfa kaynağı kontrol ediliyor: {e}")
        
        # Sayfa kaynağını al
        page_source = driver.page_source
        driver.quit()
        
        # HTML'i parse et
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Beden listesini bul
        size_list = soup.find("ul", class_="size-selector-sizes")
        if not size_list:
            return "Beden listesi bulunamadı."
        
        # İstenen bedeni ara
        size_found = False
        for li in size_list.find_all("li", class_="size-selector-sizes__size"):
            label_div = li.find("div", class_="size-selector-sizes-size__label")
            if label_div and label_div.text.strip() == size:
                size_found = True
                button = li.find("button", class_="size-selector-sizes-size__button")
                if not button:
                    return f"{size} bedeni için buton bulunamadı."
                
                action = button.get("data-qa-action", "")
                if action == "size-out-of-stock":
                    return f"{size} bedeni stokta bulunamadı."
                elif action == "size-low-on-stock":
                    return f"{size} bedeni stokta bulundu (az sayıda ürün)."
                elif action == "size-in-stock":
                    return f"{size} bedeni stokta bulundu."
                else:
                    return f"{size} bedeni için stok durumu anlaşılamadı."
        
        if not size_found:
            return f"{size} bedeni sayfada bulunamadı."
            
    except Exception as e:
        return f"Hata oluştu: {e}"