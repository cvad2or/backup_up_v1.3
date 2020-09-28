from netmiko import ConnectHandler
import os
from datetime import datetime

def connect_asa_ssh(name,ip,protocol,username,password,enable):

    cisco_asa = {
    'device_type': 'cisco_asa',
    'ip':ip,
    'username': username,
    'password': password,
    'secret': enable,
    'verbose': False,
    }

#Listado de Comandos a ejecutar
    commands = [
    'exit',    
    'show interface ip brief',
    'show running',
    ]



    try:
        net_connect = ConnectHandler(**cisco_asa)
        net_connect.enable()
        print("respaldando ASA")
        ruta = os.getcwd()
        resultado = net_connect.send_config_set(commands)
        with open(ruta+"/full backup manual/respaldo_"+name+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
            file.write(resultado)
            return ({"resultado":"equipo "+name+" OK"})
    except Exception as e:
        return("Error "+str(e))