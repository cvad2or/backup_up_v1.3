from netmiko import ConnectHandler
import os
from datetime import datetime
import json
from jumpssh import SSHSession
from telnetlib import Telnet

commands_asa = [
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

commands_ios = [
    'show ip int brief',
    'show configuration',
    'show vlans'
    ]





def respaldo_ssh_manual(hostname,ip,cisco_os,username,password,enable_password):
    try:
        ruta = os.getcwd()
        with open(ruta+"/full backup manual/respaldo_"+hostname+"_"+datetime.now().strftime("%d%m%Y_%H%M"),"w") as file:
            if cisco_os=="nxos":
                nx_node = {
                    'device_type': 'cisco_nxos',
                    'ip': ip,
                    'username': username,
                    'password': password,
                    'secret': enable_password,
                    'port': 22,
                    }
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
            elif cisco_os=="ios":
                ios_node = {
                    'device_type': 'cisco_ios',
                    'ip': ip,
                    'username': username,
                    'password': password,
                    'secret': enable_password,
                    'port': 22,
                    }
                net_connect_ios = ConnectHandler(**ios_node)
                net_connect_ios.enable()
                for comando in commands_ios:
                    resultado = net_connect_ios.send_command(comando,strip_prompt=False, strip_command=False)
                    file.write(resultado)
            elif cisco_os=="asa":
                asa_node = {
                    'device_type': 'cisco_asa',
                    'ip': ip,
                    'username': username,
                    'password': password,
                    'secret': enable_password,
                    'port': 22,
                    }
                net_connect_asa = ConnectHandler(**asa_node)
                net_connect_asa.enable()
                for comando in commands_asa:
                    resultado = net_connect_asa.send_command(comando)
                    file.write(resultado)
        return ({"resultado":"equipo "+hostname+" OK"})

    except Exception as e:
            return("Error "+str(e))


    return("realizado")


def respaldo_telnet_manual(hostname,ip,cisco_os,username,password,enable_password):
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