import os
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox, Listbox, ttk
import threading
import time
import webbrowser
import smtplib
import sv_ttk
import pywinstyles
from email.mime.text import MIMEText

# ADD PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.hmStockFinder import checkStockHM
from logic.stradivariusStockFinder import check_stockStradivarius
from logic.zaraStockFinder import checkStockZara
from logic.bershkaStockFinder import checkStockBershka

# EMAIL INFORMATION
EMAIL_ADDRESS = "example@gmail.com"  # MAIL ADDRESS
EMAIL_PASSWORD = "jwci hsjw pmmk nzzz"   # MAIL APPLICATION PASSWORD (YOU CAN USE GMAIL FOR THIS)

auto_check_interval = 180  # Default 3 hours

products = []
found_products = []
auto_check_active = False

def set_check_interval():
    global auto_check_interval
    try:
        interval = int(interval_entry.get())
        if interval <= 0:
            raise ValueError
        auto_check_interval = interval
        log_message(f"Otomatik kontrol aralığı {interval} dakika olarak ayarlandı.")
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")

def start_auto_check():
    global auto_check_active
    if auto_check_active:
        return  # Zaten çalışıyorsa tekrar başlatma

    auto_check_active = True
    btn_start_auto.config(bg="lightgreen")  # Buton rengini yeşil yap
    log_message("Otomatik kontrol başladı...")

    def auto_check():
        while auto_check_active:
            check_all_products()
            log_message(f"Bir sonraki kontrol {auto_check_interval} dakika sonra...")
            time.sleep(auto_check_interval * 60)  # Kullanıcının ayarladığı süreyi bekle

    threading.Thread(target=auto_check, daemon=True).start()


# E-posta adresi ekleme fonksiyonu
def add_email():
    email = email_entry.get().strip()
    if email:
        email_list.insert(tk.END, email)
        email_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Hata", "Lütfen bir e-posta adresi girin!")

# E-posta adresi silme fonksiyonu
def remove_selected_email():
    selection = email_list.curselection()
    if selection:
        email_list.delete(selection[0])
    else:
        messagebox.showerror("Hata", "Lütfen silmek için bir e-posta adresi seçin!")

# Tüm e-posta adreslerini temizleme
def clear_email_list():
    email_list.delete(0, tk.END)

# E-posta gönderme fonksiyonu
def send_email(subject, body):
    recipients = email_list.get(0, tk.END)
    if not recipients:
        log_message("E-posta gönderilemedi: Alıcı listesi boş!")
        return

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = ", ".join(recipients)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
        log_message("Bildirim e-postası gönderildi.")
    except Exception as e:
        log_message(f"E-posta gönderilirken hata oluştu: {e}")


# Ürün kontrol fonksiyonu
def check_all_products():
    threads = []
    for product in products[:]:  # Listeyi kopyalayarak dön
        link, size = product
        thread = threading.Thread(target=check_single_product, args=(link, size))
        threads.append(thread)
        thread.start()

    # Tüm iş parçacıklarının bitmesini bekle
    for thread in threads:
        thread.join()

    # Tüm kontroller bittikten sonra toplu e-posta gönder
    if found_products:
        body = "Aşağıdaki ürünler stokta bulundu:\n\n" + "\n".join(
            [f"Link: {link}, Beden: {size}" for link, size in found_products]
        )
        send_email("Ürün Stok Bildirimi", body)
        log_message("Tüm ürünler kontrol edildi. Bildirim e-postası gönderildi.")
    else:
        log_message("Tüm ürünler kontrol edildi. Stokta bulunan ürün yok.")

# Tek ürün kontrolü (iş parçacığı içinde)
# Tek ürün kontrolü (iş parçacığı içinde)
def check_single_product(link, size):
    result = None
    if "hm.com" in link:
        result = checkStockHM(link, size)
    elif "zara.com" in link:
        result = checkStockZara(link, size)
    elif "stradivarius.com" in link:
        result = check_stockStradivarius(link, size)
    elif "bershka.com" in link:
        result = checkStockBershka(link, size)
    else:
        result = "Bu site desteklenmiyor."

    if result and "stokta bulundu" in result.lower():  # Ürün bulunursa
        found_products.append((link, size))
        products.remove((link, size))  # Bulunan ürünü ana listeden çıkar
        update_product_list()
        log_message(f"{link} ({size}): Ürün bulundu! Bulunan Ürünler listesine eklendi.")
    else:
        log_message(f"{link} ({size}): {result or 'Hiçbir sonuç alınamadı.'}")

# Log mesajı yazdırma
def log_message(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)

# Ürün ekleme fonksiyonu
def add_product():
    link = link_entry.get()
    size = size_entry.get()

    if not link.strip():
        messagebox.showerror("Hata", "Lütfen bir link girin!")
        return
    if not size.strip():
        messagebox.showerror("Hata", "Lütfen bir beden girin!")
        return

    products.append((link, size))
    update_product_list()
    link_entry.delete(0, tk.END)
    size_entry.delete(0, tk.END)

# Ürün silme fonksiyonu
def remove_selected_product():
    selection = product_list.curselection()
    if selection:
        products.pop(selection[0])
        update_product_list()
    else:
        messagebox.showerror("Hata", "Lütfen silmek için bir ürün seçin!")

# Tüm ürünleri temizleme fonksiyonu
def clear_product_list():
    products.clear()
    update_product_list()


