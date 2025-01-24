import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def create_driver():
    options = Options()
    options.add_argument("--headless")  # Arka planda çalıştırmak için
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


    return webdriver.Chrome(options=options)

def fetch_page_source(url, wait_time=5):
    """
    Verilen URL'den Selenium ile sayfa kaynağını getirir.
    Args:
        url (str): Açılacak URL.
        wait_time (int): Sayfanın yüklenmesi için bekleme süresi.
    Returns:
        BeautifulSoup: Sayfa kaynağını döner.
    """
    try:
        driver = create_driver()
        driver.get(url)
        time.sleep(wait_time)  # Sayfanın yüklenmesi için bekleme süresi
        page_source = driver.page_source
        return BeautifulSoup(page_source, 'html.parser')
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None
    finally:
        driver.quit()