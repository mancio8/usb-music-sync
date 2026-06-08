## 💾 USB Music Sync per Orange Pi Zero2

Script automatico che copia la musica dal Orange Pi alla USB quando viene inserita, con supporto multi-USB e gestione duplicati.

## ✨ Caratteristiche

- 🔄 **Backup automatico** - Copia la musica non appena inserisci la USB
- ⏭️ **Salta duplicati** - Non copia file già presenti sulla USB
- 📝 **Logging completo** - Tutte le operazioni sono tracciate
- 🚀 **Avvio automatico** - Si avvia con systemd all'accensione del Pi
- 🔧 **Facile configurazione** - Basta modificare una variabile

## 📋 Prerequisiti

- Orange Pi Zero2 (o qualsiasi Raspberry Pi)
- Python 3
- USB formattata (FAT32/NTFS/ext4)
- Permessi root (per montare USB)

## 🚀 Installazione Rapida

### 1. Clona il repository
```bash
git clone https://github.com/mancio8/usb-music-sync.git
cd usb-music-sync
```
2. Configura il percorso della musica
```bash

nano usb_music_sync.py
# Modifica questa riga:
# SOURCE_DIR = "/root/Musica"  → metti il tuo path
```
3. Crea la directory della musica
```bash

mkdir -p /root/Musica
# Copia qui i tuoi file MP3/FLAC
```
4. Prova lo script manualmente
```bash

chmod +x usb_music_sync.py
sudo python3 usb_music_sync.py
```
5. Configura l'avvio automatico (systemd)
```bash

sudo cp usb-music-sync.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable usb-music-sync
sudo systemctl start usb-music-sync
```
⚙️ Configurazione
Variabili principali nello script
Variabile	Descrizione	Default
SOURCE_DIR	Directory della musica sul Pi	/root/Musica
USB_DEST_FOLDER	Cartella sulla USB	MUSIC/Cantautorato
USB_MOUNT_POINT	Punto di mount USB	/mnt/usb
CHECK_INTERVAL	Secondi tra controlli USB	5
SUPPORTED_EXTENSIONS	Formati audio supportati	.mp3, .wav, .flac, .m4a, .ogg, .aac
USB Target (opzionale)

Per sincronizzare SOLO con una USB specifica:
```bash

# Metodo 1: Auto-rilevamento (inserisci la USB e avvia)
sudo python3 usb_music_sync.py

# Metodo 2: Manuale (modifica nello script)
TARGET_USB_SERIAL = "SANDISK_123456"  # Metti il seriale della tua USB
```
📝 Comandi Utili
Gestione del servizio
```bash

# Avviare il servizio
sudo systemctl start usb-music-sync

# Fermare il servizio
sudo systemctl stop usb-music-sync

# Riavviare il servizio
sudo systemctl restart usb-music-sync

# Stato del servizio
sudo systemctl status usb-music-sync

# Abilitare/disabilitare all'avvio
sudo systemctl enable usb-music-sync   # Abilita
sudo systemctl disable usb-music-sync  # Disabilita
```
Visualizzazione log
```bash

# Log in tempo reale (Ctrl+C per uscire)
tail -f /var/log/usb_music_sync.log

# Ultime 50 righe
tail -n 50 /var/log/usb_music_sync.log

# Tutto il log
cat /var/log/usb_music_sync.log

# Cerca errori nel log
grep "ERROR" /var/log/usb_music_sync.log

# Cerca file copiati
grep "Copiato" /var/log/usb_music_sync.log

# Cerca file saltati
grep "saltato" /var/log/usb_music_sync.log

# Log di systemd
sudo journalctl -u usb-music-sync -f
sudo journalctl -u usb-music-sync -n 50
```
Debug e troubleshooting
```bash

# Controlla se lo script è in esecuzione
ps aux | grep usb_music_sync.py

# Controlla USB collegate
lsblk
lsusb

# Controlla mount point
mount | grep usb

# Test manuale senza servizio
sudo python3 usb_music_sync.py

# Verifica permessi file
ls -la /root/usb_music_sync.py
```
Gestione stato USB
```bash

# Vedi stato sincronizzazione per ogni USB
cat /root/.usb_sync_state.json

# Resetta stato per una USB specifica
rm /root/.usb_sync_state.json

# Resetta USB target
rm /root/.target_usb.conf
```
Pulizia e manutenzione
```bash

# Pulisci file duplicati sulla USB
./clean_usb_duplicates.sh

# Rotazione log manuale
sudo logrotate -f /etc/logrotate.d/usb-music-sync

# Verifica spazio su disco
df -h /root/Musica
```
🐛 Troubleshooting
Errore: "Nessuna USB trovata"
```bash

# Verifica che la USB sia riconosciuta
lsblk
# Controlla se è formattata
sudo fdisk -l /dev/sda1
# Prova a montare manualmente
sudo mount /dev/sda1 /mnt/usb
```
Errore: "Permission denied"
```bash

# Lo script richiede root
sudo python3 usb_music_sync.py
# O aggiungi permessi allo script
chmod +x usb_music_sync.py
```
Errore: "Directory non esiste"
```bash

# Crea la directory della musica
mkdir -p /root/Musica
# O modifica SOURCE_DIR con il path corretto
```
Lo script non parte all'avvio
```bash

# Verifica stato servizio
sudo systemctl status usb-music-sync
# Ricarica systemd
sudo systemctl daemon-reload
# Riavvia il servizio
sudo systemctl restart usb-music-sync
```
Duplicati non vengono saltati
```bash

# Cancella stato e ricomincia
rm /root/.usb_sync_state.json
# La prossima volta copierà tutto (controllo per nome)
```
📁 Struttura File
text

/home/orangepi/projects/usb-music-sync/
├── usb_music_sync.py          # Script principale
├── usb-music-sync.service     # File servizio systemd
├── clean_usb_duplicates.sh    # Script pulizia duplicati
├── README.md                  # Documentazione
└── .gitignore                 # File ignorati da git

/root/
├── .usb_sync_state.json       # Stato sincronizzazione USB
└── .target_usb.conf           # USB target configurata

/var/log/
└── usb_music_sync.log         # Log delle operazioni

/etc/systemd/system/
└── usb-music-sync.service     # Servizio systemd


🔄 Aggiornamento
bash

cd /home/orangepi/projects/usb-music-sync
git pull
sudo systemctl restart usb-music-sync

Suggerimenti e miglioramenti sono benvenuti!

Autore: mancio8
Progetto: https://github.com/mancio8/usb-music-sync

