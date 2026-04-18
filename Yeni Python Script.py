import os
import subprocess

def git_batch_push_bypass(batch_size=3):
    target_folder = "Bypass"
    
    if not os.path.exists(target_folder):
        print(f"❌ Hata: '{target_folder}' klasörü bulunamadı!")
        return

    # ÖNCE: Dosya isimlerini değiştirerek GitHub'ın takibini kıralım
    # (Eğer dosya isminde zaten '_v' varsa tekrar eklemez)
    for f in os.listdir(target_folder):
        if f.endswith('.zip') and '_v' not in f:
            old_path = os.path.join(target_folder, f)
            new_name = f.replace('.zip', '_v.zip')
            new_path = os.path.join(target_folder, new_name)
            os.rename(old_path, new_path)

    # Yeni isimli dosyaları listele
    all_zips = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith('.zip')]
    
    total_files = len(all_zips)
    print(f"🚀 Toplam {total_files} zip dosyası (yeniden isimlendirildi) bulundu. {batch_size}'erli gruplanıyor...")

    for i in range(0, total_files, batch_size):
        batch = all_zips[i : i + batch_size]
        grup_no = (i // batch_size) + 1
        
        print(f"\n--- Grup {grup_no} İşleniyor ---")
        
        for file_path in batch:
            subprocess.run(["git", "add", file_path], capture_output=True)
        
        commit_message = f"Grup {grup_no} yuklendi"
        result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True)
        
        if result.returncode == 0:
            print(f"📦 Grup {grup_no} commit edildi. Push yapılıyor...")
            # FORCE ekleyerek gönderiyoruz
            push_result = subprocess.run(["git", "push", "origin", "main", "--force"], capture_output=True, text=True)
            
            if push_result.returncode == 0:
                print(f"✅ Grup {grup_no} başarıyla gönderildi!")
            else:
                print(f"❌ Grup {grup_no} hatası: {push_result.stderr}")
                break
        else:
            print(f"⚠️ Grup {grup_no} değişikliği yok.")

if __name__ == "__main__":
    git_batch_push_bypass(3)