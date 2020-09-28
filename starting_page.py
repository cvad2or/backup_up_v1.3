from flask import Flask,render_template,jsonify,request,redirect,send_from_directory,url_for
import json
from respaldo_full_asa import connect_asa_ssh
from respaldo_full_nxos import connect_nxos_ssh
from respaldo_full_iosxe import connect_iosxe_ssh
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO,emit
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pandas
from respaldo_full_programado import respaldo_ssh
from create_parse_devices import parse_all_config
from compare_two_state import compare_state
from create_list_active_devices import create_list_active_devices
from create_testbed import create_testbed
import urllib3
from flask_bootstrap import Bootstrap
from requests.auth import HTTPBasicAuth
from fmc_change_policy import fmc_login,get_files_assignment,get_ips_assignment,get_policy_assignment
from fmc_change_policy import get_policy_assignment_with_names,get_rules_assignment,get_rules_with_names_assignment
from fmc_change_policy import get_variable_assignment,modify_all_rules,modify_some_rules

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]="/Desktop/flask/"
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,logger=True)

scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.add_jobstore('sqlalchemy', url='sqlite:///schedule.db')
scheduler.start()

user_fmc = ""
passwd_fmc = ""
ip_fmc =""

@socketio.on('from_js')
def handle_my_custom_event(text, methods=['GET', 'POST']):
    print('received my event: ' + text)
    socketio.emit("to_js","Se conecto al servidor.....")

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/trabajo/<trabajo>', methods=["GET"])
def schedule_to_delete(trabajo):
        scheduler.remove_job(trabajo)
        print("trabajo "+trabajo+" eliminado")
        all_jobs = scheduler.get_jobs()
        return redirect("/full_program_Backup")


@app.route('/')
def start():
    return render_template("starting_page.html")


@app.route('/full_backup')
def full_backup():
    return render_template('full_backup.html')


@app.route('/respaldo_full_programado')
def program_ull_backup():
    return redirect('full_program_Backup')


@app.route('/full_program_Backup',methods=["GET","POST"])
def full_program_Backup():
    if request.method == "POST":
        f = request.files["file"]
        f.save('devices.xlsx')
        excel_data_fragment = pandas.read_excel('devices.xlsx', sheet_name='Sheet1')
        json_str = excel_data_fragment.to_json()
        with open("devices.json","w") as file:
            file.write(json_str)
        data_numero = request.form["quantity"]
        data_frecuencia = request.form["frecuencia"]
        if data_frecuencia=="minuto":
            job = scheduler.add_job(respaldo_ssh, "interval",minutes=int(data_numero))
        elif data_frecuencia=="hora":
            job = scheduler.add_job(respaldo_ssh, "interval",hours=int(data_numero))
        elif data_frecuencia=="dia":
            job = scheduler.add_job(respaldo_ssh, "interval",days=int(data_numero))
        all_jobs = scheduler.get_jobs()
        return redirect("full_program_Backup")
    if request.method == "GET":
        #scheduler.remove_all_jobs()
        all_jobs = scheduler.get_jobs()
        return render_template("respaldo_full_programado.html",respuesta=all_jobs)


