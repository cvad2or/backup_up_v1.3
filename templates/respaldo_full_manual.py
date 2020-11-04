from netmiko import ConnectHandler
import os
from datetime import datetime
import json
from jumpssh import SSHSession
from telnetlib import Telnet

commands_asa = [
    'exit',
    'show interface ip brief',
    'show running',
    ]

commands_iosxe = [
    'show ip interface brief',
    'show running',
    ]

commands_nxos = [
    'show ip interface brief',
    'show running',
    ]

commands_junos = [
    'show configuration',
    'show vlan'
    ]

def respaldo_qqq_ssh():
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
            else:
                print("otro equipo")

def respaldo_ssh(hostname,ip,cisco_os,username,password,enable_password):

    try:
        ruta = os.getcwd()
        with open(ruta+"/full backup manual/respaldo_"+hostname+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
            if cisco_os=="nxos":
                ssh_session = SSHSession(ip, username, password=password).open()
                for comando in commands_nxos:
                    resultado = ssh_session.run_cmd(comando)
                    file.write(resultado.output)
                ssh_session.close()
            elif cisco_os=="iosxe":
                ssh_session = SSHSession(ip, username, password=password).open()
                for comando in commands_iosxe:
                    resultado = ssh_session.run_cmd(comando)
                    file.write(resultado.output)
                ssh_session.close()
            elif cisco_os=="junos":
                ssh_session = SSHSession(ip, username, password=password,timeout=10).open()
                for comando in commands_junos:
                    resultado = ssh_session.run_cmd(comando)
                    file.write(resultado.output)
                ssh_session.close()


    except Exception as e:
            print(e)
            return("fallido")


    return("realizado")

"""    if cisco_os=="nxos":
        equipo = {
        'device_type': "cisco_nxos",
        'ip':ip,
        'username': username,
        'password': password,
        'secret': enable_password,
        'verbose': False,
        }
        try:
            ruta = os.getcwd()
            net_connect = ConnectHandler(**equipo)
            print(equipo)

            net_connect.enable()
            resultado = net_connect.send_config_set(commands_nxos)
            print(resultado)
            with open(ruta+"/full backup manual/respaldo_"+hostname+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
                file.write(resultado)
            print("..........respaldo realizado.."+hostname)
            net_connect.disconnect()
        except Exception as e:
            print(e)

    elif cisco_os=="ioxe":
        equipo = {
        'device_type': "cisco_iosxe",
        'ip':ip,
        'username': username,
        'password': password,
        'secret': enable_password,
        'verbose': False,
        }
        try:
            ruta = os.getcwd()
            net_connect = ConnectHandler(**equipo)
            print(equipo)

            net_connect.enable()
            resultado = net_connect.send_config_set(commands_iosxe)
            print(resultado)
            with open(ruta+"/full backup manual/respaldo_"+hostname+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
                file.write(resultado)
            net_connect.disconnect()
            if equipo["device_type"]=="asa":
                resultado = net_connect.send_config_set(commands_asa)
                print(resultado)
                with open(ruta+"/full backup scheduled/respaldo_"+hostname+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
                    file.write(resultado)

            return
        except Exception as e:
            print(e)

    return("realizado")

"""
def respaldo_telnet(hostname,ip,cisco_os,username,password,enable_password):
    try:
        ruta = os.getcwd()
        with open(ruta+"/full backup manual/respaldo_"+hostname+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
            if cisco_os=="nxos":
                print("....se conecta via telnet.."+hostname)
                tn = Telnet(ip)
                tn.read_all()
                tn.write(username.encode('utf-8'))
                tn.write(b"\r")
                tn.read_all()
                tn.write(password.encode('utf-8'))
                tn.write(b"\r")
                for comando in commands_nxos:
                    print("...."+comando+"......")
                    resultado = tn.write(comando + "\n")
                    file.write(tn.read_all())
                print (tn.read_all())
            elif cisco_os=="iosxe":
                print("....se conecta via telnet.."+hostname)
                tn = Telnet(ip)
                tn.read_until(b"Username: ")
                tn.write(b"alex")
                tn.read_until(b"Password: ")
                tn.write(b"alex")
                tn.read_until(b"#")


    except Exception as e:
            print(e)
            return(e)


    return("realizado")