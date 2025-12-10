import socket
import psutil
from jinja2 import Environment, FileSystemLoader

# Adresse IP

def ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"
print("Adresse IP :", ip_address())


data = {
    "ip_address": ip_address()
}


env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')
rendered_html = template.render(data)


with open("template.html", "w", encoding="utf-8") as f:
    f.write(rendered_html)


print("Dashboard généré ✅")



# Nombre de coeurs CPU 

def cpu_cores():

    total_cores = psutil.cpu_count(logical=True)
    physical_cores = psutil.cpu_count(logical=False)

    print("Coeurs logiques : ", total_cores)
    print("Coeurs physiques : ", physical_cores)

print(cpu_cores())



