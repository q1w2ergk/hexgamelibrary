import os
import shutil
import subprocess
import time

# --- AYARLAR ---
# Kaynak: Zipleri aldığın yer
kaynak_dizini = r"C:\Users\koyun\Documents\RedXFreeSteamInstaller-main\Bypass"

# Hedef: Zipleri taşıdığın alt klasör
hedef_dizini = r"C:\Users\koyun\Documents\GitHub\hexgamelibrary\hexgamelibrary\Bypass"

# Git Reposunun Ana Dizini: .git klasörü muhtemelen buradadır
# Eğer yine hata verirse bu yolu r"C:\Users\koyun\Documents\GitHub\hexgamelibrary" olarak dene
repo_yolu = r"C:\Users\koyun\Documents\GitHub\hexgamelibrary\hexgamelibrary"
# ---------------

def git_islemlerini_yap():
    try:
        print(f"Git: Değişiklikler işleniyor...")
        
        # 1. Add
        subprocess.run(["git", "add", "."], cwd=repo_yolu, check=True)
        
        # 2. Commit
        # --allow-empty ekledim ki eğer değişiklik yoksa script takılmasın
        subprocess.run(["git", "commit", "-m", "grup1 eklendi", "--allow-empty"], cwd=repo_yolu, check=True)
        
        # 3. Push
        print("Git: Push işlemi yapılıyor...")
        subprocess.run(["git", "push", "origin", "main", "--force"], cwd=repo_yolu, check=True)
        
        print("İşlem Başarılı.\n")
    except subprocess.CalledProcessError as e:
        print(f"Git hatası: {e}")

def dosya_tasi_ve_islem_yap():
    if not os.path.exists(kaynak_dizini):
        print(f"Kaynak bulunamadı: {kaynak_dizini}")
        return

    dosyalar = [f for f in os.listdir(kaynak_dizini) if f.endswith('.zip')]
    
    if not dosyalar:
        print("Klasörde .zip dosyası kalmadı.")
        return

    if not os.path.exists(hedef_dizini):
        os.makedirs(hedef_dizini)

    for dosya_adi in dosyalar:
        kaynak_yolu = os.path.join(kaynak_dizini, dosya_adi)
        hedef_yolu = os.path.join(hedef_dizini, dosya_adi)
        
        print(f"Sıradaki: {dosya_adi}")
        
        try:
            shutil.move(kaynak_yolu, hedef_yolu)
            git_islemlerini_yap()
            # GitHub'ın spam olarak algılamaması için 2 saniye bekle
            time.sleep(2)
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    # ÖNEMLİ: Eğer .git klasörü bir üst dizindeyse kodu çalıştırmadan önce 
    # repo_yolu değişkenini bir üst klasöre ayarla.
    dosya_tasi_ve_islem_yap()