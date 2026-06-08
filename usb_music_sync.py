#!/usr/bin/env python3
import os
import shutil
import time
import logging
from pathlib import Path
import subprocess

# ===== CONFIGURAZIONE =====
SOURCE_DIR = "/root/Musica"
USB_DEST_FOLDER = "Cantautorato"
USB_MOUNT_POINT = "/mnt/usb"
LOG_FILE = "/var/log/usb_music_sync.log"
CHECK_INTERVAL = 5
SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class USBMusicSyncer:
    def __init__(self):
        Path(USB_MOUNT_POINT).mkdir(parents=True, exist_ok=True)
        Path(SOURCE_DIR).mkdir(parents=True, exist_ok=True)
    
    def get_usb_devices(self):
        try:
            result = subprocess.run(['lsblk', '-o', 'NAME,TYPE', '-l'], capture_output=True, text=True)
            usb_devices = []
            for line in result.stdout.split('\n'):
                if 'part' in line:
                    device = line.split()[0]
                    check = subprocess.run(['udevadm', 'info', '--query=property', f'/dev/{device}'], 
                                         capture_output=True, text=True)
                    if 'ID_BUS=usb' in check.stdout:
                        usb_devices.append(f'/dev/{device}')
            return usb_devices
        except Exception as e:
            logger.error(f"Errore USB: {e}")
            return []
    
    def mount_usb(self, device):
        try:
            mount_point = f"{USB_MOUNT_POINT}/{os.path.basename(device)}"
            Path(mount_point).mkdir(parents=True, exist_ok=True)
            result = subprocess.run(['mount', device, mount_point], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ USB montata")
                return mount_point
            return None
        except Exception as e:
            logger.error(f"Errore mount: {e}")
            return None
    
    def unmount_usb(self, mount_point):
        try:
            subprocess.run(['umount', mount_point], capture_output=True)
            os.rmdir(mount_point)
        except:
            pass
    
    def sync_music_to_usb(self, usb_path):
        try:
            dest_dir = os.path.join(usb_path, USB_DEST_FOLDER)
            Path(dest_dir).mkdir(parents=True, exist_ok=True)
            
            pi_files = []
            for ext in SUPPORTED_EXTENSIONS:
                pi_files.extend(Path(SOURCE_DIR).glob(f'*{ext}'))
                pi_files.extend(Path(SOURCE_DIR).glob(f'*{ext.upper()}'))
            
            if not pi_files:
                logger.info(f"❌ Nessun file in {SOURCE_DIR}")
                return
            
            logger.info(f"🎵 Trovati {len(pi_files)} file sul Pi")
            
            copied = 0
            skipped = 0
            
            for pi_file in pi_files:
                dest_file = os.path.join(dest_dir, pi_file.name)
                
                # CONTROLLA SE IL FILE ESISTE GIÀ → SALTA
                if os.path.exists(dest_file):
                    logger.info(f"⏭️ Già esiste, saltato: {pi_file.name}")
                    skipped += 1
                else:
                    shutil.copy2(pi_file, dest_file)
                    logger.info(f"✅ Copiato: {pi_file.name}")
                    copied += 1
            
            logger.info(f"📊 Completato: {copied} copiati, {skipped} saltati (già esistenti)")
            
        except Exception as e:
            logger.error(f"Errore: {e}")
    
    def run(self):
        logger.info("="*50)
        logger.info(f"🚀 Backup USB - Source: {SOURCE_DIR}")
        logger.info(f"📁 Destinazione USB: {USB_DEST_FOLDER}")
        logger.info("="*50)
        
        last_usb = False
        while True:
            try:
                usb = self.get_usb_devices()
                if usb and not last_usb:
                    logger.info(f"🔌 USB rilevata")
                    mp = self.mount_usb(usb[0])
                    if mp:
                        self.sync_music_to_usb(mp)
                        self.unmount_usb(mp)
                        logger.info("✅ Backup completo! Puoi rimuovere la USB")
                elif not usb and last_usb:
                    logger.info("🔌 USB rimossa")
                last_usb = bool(usb)
                time.sleep(CHECK_INTERVAL)
            except KeyboardInterrupt:
                logger.info("⏹️ Fermato")
                break
            except Exception as e:
                logger.error(f"Errore: {e}")
                time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ Esegui con: sudo python3 usb_music_sync.py")
        exit(1)
    
    if not os.path.exists(SOURCE_DIR):
        print(f"⚠️ Directory {SOURCE_DIR} non esiste!")
        print(f"Creala con: mkdir -p {SOURCE_DIR}")
        exit(1)
    
    USBMusicSyncer().run()
