import psutil #components info
import time
import socket #machine info
import platform #os info
import folderstats
import os
from pathlib import Path


path = '/home/paragon/Desktop/projetAAA'
# path = input("Select a path to analyze: ")
ext = ('.txt', '.py', '.pdf', '.jpg')
files_with_set_ext = []

def get_primary_ip():
    req = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        req.connect(("8.8.8.8", 80))
        return req.getsockname()[0]
    finally:
        req.close()

while True:
    #sysinfo
    name = socket.gethostname()
    os_name = platform.system()

    boot_timestamp = psutil.boot_time()
    current_time = time.time()
    uptime = current_time - boot_timestamp 

    users = psutil.users()
    user_count = len(users)

    #CPU
    cores = psutil.cpu_count()

    clock_rate = psutil.cpu_freq()
    curr_cl = clock_rate.current
    min_cl = clock_rate.min
    max_cl = clock_rate.max

    cpu_percent = psutil.cpu_percent()
    #RAM
    ram = psutil.virtual_memory()
    total_ram = ram.total
    in_use = ram.used
    percent_ram = ram.percent
    #IP
    main_ip = get_primary_ip()
    #PROCESSES
    processes = [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])]
    top3_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:3]
    top3_ram = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:3]
    top3 = sorted(processes, key=lambda x: x['cpu_percent'] + x['memory_percent'], reverse=True)[:3]


    cpu_pid1 = top3_cpu[0]['pid']
    cpu_pid2 = top3_cpu[1]['pid']
    cpu_pid3 = top3_cpu[2]['pid']
    cpu_name1 = top3_cpu[0]['name']
    cpu_name2 = top3_cpu[1]['name']
    cpu_name3 = top3_cpu[2]['name']
    cpu_memory1 = top3_cpu[0]['memory_percent']
    cpu_memory2 = top3_cpu[1]['memory_percent']
    cpu_memory3 = top3_cpu[2]['memory_percent']
    cpu_cpu1 = top3_cpu[0]['cpu_percent']
    cpu_cpu2 = top3_cpu[1]['cpu_percent']
    cpu_cpu3 = top3_cpu[2]['cpu_percent']

    ram_pid1 = top3_ram[0]['pid']
    ram_pid2 = top3_ram[1]['pid']
    ram_pid3 = top3_ram[2]['pid']
    ram_name1 = top3_ram[0]['name']
    ram_name2 = top3_ram[1]['name']
    ram_name3 = top3_ram[2]['name']
    ram_memory1 = top3_ram[0]['memory_percent']
    ram_memory2 = top3_ram[1]['memory_percent']
    ram_memory3 = top3_ram[2]['memory_percent']
    ram_cpu1 = top3_ram[0]['cpu_percent']
    ram_cpu2 = top3_ram[1]['cpu_percent']
    ram_cpu3 = top3_ram[2]['cpu_percent']

    top_pid1 = top3[0]['pid']
    top_pid2 = top3[1]['pid']
    top_pid3 = top3[2]['pid']
    top_name1 = top3[0]['name']
    top_name2 = top3[1]['name']
    top_name3 = top3[2]['name']
    top_memory1 = top3[0]['memory_percent']
    top_memory2 = top3[1]['memory_percent']
    top_memory3 = top3[2]['memory_percent']
    top_cpu1 = top3[0]['cpu_percent']
    top_cpu2 = top3[1]['cpu_percent']
    top_cpu3 = top3[2]['cpu_percent']


    #analyze folder
    analyze = os.listdir(path)
    files_name = analyze
    total_files_count = len(analyze)
    directory_size = sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())

    for File in os.listdir(path):
        if File.endswith(ext):
            if File in files_with_set_ext:
                break
            else:
                files_with_set_ext.append(File)
                print(files_with_set_ext)
    set_files_count = len(files_with_set_ext)


    with open("main.html", "r") as f:
        html = f.read()

    html = html.replace("{{NAME}}", str(name))
    html = html.replace("{{OS_NAME}}", str(os_name))
    html = html.replace("{{UPTIME}}", str(uptime))
    html = html.replace("{{USER_COUNT}}", str(user_count))
    html = html.replace("{{CORES}}", str(cores))
    html = html.replace("{{CURR_CL}}", str(curr_cl))
    html = html.replace("{{MIN_CL}}", str(min_cl))
    html = html.replace("{{MAX_CL}}", str(max_cl))
    html = html.replace("{{CPU}}", str(cpu_percent))
    html = html.replace("{{TOTAL_RAM}}", str(total_ram))
    html = html.replace("{{IN_USE}}", str(in_use))
    html = html.replace("{{PERCENT_RAM}}", str(percent_ram))
    html = html.replace("{{MAIN_IP}}", str(main_ip))
