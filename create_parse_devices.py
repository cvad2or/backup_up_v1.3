
import os
from datetime import datetime

def parse_all_config(lista_equipos_activos):
    carpeta = "my_parsed_output_"+datetime.now().strftime("%d%m%Y_%H%M")
    for equipo in lista_equipos_activos:
        print("parsing ..............")
        #socketio.emit('to_state_backup', "generando estado de "+equipo)
        try:
            print(os.getcwd()+" parse dir....................")
            os.system("genie parse all --testbed-file testbed.yaml --devices " + equipo+ " --output "+carpeta)
            #socketio.emit('to_state_backup', "estado de "+equipo+" generado")
        except Exception as e:
            print(e)
            print("error...........................")
            return(e)
            #socketio.emit('to_state_backup', (str(e)))
    return("todo bien")


