# EMAIL INFORMATION
EMAIL_ADDRESS = "emreemreakb@gmail.com"  # MAIL ADDRESS
EMAIL_PASSWORD = "jwli hsje phmk nrvc"   # MAIL APPLICATION PASSWORD (YOU CAN USE GMAIL FOR THIS)

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