@app.route('/fullBackup')
def fullBackup():
    hostname=request.args.get("hostname")
    ip = request.args.get("ip")
    os = request.args.get("os")
    protocol = request.args.get("protocol")
    username= request.args.get("username")
    password= request.args.get("password")
    enable = request.args.get("enable_password")
    platform = request.args.get("platform")

    if os == "nxos" and protocol == "ssh":
        resultado = connect_nxos_ssh(hostname,ip,protocol,username,password,enable)
        socketio.emit("to_js","Respaldando equipo "+hostname+" con IP "+ip+" <br>")
        if "Error" in resultado:
            socketio.emit("to_js","Respaldo de "+hostname+" con IP "+ip+" fallo</font>")
            return jsonify(resultado)
        else:
            socketio.emit("to_js","Respaldo de "+hostname+" con IP "+ip+" se ejecuto!</font>")
            return jsonify(resultado)
        return jsonify(resultado)
    elif os == "asa" and protocol == "ssh":
        socketio.emit("to_js","Respaldando equipo "+hostname+" con IP "+ip)
        resultado = connect_asa_ssh(hostname,ip,protocol,username,password,enable)
        if "Error" in resultado:
            socketio.emit("to_js","Respaldo de "+hostname+" con IP "+ip+" fallo</font>")
            return jsonify({"resultado":"equipo "+hostname+" Error!!!! "+resultado})
        else:
            socketio.emit("to_js","Respaldo de "+hostname+" con IP "+ip+" se ejecuto!</font>")
            return jsonify(resultado)
    elif os == "iosxe" and protocol == "ssh":
        socketio.emit("to_js","Respaldando equipo "+hostname+" con IP "+ip)
        resultado = connect_iosxe_ssh(hostname,ip,protocol,username,password,enable)
        if "Error" in resultado:
            socketio.emit("to_js","Respaldo de "+hostname+" con IP "+ip+" fallo</font>")
            return jsonify({"resultado":"equipo "+hostname+" Error!!!! "+resultado})
        else:
            socketio.emit("to_js","Respaldo de "+hostname+" con IP "+ip+" se ejecuto!</font>")
            return jsonify(resultado)
    else:
        return jsonify({"resultado":"equipo "+hostname+" Error!!!!"})


@app.route("/stateBackup",methods=["POST","GET"])
def stateBackup():
    if request.method == "POST":
        f = request.files["file"]
        f.save(secure_filename(f.filename))
        create_testbed(f.filename)
        lista_equipos_activos = create_list_active_devices()
        if lista_equipos_activos == []:
            print("lista vacia...........")
            socketio.emit("to_state_backup", "no existen equipos activos")
            return("No existen equipos activos")
        else:
            carpeta = parse_all_config(lista_equipos_activos)
            socketio.emit("to_state_backup", "Estado generado exitosamente...")
            return redirect("stateBackup")
    elif request.method == "GET":
        lista_dir = os.listdir()
        return render_template("state_backup.html",lista=lista_dir)


@app.route("/compareStateBackup/<filenames>",methods=["GET","POST"])
def compareStateBackup(filenames):
    result_diff = compare_state(filenames)
    lista_dir =sorted( os.listdir())
    return render_template("state_backup.html",lista = lista_dir)

@app.route("/stateBackup/<carpeta>")
def carpeta(carpeta):
    archivos = sorted(os.listdir(carpeta))
    return render_template("lista_archivos.html", lista_archivos = archivos, folder = carpeta)


@app.route("/stateBackup/<carpeta>/<archivo>")
def archivo(carpeta,archivo):
    return send_from_directory(carpeta,archivo)


