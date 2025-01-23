import requests
from bs4 import BeautifulSoup

def checkStockZara(url, size="M"): #
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"Sayfaya ulaşılamadı. HTTP Durum Kodu: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # İlgili divleri bul
        size_elements = soup.find_all("div", class_="size-selector-sizes-size__label", 
                                      attrs={"data-qa-qualifier": "size-selector-sizes-size-label"})

        for size_element in size_elements:
            if size_element.text.strip() == size:
                next_sibling = size_element.find_next_sibling("div", class_="size-selector-sizes-size__view-similars")
                
                if next_sibling:
                    return f"{size} bedeni stokta bulunamadı."
                else:
                    return f"{size} bedeni stokta bulundu."

        return f"{size} bedeni sayfada bulunamadı."

    except Exception as e:
        return f"Hata oluştu: {e}"