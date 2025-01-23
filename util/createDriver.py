from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def create_driver():
    options = Options()
    options.add_argument("--headless")  # Arka planda çalıştırmak için
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


    return webdriver.Chrome(options=options)