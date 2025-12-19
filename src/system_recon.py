#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kodlayan: @akçay

import os
import sys
import time
import platform
import subprocess
import socket
import threading
from datetime import datetime
import psutil
from concurrent.futures import ThreadPoolExecutor
import json
import ipaddress

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

class ASCIIArt:
    TITLE = f"""
    {Colors.CYAN}
 __   __               
 \ \ / /_ _  __ _ ____ 
  \ V / _` |/ _` |_  / 
   | | (_| | (_| |/ /  
   |_|\__,_|\__,_/___|  
    {Colors.RESET}
            """
    
    SUCCESS = f"{Colors.GREEN}✓{Colors.RESET}"
    FAIL = f"{Colors.RED}✗{Colors.RESET}"
    INFO = f"{Colors.BLUE}ℹ{Colors.RESET}"
    WARNING = f"{Colors.YELLOW}⚠{Colors.RESET}"

class Sistem:
    @staticmethod
    def get_title():
        sistem = platform.system()

        if sistem == "Windows":
            return rf"""
            {Colors.BLUE}
 __        ___           _                   
 \ \      / (_)_ __   __| | _____      _____ 
  \ \ /\ / /| | '_ \ / _` |/ _ \ \ /\ / / __|
   \ V  V / | | | | | (_| | (_) \ V  V /\__ \
    \_/\_/  |_|_| |_|\__,_|\___/ \_/\_/ |___/ 
            {Colors.RESET}
                    """

        elif sistem == "Linux":
            return rf"""
            {Colors.PURPLE}
 _     _                  
| |   (_)_ __  _   ___  __
| |   | | '_ \| | | \ \/ /
| |___| | | | | |_| |>  < 
|_____|_|_| |_|\__,_/_/\_\
            {Colors.RESET}
                    """

        elif sistem == "Darwin":
            return rf"""
            {Colors.WHITE}
  __  __             ___      
 |  \/  | __ _  ___ / _ \ ___ 
 | |\/| |/ _` |/ __| | | / __|
 | |  | | (_| | (__| |_| \__ \
 |_|  |_|\__,_|\___|\___/|___|  
            {Colors.RESET}
                    """

        else:
            return "[!] İşletim Sistemi Algılanamadı"

