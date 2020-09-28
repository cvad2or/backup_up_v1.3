import os
import yaml
from datetime import datetime

def compare_state(filenames):
    try:
        filenames = filenames.split(",")
        carpeta_diff = "compare_result_"+datetime.now().strftime("%d%m%Y_%H%M")
        os.system("pyats diff  "+filenames[1].strip('"')+"  "+filenames[0].strip('"')+" --output "+carpeta_diff)
        return("comparacion realizada "+ carpeta_diff)
    except Exception as e:
        print(e)