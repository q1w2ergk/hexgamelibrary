import os
import shutil
import subprocess
import time

# --- KESİN AYARLAR ---
kaynak_dizini = r"C:\Users\koyun\Documents\RedXFreeSteamInstaller-main\Bypass"
hedef_dizini = r"C:\Users\koyun\Documents\GitHub\hexgamelibrary\hexgamelibrary\Bypass"
repo_yolu = r"C:\Users\koyun\Documents\GitHub\hexgamelibrary\hexgamelibrary"

def git_komutu(komut):
    try:
        # Komutları terminale yazıyormuş gibi çalıştırır
        result = subprocess.run(komut, cwd=repo_yolu, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.stderr}")
        return False

def dosya_isleme_dongusu():
    if not os.path.exists(kaynak_dizini):
        print("Kaynak klasör bulunamadı!")
        return

    # Hedef klasörü hazırla
    if not os.path.exists(hedef_dizini):
        os.makedirs(hedef_dizini)

    zip_dosyalari = [f for f in os.listdir(kaynak_dizini) if f.endswith('.zip')]
    
    if not zip_dosyalari:
        print("İşlenecek .zip kalmadı.")
        return

    for dosya in zip_dosyalari:
        print(f"\n>>> İşleniyor: {dosya}")
        
        # 1. Dosyayı taşı
        shutil.move(os.path.join(kaynak_dizini, dosya), os.path.join(hedef_dizini, dosya))
        
        # 2. Git işlemlerini sırayla yap
        print("Git: Dosya ekleniyor ve commit ediliyor...")
        git_komutu(["git", "add", "."])
        git_komutu(["git", "commit", "-m", f"{dosya} eklendi", "--allow-empty"])
        
        # 3. LFS ve Push (Kritik nokta)
        print("Git: GitHub'a gönderiliyor (LFS dahil)...")
        # Sadece bu commit'i pushlamaya çalışır
        if git_komutu(["git", "push", "origin", "main", "--force"]):
            print(f"+++ {dosya} başarıyla gönderildi.")
        else:
            print(f"--- {dosya} gönderilirken hata oluştu, bir sonrakine geçiliyor.")
        
        # GitHub'ı yormayalım
        time.sleep(2)

if __name__ == "__main__":
    # Önce LFS'in kurulu olduğundan emin olalım
    subprocess.run(["git", "lfs", "install"], cwd=repo_yolu)
    dosya_isleme_dongusu()