# Ürün listesi güncelleme
def update_product_list():
    product_list.delete(0, tk.END)
    for link, size in products:
        product_list.insert(tk.END, f"{link} ({size})")
    found_product_list.delete(0, tk.END)
    for link, size in found_products:
        found_product_list.insert(tk.END, f"{link} ({size})")

# Linke tıklama işlevi
def open_link(event):
    selection = product_list.curselection()
    if selection:
        index = selection[0]
        link, _ = products[index]
        webbrowser.open(link)

def open_found_link(event):
    selection = found_product_list.curselection()
    if selection:
        index = selection[0]
        link, _ = found_products[index]
        webbrowser.open(link)

# Otomatik kontrol başlatma
def start_auto_check():
    global auto_check_active
    if auto_check_active:
        return  # Zaten çalışıyorsa tekrar başlatma

    auto_check_active = True
    log_message("Otomatik kontrol başladı...")

    def auto_check():
        while auto_check_active:
            check_all_products()
            log_message(f"Bir sonraki kontrol {auto_check_interval} dakika sonra...")
            time.sleep(auto_check_interval  * 60)  # 3 saat bekle

    threading.Thread(target=auto_check, daemon=True).start()

# Otomatik kontrolü durdurma
def stop_auto_check():
    global auto_check_active
    auto_check_active = False
    log_message("Otomatik kontrol durduruldu.")



root = tk.Tk()
root.title("Ürün Stok Kontrol Uygulaması")
root.geometry("800x600")
sv_ttk.set_theme("light" if sv_ttk.get_theme() == "dark" else "dark")


# Tab Kontrol
tab_control = ttk.Notebook(root)

# Ürünler Tabı
tab_products = ttk.Frame(tab_control)
tab_control.add(tab_products, text="Ürünler")

# Üst Çerçeve: Link, Beden ve Aralık
frame_product_top = ttk.Frame(tab_products)
frame_product_top.pack(pady=10)
ttk.Label(frame_product_top, text="Link: ").pack(side=tk.LEFT)
link_entry = ttk.Entry(frame_product_top, width=50)
link_entry.pack(side=tk.LEFT, padx=5)
ttk.Label(frame_product_top, text="Beden: ").pack(side=tk.LEFT)
size_entry = ttk.Entry(frame_product_top, width=10)
size_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(frame_product_top, text="Ekle", command=add_product).pack(side=tk.LEFT, padx=5)

frame_interval = ttk.Frame(tab_products)
frame_interval.pack(pady=5)
ttk.Label(frame_interval, text="Kontrol Aralığı (dakika):").pack(side=tk.LEFT)
interval_entry = ttk.Entry(frame_interval, width=10)
interval_entry.insert(0, "180")
interval_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(frame_interval, text="Ayarla", command=set_check_interval).pack(side=tk.LEFT, padx=5)

# Ürün Listesi
frame_product_list = ttk.Frame(tab_products)
frame_product_list.pack(pady=10, fill=tk.BOTH, expand=True)
product_list = tk.Listbox(frame_product_list, height=10, width=80)
product_list.pack(fill=tk.BOTH, expand=True)
product_list.bind("<Double-Button-1>", open_link)  # Çift tıklama ile link açma işlevi

# Otomatik Kontrol Butonları
frame_auto_control = ttk.Frame(tab_products)
frame_auto_control.pack(pady=10)
btn_start_auto = ttk.Button(frame_auto_control, text="Otomatik Kontrolü Başlat", command=start_auto_check)
btn_start_auto.pack(side=tk.LEFT, padx=5)
btn_stop_auto = ttk.Button(frame_auto_control, text="Otomatik Kontrolü Durdur", command=stop_auto_check)
btn_stop_auto.pack(side=tk.LEFT, padx=5)

# Bulunan Ürünler Listesi
ttk.Label(frame_product_list, text="Bulunan Ürünler:").pack(anchor="w")
found_product_list = tk.Listbox(frame_product_list, height=10, width=80)
found_product_list.pack(fill=tk.BOTH, expand=True)
found_product_list.bind("<Double-Button-1>", open_found_link)  # Çift tıklama ile link açma işlevi

# E-posta Tabı
tab_emails = ttk.Frame(tab_control)
tab_control.add(tab_emails, text="E-posta Listesi")

frame_email = ttk.Frame(tab_emails)
frame_email.pack(pady=10)
ttk.Label(frame_email, text="E-posta: ").pack(side=tk.LEFT)
email_entry = ttk.Entry(frame_email, width=40)
email_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(frame_email, text="Ekle", command=add_email).pack(side=tk.LEFT, padx=5)
ttk.Button(frame_email, text="Seçiliyi Sil", command=remove_selected_email).pack(side=tk.LEFT, padx=5)
ttk.Button(frame_email, text="Tümünü Sil", command=clear_email_list).pack(side=tk.LEFT, padx=5)

email_list = tk.Listbox(tab_emails, height=10, width=80)
email_list.pack(fill=tk.BOTH, expand=True)

# Loglar Tabı
tab_logs = ttk.Frame(tab_control)
tab_control.add(tab_logs, text="Loglar")
log_box = scrolledtext.ScrolledText(tab_logs, height=20, width=80)
log_box.pack(fill=tk.BOTH, expand=True)

# Sekme Yerleşimi
tab_control.pack(expand=1, fill="both")

root.mainloop()
