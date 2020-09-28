import os

def create_testbed(filename):
    try:
        print(".......1..........")
        print(os.getcwd())
        os.system("pyats create testbed file --path="+filename+" --output testbed.yaml")
        return("testbed.yaml creado")
    except Exception as e:
        print(e)