class SystemRecon:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.results = {}
        self.start_time = datetime.now()
        
    def check_dependencies(self):
        required_packages = ['psutil', 'requests']
        missing_packages = []
        
        print(f"{Colors.YELLOW}[*] Gerekli kütüphaneler kontrol ediliyor...{Colors.RESET}")
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  {ASCIIArt.SUCCESS} {package} yüklü")
            except ImportError:
                print(f"  {ASCIIArt.FAIL} {package} bulunamadı")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"{Colors.YELLOW}[*] Eksik kütüphaneler yükleniyor...{Colors.RESET}")
            for package in missing_packages:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"  {ASCIIArt.SUCCESS} {package} başarıyla yüklendi")
                except subprocess.CalledProcessError:
                    print(f"  {ASCIIArt.FAIL} {package} yüklenirken hata oluştu")
                    return False

        try:
            import netifaces
            print(f"  {ASCIIArt.SUCCESS} netifaces yüklü")
        except ImportError:
            print(f"  {ASCIIArt.WARNING} netifaces yüklenemedi!")
        
        return True
    
    def animate_text(self, text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def print_section(self, title):
        print(f"\n{Colors.PURPLE}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{title.center(80)}{Colors.RESET}")
        print(f"{Colors.PURPLE}{'='*80}{Colors.RESET}\n")
    
    def get_network_interfaces(self):
        interfaces_info = []
        
        try:
            try:
                import netifaces
                interfaces = netifaces.interfaces()
                for interface in interfaces:
                    addrs = netifaces.ifaddresses(interface)
                    interface_info = {'name': interface, 'ipv4': [], 'mac': ''}
                    
                    if netifaces.AF_INET in addrs:
                        for addr in addrs[netifaces.AF_INET]:
                            interface_info['ipv4'].append({
                                'ip': addr.get('addr', 'N/A'),
                                'netmask': addr.get('netmask', 'N/A'),
                                'broadcast': addr.get('broadcast', 'N/A')
                            })
                    
                    if netifaces.AF_LINK in addrs:
                        for addr in addrs[netifaces.AF_LINK]:
                            interface_info['mac'] = addr.get('addr', 'N/A')
                    
                    interfaces_info.append(interface_info)
                return interfaces_info
            except ImportError:
                pass

            net_io = psutil.net_if_addrs()
            for interface, addrs in net_io.items():
                interface_info = {'name': interface, 'ipv4': [], 'mac': ''}
                
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # IPv4
                        interface_info['ipv4'].append({
                            'ip': addr.address,
                            'netmask': addr.netmask,
                            'broadcast': addr.broadcast
                        })
                    elif addr.family == psutil.AF_LINK:  # MAC
                        interface_info['mac'] = addr.address
                
                interfaces_info.append(interface_info)
            
            return interfaces_info
            
        except Exception as e:
            print(f"{Colors.RED}Ağ arayüzleri alınırken hata: {e}{Colors.RESET}")
            return interfaces_info
    
    def get_system_info(self):
        self.print_section("SİSTEM BİLGİLERİ")
        
        try:
            system_info = {
                "Sistem": platform.system(),
                "Sürüm": platform.version(),
                "Mimari": platform.architecture()[0],
                "İşlemci": platform.processor(),
                "Hostname": socket.gethostname(),
                "Kullanıcı": os.getenv('USERNAME') or os.getenv('USER') or "Bilinmiyor"
            }
            
            for key, value in system_info.items():
                print(f"{Colors.GREEN}{key:<15}: {Colors.WHITE}{value}{Colors.RESET}")
                time.sleep(0.1)

            memory = psutil.virtual_memory()
            print(f"\n{Colors.GREEN}Bellek Bilgisi:{Colors.RESET}")
            print(f"  {Colors.YELLOW}Toplam:{Colors.RESET} {memory.total // (1024**3)} GB")
            print(f"  {Colors.YELLOW}Kullanılan:{Colors.RESET} {memory.used // (1024**3)} GB")
            print(f"  {Colors.YELLOW}Boş:{Colors.RESET} {memory.available // (1024**3)} GB")
            print(f"  {Colors.YELLOW}Kullanım Oranı:{Colors.RESET} {memory.percent}%")

            print(f"\n{Colors.GREEN}Disk Bilgisi:{Colors.RESET}")
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    print(f"  {Colors.YELLOW}{partition.device} ({partition.fstype}):{Colors.RESET}")
                    print(f"    Bağlama Noktası: {partition.mountpoint}")
                    print(f"    Toplam: {usage.total // (1024**3)} GB")
                    print(f"    Kullanılan: {usage.used // (1024**3)} GB")
                    print(f"    Boş: {usage.free // (1024**3)} GB")
                    print(f"    Kullanım: {usage.percent}%")
                except (PermissionError, OSError):
                    continue
            
            self.results['system_info'] = system_info
            
        except Exception as e:
            print(f"{Colors.RED}Sistem bilgisi alınırken hata: {e}{Colors.RESET}")
    
    def get_network_info(self):
        self.print_section("AĞ BİLGİLERİ")
        
        try:
            interfaces = self.get_network_interfaces()
            print(f"{Colors.GREEN}Ağ Arayüzleri:{Colors.RESET}")
            
            for interface in interfaces:
                print(f"\n  {Colors.YELLOW}{interface['name']}:{Colors.RESET}")
                
                if interface['mac']:
                    print(f"    MAC: {interface['mac']}")
                
                for ip_info in interface['ipv4']:
                    print(f"    IP: {ip_info['ip']}")
                    if ip_info['netmask'] != 'N/A':
                        print(f"    Alt Ağ Maskesi: {ip_info['netmask']}")
                    if ip_info['broadcast'] != 'N/A':
                        print(f"    Yayın Adresi: {ip_info['broadcast']}")

            print(f"\n{Colors.GREEN}Aktif Bağlantılar:{Colors.RESET}")
            try:
                connections = psutil.net_connections()
                established_count = 0
                
                for conn in connections[:15]:
                    if conn.status == 'ESTABLISHED' and conn.laddr:
                        established_count += 1
                        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'N/A'
                        print(f"  {conn.laddr.ip}:{conn.laddr.port} -> {raddr} ({conn.status})")
                
                print(f"\n  {Colors.YELLOW}Toplam kurulu bağlantı: {established_count}{Colors.RESET}")
                
            except (psutil.AccessDenied, PermissionError):
                print(f"  {Colors.RED}Bağlantı bilgilerine erişim reddedildi{Colors.RESET}")
            
            self.results['network_info'] = {
                'interfaces': [iface['name'] for iface in interfaces],
                'connections': len(connections) if 'connections' in locals() else 0
            }
            
        except Exception as e:
            print(f"{Colors.RED}Ağ bilgisi alınırken hata: {e}{Colors.RESET}")
    
    def scan_ports(self, target_ip="127.0.0.1", ports_range=(1, 100)):
        self.print_section("PORT TARAMASI")
        
        print(f"{Colors.YELLOW}[*] {target_ip} üzerinde port taraması başlatılıyor ({ports_range[0]}-{ports_range[1]})...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Bu işlem birkaç dakika sürebilir...{Colors.RESET}")
        
        open_ports = []
        
        def scan_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.5)
                    result = sock.connect_ex((target_ip, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "bilinmeyen"
                        
                        open_ports.append((port, service))
                        print(f"  {ASCIIArt.SUCCESS} Port {port:5} açık ({service})")
            except:
                pass

        total_ports = ports_range[1] - ports_range[0] + 1
        completed = 0

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(scan_port, port): port for port in range(ports_range[0], ports_range[1] + 1)}
            
            for future in futures:
                future.result()
                completed += 1
                if completed % 20 == 0:
                    progress = (completed / total_ports) * 100
                    print(f"{Colors.BLUE}[{completed}/{total_ports}] %{progress:.1f} tamamlandı...{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}Tarama tamamlandı! {len(open_ports)} açık port bulundu.{Colors.RESET}")
        self.results['open_ports'] = open_ports
    
    def network_discovery(self):
        self.print_section("AĞ KEŞFİ")
        
        try:
            local_ip = None
            interfaces = self.get_network_interfaces()
            
            for interface in interfaces:
                for ip_info in interface['ipv4']:
                    ip = ip_info['ip']
                    if ip != '127.0.0.1' and not ip.startswith('169.254.'):
                        try:
                            ip_obj = ipaddress.IPv4Address(ip)
                            if ip_obj.is_private:
                                local_ip = ip
                                break
                        except:
                            continue
                if local_ip:
                    break
            
            if not local_ip:
                print(f"{Colors.RED}Yerel IP adresi bulunamadı.{Colors.RESET}")
                return
            
            print(f"{Colors.YELLOW}[*] Yerel ağ taraması başlatılıyor ({local_ip})...{Colors.RESET}")

            network_prefix = '.'.join(local_ip.split('.')[:-1])
            discovered_devices = []
            
            def ping_host(host_ip):
                try:
                    param = "-n" if self.os_type == "windows" else "-c"
                    timeout = "-w" if self.os_type == "windows" else "-W"
                    
                    result = subprocess.run(
                        ["ping", param, "1", timeout, "1000", host_ip],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        try:
                            hostname = socket.gethostbyaddr(host_ip)[0]
                        except:
                            hostname = "bilinmiyor"
                        
                        discovered_devices.append((host_ip, hostname))
                        print(f"  {ASCIIArt.SUCCESS} {host_ip:15} ({hostname})")
                except (subprocess.TimeoutExpired, Exception):
                    pass
            
            print(f"{Colors.YELLOW}[*] Ağdaki cihazlar taranıyor...{Colors.RESET}")

            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = []
                for i in range(1, 50):
                    host_ip = f"{network_prefix}.{i}"
                    futures.append(executor.submit(ping_host, host_ip))

                for future in futures:
                    future.result()
            
            print(f"\n{Colors.GREEN}Keşif tamamlandı! {len(discovered_devices)} cihaz bulundu.{Colors.RESET}")
            self.results['discovered_devices'] = discovered_devices
            
        except Exception as e:
            print(f"{Colors.RED}Ağ keşfi sırasında hata: {e}{Colors.RESET}")
    
    def get_running_processes(self):
        self.print_section("ÇALIŞAN PROSESLER")
        
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            print(f"{Colors.GREEN}Top 10 CPU Kullanan Prosesler:{Colors.RESET}")
            print(f"{'PID':<8} {'İsim':<25} {'Kullanıcı':<15} {'CPU%':<8} {'Bellek%':<10}")
            print(f"{'-'*70}")
            
            for proc in processes[:10]:
                pid = proc['pid']
                name = proc['name'][:24] if proc['name'] else 'N/A'
                username = proc['username'][:14] if proc['username'] else 'N/A'
                cpu = proc['cpu_percent'] or 0
                memory = proc['memory_percent'] or 0
                
                print(f"{Colors.YELLOW}{pid:<8}{Colors.RESET} {name:<25} {username:<15} {cpu:<8.2f} {memory:<10.2f}")
            
            self.results['process_count'] = len(processes)
            
        except Exception as e:
            print(f"{Colors.RED}Proses bilgisi alınırken hata: {e}{Colors.RESET}")
    
    def get_hardware_info(self):
        self.print_section("DONANIM BİLGİLERİ")
        
        try:
            print(f"{Colors.GREEN}İşlemci:{Colors.RESET}")
            print(f"  {Colors.YELLOW}Çekirdek:{Colors.RESET} {psutil.cpu_count(logical=False)} fiziksel, {psutil.cpu_count(logical=True)} mantıksal")
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"  {Colors.YELLOW}Kullanım:{Colors.RESET} {cpu_percent}%")
            
            try:
                cpu_freq = psutil.cpu_freq()
                if cpu_freq:
                    print(f"  {Colors.YELLOW}Frekanz:{Colors.RESET} {cpu_freq.current:.2f} MHz")
            except AttributeError:
                print(f"  {Colors.YELLOW}Frekanz:{Colors.RESET} Bilinmiyor")

            print(f"\n{Colors.GREEN}Disk İstatistikleri:{Colors.RESET}")
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    print(f"  {Colors.YELLOW}Okunan:{Colors.RESET} {disk_io.read_bytes // (1024**2)} MB")
                    print(f"  {Colors.YELLOW}Yazılan:{Colors.RESET} {disk_io.write_bytes // (1024**2)} MB")
            except AttributeError:
                print(f"  {Colors.YELLOW}Disk IO:{Colors.RESET} Bilinmiyor")

            print(f"\n{Colors.GREEN}Ağ İstatistikleri:{Colors.RESET}")
            try:
                net_io = psutil.net_io_counters()
                if net_io:
                    print(f"  {Colors.YELLOW}Gönderilen:{Colors.RESET} {net_io.bytes_sent // (1024**2)} MB")
                    print(f"  {Colors.YELLOW}Alınan:{Colors.RESET} {net_io.bytes_recv // (1024**2)} MB")
            except AttributeError:
                print(f"  {Colors.YELLOW}Ağ IO:{Colors.RESET} Bilinmiyor")

            try:
                battery = psutil.sensors_battery()
                if battery:
                    print(f"\n{Colors.GREEN}Pil Durumu:{Colors.RESET}")
                    print(f"  {Colors.YELLOW}Şarj:{Colors.RESET} {battery.percent}%")
                    print(f"  {Colors.YELLOW}Fişe Takılı:{Colors.RESET} {'Evet' if battery.power_plugged else 'Hayır'}")
            except AttributeError:
                pass
            
            self.results['hardware_info'] = {
                'cpu_cores': psutil.cpu_count(logical=True),
                'cpu_usage': cpu_percent,
                'memory_usage': psutil.virtual_memory().percent
            }
            
        except Exception as e:
            print(f"{Colors.RED}Donanım bilgisi alınırken hata: {e}{Colors.RESET}")
    
    def save_results(self):
        self.print_section("RAPOR OLUŞTURMA")
        
        filename = f"system_recon_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json_results = {}
                for key, value in self.results.items():
                    if isinstance(value, (dict, list, str, int, float, bool, type(None))):
                        json_results[key] = value
                    else:
                        json_results[key] = str(value)
                
                json.dump(json_results, f, indent=2, ensure_ascii=False)
            
            print(f"{Colors.GREEN}[+] Sonuçlar '{filename}' dosyasına kaydedildi.{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}[-] Sonuçlar kaydedilirken hata oluştu: {e}{Colors.RESET}")
    
    def display_summary(self):
        self.print_section("ÖZET RAPOR")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print(f"{Colors.GREEN}Tarama Süresi:{Colors.RESET} {duration.total_seconds():.2f} saniye")
        print(f"{Colors.GREEN}Başlangıç Zamanı:{Colors.RESET} {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.GREEN}Bitiş Zamanı:{Colors.RESET} {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if 'system_info' in self.results:
            print(f"{Colors.GREEN}Sistem:{Colors.RESET} {self.results['system_info'].get('Sistem', 'Bilinmiyor')}")
        
        if 'open_ports' in self.results:
            print(f"{Colors.GREEN}Açık Portlar:{Colors.RESET} {len(self.results['open_ports'])}")
        
        if 'discovered_devices' in self.results:
            print(f"{Colors.GREEN}Keşfedilen Cihazlar:{Colors.RESET} {len(self.results['discovered_devices'])}")
        
        if 'process_count' in self.results:
            print(f"{Colors.GREEN}Toplam Proses:{Colors.RESET} {self.results['process_count']}")
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[!] Sistem analizi tamamlandı!{Colors.RESET}")
    
    def run(self):
        try:
            print(ASCIIArt.TITLE)
            self.animate_text(f"{Colors.CYAN}{Colors.BOLD}Sistem Recon Tool'u başlatılıyor...{Colors.RESET}")
            time.sleep(1)

            if not self.check_dependencies():
                print(f"{Colors.RED}[-] Gerekli kütüphaneler yüklenemedi. Lütfen manuel olarak yükleyin.{Colors.RESET}")
                return
            
            time.sleep(1)

            analyses = [
                self.get_system_info,
                self.get_network_info,
                self.get_hardware_info,
                self.get_running_processes,
                self.scan_ports,
                self.network_discovery
            ]
            
            for analysis in analyses:
                try:
                    analysis()
                    time.sleep(1)
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}[!] Analiz kullanıcı tarafından durduruldu.{Colors.RESET}")
                    break
                except Exception as e:
                    print(f"{Colors.RED}[-] Analiz sırasında hata: {e}{Colors.RESET}")
                    continue

            self.display_summary()
            self.save_results()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Program kullanıcı tarafından durduruldu.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[-] Beklenmeyen hata: {e}{Colors.RESET}")

def main():
    ASCIIArt.TITLE = Sistem.get_title()
    if os.name != 'nt' and os.geteuid() != 0:
        print(f"{Colors.YELLOW}[!] Bazı özellikler için SUDO yetkisi gerekebilir.{Colors.RESET}")

    recon = SystemRecon()
    recon.run()

if __name__ == "__main__":
    main()