import os
import yaml
from jumpssh import SSHSession
from datetime import datetime


def create_list_active_devices():
    lista_equipos_activos = []
    try:
        with open("testbed.yaml","r") as file:
            yaml_to_dict = yaml.load(file)
            for nombre_equipo in yaml_to_dict["devices"]:
                #print(yaml_to_dict["devices"][nombre_equipo])
                ip_device = yaml_to_dict["devices"][nombre_equipo]["connections"]["cli"]["ip"]
                password_device = yaml_to_dict["devices"][nombre_equipo]["credentials"]["default"]["password"]
                username_device = yaml_to_dict["devices"][nombre_equipo]["credentials"]["default"]["username"]
                try:
                    #print("conectandose a "+ip_device)
                    gateway_session = SSHSession(ip_device,username=username_device,password=password_device).open()
                    gateway_session.close()
                    lista_equipos_activos.append(nombre_equipo)
                except Exception as e:
                    print(e)
            print(lista_equipos_activos)
            return(lista_equipos_activos)
    except Exception as e:
        print(e)