#    html = html.replace("{{TOP3_CPU}}", str(top3_cpu))
#    html = html.replace("{{TOP3_RAM}}", str(top3_ram))
#    html = html.replace("{{TOP3}}", str(top3))
    html = html.replace("{{RAM_PID1}}", str(ram_pid1))
    html = html.replace("{{RAM_PID2}}", str(ram_pid2))
    html = html.replace("{{RAM_PID3}}", str(ram_pid3))
    html = html.replace("{{RAM_NAME1}}", str(ram_name1))
    html = html.replace("{{RAM_NAME2}}", str(ram_name2))
    html = html.replace("{{RAM_NAME3}}", str(ram_name3))
    html = html.replace("{{RAM_MEMORY1}}", str(ram_memory1))
    html = html.replace("{{RAM_MEMORY2}}", str(ram_memory2))
    html = html.replace("{{RAM_MEMORY3}}", str(ram_memory3))
    html = html.replace("{{RAM_CPU1}}", str(ram_cpu1))
    html = html.replace("{{RAM_CPU2}}", str(ram_cpu2))
    html = html.replace("{{RAM_CPU3}}", str(ram_cpu3))
    html = html.replace("{{CPU_PID1}}", str(cpu_pid1))
    html = html.replace("{{CPU_PID2}}", str(cpu_pid2))
    html = html.replace("{{CPU_PID3}}", str(cpu_pid3))
    html = html.replace("{{CPU_NAME1}}", str(cpu_name1))
    html = html.replace("{{CPU_NAME2}}", str(cpu_name2))
    html = html.replace("{{CPU_NAME3}}", str(cpu_name3))
    html = html.replace("{{CPU_MEMORY1}}", str(cpu_memory1))
    html = html.replace("{{CPU_MEMORY2}}", str(cpu_memory2))
    html = html.replace("{{CPU_MEMORY3}}", str(cpu_memory3))
    html = html.replace("{{CPU_CPU1}}", str(cpu_cpu1))
    html = html.replace("{{CPU_CPU2}}", str(cpu_cpu2))
    html = html.replace("{{CPU_CPU3}}", str(cpu_cpu3))
    html = html.replace("{{TOP_PID1}}", str(top_pid1))
    html = html.replace("{{TOP_PID2}}", str(top_pid2))
    html = html.replace("{{TOP_PID3}}", str(top_pid3))
    html = html.replace("{{TOP_NAME1}}", str(top_name1))
    html = html.replace("{{TOP_NAME2}}", str(top_name2))
    html = html.replace("{{TOP_NAME3}}", str(top_name3))
    html = html.replace("{{TOP_MEMORY1}}", str(top_memory1))
    html = html.replace("{{TOP_MEMORY2}}", str(top_memory2))
    html = html.replace("{{TOP_MEMORY3}}", str(top_memory3))
    html = html.replace("{{TOP_CPU1}}", str(top_cpu1))
    html = html.replace("{{TOP_CPU2}}", str(top_cpu2))
    html = html.replace("{{TOP_CPU3}}", str(top_cpu3))
    html = html.replace("{{FILES_NAME}}", str(files_name))
    html = html.replace("{{TOTAL_FILES_COUNT}}", str(total_files_count))
    html = html.replace("{{SET_FILES_COUNT}}", str(set_files_count))
    html = html.replace("{{DIRECTORY_SIZE}}", str(directory_size))
    html = html.replace("{{FILES_WITH_SET_EXT}}", str(files_with_set_ext))
    html = html.replace("{{PATH}}", str(path))


    with open("index.html", "w") as f:
        f.write(html)

    time.sleep(1)
