project:
  name: System Recon Tool
  description_tr: >
    Python ile geliştirilmiş gelişmiş sistem ve ağ keşif (reconnaissance) aracıdır.
    Eğitim, sistem analizi ve yetkili güvenlik testleri için tasarlanmıştır.
  description_en: >
    An advanced system and network reconnaissance tool written in Python.
    Designed for education, system analysis and authorized security testing.

stages_tr:
  - stage: Banner
    image: images/banner.png

  - stage: Ozellikler
    items:
      - Sistem bilgileri (OS, CPU, RAM, Disk)
      - Ağ arayüzleri ve IP analizi
      - Açık port taraması
      - Yerel ağ cihaz keşfi
      - Çalışan proses analizi
      - Donanım istatistikleri
      - JSON rapor çıktısı
      - Renkli terminal arayüzü

  - stage: Kurulum
    commands:
      - git clone https://github.com/KULLANICI_ADIN/system-recon.git
      - cd system-recon
      - pip install -r requirements.txt

  - stage: Kullanim
    command: sudo python3 src/system_recon.py
    note: >
      Bazı özellikler için sudo / yönetici yetkisi gerekebilir.

  - stage: Ekran_Goruntuleri
    images:
      - images/system_info.png
      - images/network_scan.png
      - images/summary.png

  - stage: Cikti
    file_format: system_recon_YYYYMMDD_HHMMSS.json
    description: >
      Sistem, ağ, port ve proses bilgilerini içerir.

  - stage: Yasal_Uyari
    text: >
      Bu araç yalnızca eğitim ve yetkili test ortamlarında kullanılmalıdır.
      İzinsiz kullanım tamamen kullanıcı sorumluluğundadır.

stages_en:
  - stage: Banner
    image: images/banner.png

  - stage: Features
    items:
      - System information gathering (OS, CPU, RAM, Disk)
      - Network interface and IP analysis
      - Open port scanning
      - Local network discovery
      - Running process inspection
      - Hardware statistics
      - JSON report output
      - Colorful terminal interface

  - stage: Installation
    commands:
      - git clone https://github.com/USERNAME/system-recon.git
      - cd system-recon
      - pip install -r requirements.txt

  - stage: Usage
    command: sudo python3 src/system_recon.py
    note: >
      Some features require root / administrator privileges.

  - stage: Screenshots
    images:
      - images/system_info.png
      - images/network_scan.png
      - images/summary.png

  - stage: Output
    file_format: system_recon_YYYYMMDD_HHMMSS.json
    description: >
      Contains system, network, port and process information.

  - stage: Disclaimer
    text: >
      This tool is intended for educational purposes and authorized testing only.
      The author is not responsible for misuse.
