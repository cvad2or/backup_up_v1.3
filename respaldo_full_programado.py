from netmiko import ConnectHandler
import os
from datetime import datetime
import json

commands_asa = [
    'exit',
    'show interface ip brief',
    'show running',
    ]

commands_iosxe = [
    'exit',
    'show ip interface brief',
    'show running',
    ]

commands_nxos = [
    'exit',
    'show ip interface brief',
    'show running',
    ]

commands_ios = [
    'exit',
    'show ip interface brief',
    'show running',
    ]

def respaldo_ssh():
    with open("devices.json") as file:
        device_json = json.load(file)
        for i in device_json["os"]:
            if device_json["os"][i] == "asa":
                equipo = {
                'device_type': 'cisco_asa',
                'ip':device_json["ip"][i],
                'username': device_json["username"][i],
                'password': device_json["password"][i],
                'secret': device_json["enable_password"][i],
                'verbose': True,
                }
                hostname = device_json["hostname"][i]
                commands = commands_asa
                conexion_netmiko(commands,equipo,hostname)
            elif device_json["os"][i] == "iosxe":
                equipo = {
                'device_type': 'cisco_xe',
                'ip':device_json["ip"][i],
                'username': device_json["username"][i],
                'password': device_json["password"][i],
                'secret': device_json["enable_password"][i],
                'verbose': True,
                'global_delay_factor': 1,
                }
                hostname = device_json["hostname"][i]
                commands = commands_iosxe
                conexion_netmiko(commands,equipo,hostname)
            elif device_json["os"][i] == "nxos":
                equipo = {
                'device_type': 'cisco_nxos',
                'ip':device_json["ip"][i],
                'username': device_json["username"][i],
                'password': device_json["password"][i],
                'secret': device_json["enable_password"][i],
                'verbose': True,
                'global_delay_factor': 1,
                }
                hostname = device_json["hostname"][i]
                commands = commands_nxos
                conexion_netmiko(commands,equipo,hostname)
            elif device_json["os"][i] == "ios":
                equipo = {
                'device_type': 'cisco_ios',
                'ip':device_json["ip"][i],
                'username': device_json["username"][i],
                'password': device_json["password"][i],
                'secret': device_json["enable_password"][i],
                'verbose': True,
                'global_delay_factor': 1,
                }
                hostname = str(device_json["hostname"][i])
                commands = commands_ios
                conexion_netmiko(commands,equipo,hostname)
            else:
                print("otro equipo")

def conexion_netmiko(commands,equipo,hostname):
    try:
        ruta = os.getcwd()
        net_connect = ConnectHandler(**equipo)
        #print(equipo)  
        if equipo["device_type"]!="cisco_asa" or equipo["device_type"]!="cisco_ios":
            net_connect.enable()
        resultado = net_connect.send_config_set(commands)
        #print(resultado)
        with open(ruta+"/full backup scheduled/respaldo_"+hostname+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
            file.write(resultado)
    except Exception as e:
        print(e)
          


