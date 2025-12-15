import psutil
import time
import socket
import platform
import os
from pathlib import Path

# Configuration
path = '/home/tommy/dashboard_project'
ext = ('.txt', '.py', '.pdf', '.jpg')

def get_primary_ip():
    """Récupère l'adresse IP principale de la machine"""
    req = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        req.connect(("8.8.8.8", 80))
        return req.getsockname()[0]
    except Exception:
        return "N/A"
    finally:
        req.close()

def format_bytes(bytes_val):
    """Formate les bytes en unité lisible"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
              return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"

print("Dashboard lancé. Appuyez sur Ctrl+C pour arrêter.")

# Vérifier que template.html existe
if not os.path.exists("template.html"):
    print("ERREUR: Le fichier template.html n'existe pas!")
    exit(1)

iteration = 0

try:
    while True:
        iteration += 1
        
        # === SYSTEM INFO ===
        name = socket.gethostname()
        os_name = platform.system()
        
        boot_timestamp = psutil.boot_time()
        current_time = time.time()
        uptime = int(current_time - boot_timestamp)
        
        users = psutil.users()
        user_count = len(users)
        
        # === CPU INFO ===
        cpu_cores = psutil.cpu_count()
        
        clock_rate = psutil.cpu_freq()
        curr_cl = round(clock_rate.current, 2) if clock_rate else 0
        min_cl = round(clock_rate.min, 2) if clock_rate else 0
        max_cl = round(clock_rate.max, 2) if clock_rate else 0
        
        cpu_usage = round(psutil.cpu_percent(interval=0.1), 2)
        
        # === RAM INFO ===
        ram = psutil.virtual_memory()
        total_ram = format_bytes(ram.total)
        used_ram = format_bytes(ram.used)
        percent_ram = round(ram.percent, 2)
        
        # === NETWORK INFO ===
        ip_address = get_primary_ip()
        
        # === PROCESSES INFO ===
        processes = [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])]
        
        # Top 3 CPU
        top3_cpu = sorted(processes, key=lambda x: x['cpu_percent'] if x['cpu_percent'] else 0, reverse=True)[:3]
        
        # Top 3 RAM
        top3_ram = sorted(processes, key=lambda x: x['memory_percent'] if x['memory_percent'] else 0, reverse=True)[:3]
        
        # Top 3 Overall (CPU + RAM)
        top3 = sorted(processes, key=lambda x: (x['cpu_percent'] if x['cpu_percent'] else 0) + (x['memory_percent'] if x['memory_percent'] else 0), reverse=True)[:3]
        
        # === FOLDER ANALYSIS ===
        if os.path.exists(path):
            analyze = os.listdir(path)
            files_name = ', '.join(analyze[:10]) if analyze else 'No files'
            if len(analyze) > 10:
                files_name += f" ... ({len(analyze)} total)"
            total_files_count = len(analyze)
            directory_size = sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())
            
            files_with_set_ext = [f for f in os.listdir(path) if f.endswith(ext)]
            set_files_count = len(files_with_set_ext)
            files_with_set_ext_str = ', '.join(files_with_set_ext) if files_with_set_ext else 'None'
        else:
            files_name = "Path not found"
            total_files_count = 0
            directory_size = 0
            files_with_set_ext_str = "N/A"
            set_files_count = 0
        
        # Créer le dictionnaire de toutes les valeurs
        data = {
            'name': name,
            'os_name': os_name,
            'uptime': uptime,
            'user_count': user_count,
            'cpu_cores': cpu_cores,
            'curr_cl': curr_cl,
            'min_cl': min_cl,
            'max_cl': max_cl,
            'cpu_usage': cpu_usage,
            'total_ram': total_ram,
            'used_ram': used_ram,
            'percent_ram': percent_ram,
            'ip_address': ip_address,
            'cpu_pid1': top3_cpu[0]['pid'],
            'cpu_pid2': top3_cpu[1]['pid'],
            'cpu_pid3': top3_cpu[2]['pid'],
            'cpu_name1': top3_cpu[0]['name'],
            'cpu_name2': top3_cpu[1]['name'],
            'cpu_name3': top3_cpu[2]['name'],
            'cpu_memory1': round(top3_cpu[0]['memory_percent'], 2) if top3_cpu[0]['memory_percent'] else 0,
            'cpu_memory2': round(top3_cpu[1]['memory_percent'], 2) if top3_cpu[1]['memory_percent'] else 0,
            'cpu_memory3': round(top3_cpu[2]['memory_percent'], 2) if top3_cpu[2]['memory_percent'] else 0,
            'cpu_cpu1': round(top3_cpu[0]['cpu_percent'], 2) if top3_cpu[0]['cpu_percent'] else 0,
            'cpu_cpu2': round(top3_cpu[1]['cpu_percent'], 2) if top3_cpu[1]['cpu_percent'] else 0,
            'cpu_cpu3': round(top3_cpu[2]['cpu_percent'], 2) if top3_cpu[2]['cpu_percent'] else 0,
            'ram_pid1': top3_ram[0]['pid'],
            'ram_pid2': top3_ram[1]['pid'],
            'ram_pid3': top3_ram[2]['pid'],
            'ram_name1': top3_ram[0]['name'],
            'ram_name2': top3_ram[1]['name'],
            'ram_name3': top3_ram[2]['name'],
            'ram_memory1': round(top3_ram[0]['memory_percent'], 2) if top3_ram[0]['memory_percent'] else 0,
            'ram_memory2': round(top3_ram[1]['memory_percent'], 2) if top3_ram[1]['memory_percent'] else 0,
            'ram_memory3': round(top3_ram[2]['memory_percent'], 2) if top3_ram[2]['memory_percent'] else 0,
            'ram_cpu1': round(top3_ram[0]['cpu_percent'], 2) if top3_ram[0]['cpu_percent'] else 0,
            'ram_cpu2': round(top3_ram[1]['cpu_percent'], 2) if top3_ram[1]['cpu_percent'] else 0,
            'ram_cpu3': round(top3_ram[2]['cpu_percent'], 2) if top3_ram[2]['cpu_percent'] else 0,
            'top_pid1': top3[0]['pid'],
            'top_pid2': top3[1]['pid'],
            'top_pid3': top3[2]['pid'],
            'top_name1': top3[0]['name'],
            'top_name2': top3[1]['name'],
            'top_name3': top3[2]['name'],
            'top_memory1': round(top3[0]['memory_percent'], 2) if top3[0]['memory_percent'] else 0,
            'top_memory2': round(top3[1]['memory_percent'], 2) if top3[1]['memory_percent'] else 0,
            'top_memory3': round(top3[2]['memory_percent'], 2) if top3[2]['memory_percent'] else 0,
            'top_cpu1': round(top3[0]['cpu_percent'], 2) if top3[0]['cpu_percent'] else 0,
            'top_cpu2': round(top3[1]['cpu_percent'], 2) if top3[1]['cpu_percent'] else 0,
            'top_cpu3': round(top3[2]['cpu_percent'], 2) if top3[2]['cpu_percent'] else 0,
            'path': path,
            'files_name': files_name,
            'total_files_count': total_files_count,
            'directory_size': directory_size,
            'files_with_set_ext': files_with_set_ext_str,
            'set_files_count': set_files_count
        }
        
        # === LECTURE ET REMPLACEMENT ===
        with open("template.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        # Remplacement avec .format()
        html = html.format(**data)
        
        # Écriture du fichier
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"Dashboard mis à jour - {time.strftime('%H:%M:%S')}", end="\r")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nDashboard arrêté.")
except Exception as e:
    print(f"Erreur: {e}")