#pagina de inicio de acceso a FMC
@app.route("/fmc_start_page",methods = ["POST","GET"])
def fmc_starting_page():
    # generar token de fmc con uuid
    #fmc_login esta en fmc_change_policy.py

    global user_fmc
    global passwd_fmc
    global addr_fmc

    if request.method == "GET":
        if user_fmc == "":
            return render_template("login_fmc.html")
        else:
            respuesta_fmc = fmc_login(user_fmc,passwd_fmc,addr_fmc)
            token_auth = respuesta_fmc["X-auth-access-token"]
            token_refresh = respuesta_fmc['X-auth-refresh-token']
            uuid_fmc = respuesta_fmc["DOMAIN_UUID"]

            lista_de_policy_with_names = get_policy_assignment_with_names(addr_fmc,uuid_fmc,token_auth)
            #print(lista_de_policy_with_names)

            lista_de_ips=get_ips_assignment(addr_fmc,uuid_fmc,token_auth)
            #print(lista_de_ips)

            lista_de_rules_with_names = get_rules_with_names_assignment(addr_fmc,uuid_fmc,lista_de_policy_with_names, token_auth)
            #print(lista_de_rules_with_names)
            lista_de_files=get_files_assignment(addr_fmc,uuid_fmc,token_auth)
            #print(lista_de_files)

            lista_de_variables=get_variable_assignment(addr_fmc,uuid_fmc,token_auth)
            #print(lista_de_variables)
            return render_template("select_fmc_rules.html",lista_de_politicas=json.dumps(lista_de_policy_with_names), lista_de_ips =json.dumps(lista_de_ips), lista_de_files =json.dumps(lista_de_files), lista_de_rules = json.dumps(lista_de_rules_with_names), lista_de_variables = json.dumps(lista_de_variables) )
    if request.method == "POST":
        addr_fmc = request.form["ip"]
        user_fmc = request.form["user"]
        passwd_fmc = request.form["passwd"]
        #return(f"hello {user}")


        respuesta_fmc = fmc_login(user_fmc,passwd_fmc,addr_fmc)
        token_auth = respuesta_fmc["X-auth-access-token"]
        token_refresh = respuesta_fmc['X-auth-refresh-token']
        uuid_fmc = respuesta_fmc["DOMAIN_UUID"]

        lista_de_policy_with_names = get_policy_assignment_with_names(addr_fmc,uuid_fmc,token_auth)
        #print(lista_de_policy_with_names)

        lista_de_ips=get_ips_assignment(addr_fmc,uuid_fmc,token_auth)
        #print(lista_de_ips)

        lista_de_rules_with_names = get_rules_with_names_assignment(addr_fmc,uuid_fmc,lista_de_policy_with_names, token_auth)
        #print(lista_de_rules_with_names)
        lista_de_files=get_files_assignment(addr_fmc,uuid_fmc,token_auth)
        #print(lista_de_files)

        lista_de_variables=get_variable_assignment(addr_fmc,uuid_fmc,token_auth)
        #print(lista_de_variables)
        return render_template("select_fmc_rules.html",lista_de_politicas=json.dumps(lista_de_policy_with_names), lista_de_ips =json.dumps(lista_de_ips), lista_de_files =json.dumps(lista_de_files), lista_de_rules = json.dumps(lista_de_rules_with_names), lista_de_variables = json.dumps(lista_de_variables) )


@app.route("/fmc_change_policy",methods=["POST","GET"])
def fmc_change_policy():
    global user_fmc
    global passwd_fmc
    global addr_fmc


    if request.method == "POST":
        #print(request.form.getlist("mySelect"))
        #print(request.form.getlist("ips_select"))

        pol = request.form["mySelect"]
        ips = request.form["ips_select"]
        files = request.form["files_select"]
        rules = request.form.getlist("rules_select")
        logBegin = request.form["logBegin_select"]
        logEnd = request.form["logEnd_select"]
        variable_set = request.form["var_select"]

        respuesta_fmc = fmc_login(user_fmc,passwd_fmc,addr_fmc)
        token_auth = respuesta_fmc["X-auth-access-token"]
        token_refresh = respuesta_fmc['X-auth-refresh-token']
        uuid_fmc = respuesta_fmc["DOMAIN_UUID"]

        lista_de_policy = get_policy_assignment(addr_fmc,uuid_fmc,token_auth)

        lista_de_policy_with_names = get_policy_assignment_with_names(addr_fmc,uuid_fmc,token_auth)

        lista_de_rules = get_rules_assignment(addr_fmc,uuid_fmc,lista_de_policy, token_auth)

        lista_de_ips=get_ips_assignment(addr_fmc,uuid_fmc,token_auth)

        lista_de_files=get_files_assignment(addr_fmc,uuid_fmc,token_auth)

        lista_de_variables=get_variable_assignment(addr_fmc,uuid_fmc,token_auth)

        if len(rules)==0:
            modify_all_rules(user_fmc,passwd_fmc,addr_fmc,uuid_fmc,lista_de_policy_with_names,lista_de_rules, lista_de_ips,lista_de_files,lista_de_variables, pol,ips,files, variable_set)
            return redirect("/fmc_start_page")
        else:
            modify_some_rules(user_fmc,passwd_fmc,addr_fmc,uuid_fmc,lista_de_policy_with_names,lista_de_rules, lista_de_ips,lista_de_files,lista_de_variables, pol,rules,ips,files,logBegin,logEnd, variable_set)
            return redirect("/fmc_start_page")
        return redirect("/fmc_start_page")

    if request.method == "GET":
        return redirect("/fmc_start_page")


if __name__=="__main__":
    socketio.run(app,port=5000, host= "0.0.0.0",debug=True)
