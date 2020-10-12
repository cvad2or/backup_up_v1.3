import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import urllib3
from flask_bootstrap import Bootstrap
urllib3.disable_warnings()

#prueba fmc

def fmc_login(user_fmc,passwd_fmc,addr_fmc):
    response_fmc = requests.post('https://'+addr_fmc+'//api/fmc_platform/v1/auth/generatetoken', verify=False, auth=HTTPBasicAuth(user_fmc, passwd_fmc))
    response_fmc_json =  {
        "X-auth-access-token": response_fmc.headers["X-auth-access-token"],
        "X-auth-refresh-token": response_fmc.headers["X-auth-refresh-token"],
        "DOMAIN_UUID": response_fmc.headers["DOMAIN_UUID"]
    }
    #print(responce_fmc_json)
    return(response_fmc_json)

def get_policy_assignment(addr_fmc,uuid_fmc,token_auth):
    api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies?limit=900"
    url = "https://" + addr_fmc + api_uri
    headers = {
        "X-auth-access-token": token_auth
    }
    lista_de_policy = []
    response = requests.get(url, headers=headers, verify=False)

    #print(json.loads(response.text)["items"])
    for i in json.loads(response.text)["items"]:
        lista_de_policy.append(i["id"])
        #lista_de_policy.append(i["name"])
    return lista_de_policy

def get_policy_assignment_with_names(addr_fmc,uuid_fmc,token_auth):
    api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies?limit=900"
    url = "https://" + addr_fmc + api_uri
    headers = {
        "X-auth-access-token": token_auth
    }
    lista_de_policy = {}
    response = requests.get(url, headers=headers, verify=False)

    #print(json.loads(response.text)["items"])
    for i in json.loads(response.text)["items"]:
        i.pop("type")
        i.pop("links")
        lista_de_policy[i["name"]]=i["id"]
    return lista_de_policy

def get_ips_assignment(addr_fmc,uuid_fmc,token_auth):
    api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/intrusionpolicies"
    url = "https://" + addr_fmc + api_uri
    headers = {
        "X-auth-access-token": token_auth
    }
    lista_de_ips = {}
    response = requests.get(url, headers=headers, verify=False)

    #print(json.loads(response.text)["items"])
    for i in json.loads(response.text)["items"]:
        i.pop("links")
        i.pop("type")
        lista_de_ips[i["name"]]=i["id"]
        #print(lista_de_ips)
    return lista_de_ips

def get_files_assignment(addr_fmc,uuid_fmc,token_auth):
    api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/filepolicies"
    url = "https://" + addr_fmc + api_uri
    headers = {
        "X-auth-access-token": token_auth
    }
    lista_de_files = {}
    response = requests.get(url, headers=headers, verify=False)

    #print(json.loads(response.text)["items"])
    if "items" not in json.loads(response.text):
        return lista_de_files
    else:
        for i in json.loads(response.text)["items"]:
            i.pop("links")
            i.pop("type")
            lista_de_files[i["name"]]=i["id"]
            #print(lista_de_files)
        return lista_de_files

def get_variable_assignment(addr_fmc,uuid_fmc,token_auth):
    api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/object/variablesets"
    url = "https://" + addr_fmc + api_uri
    headers = {
        "X-auth-access-token": token_auth
    }
    lista_de_variables = {}
    response = requests.get(url, headers=headers, verify=False)

    #print(json.loads(response.text)["items"])
    for i in json.loads(response.text)["items"]:
        i.pop("links")
        i.pop("type")
        lista_de_variables[i["name"]]=i["id"]
        #print(lista_de_variables)
    return lista_de_variables

def get_rules_assignment(addr_fmc,uuid_fmc,lista_de_policy, token_auth):
    lista_de_rules = {}
    for policy_id in lista_de_policy:
        #print(policy_id)
        lista_de_rules[policy_id]=[]
        api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies/{policy_id}/accessrules?limit=5000"
        url = "https://" + addr_fmc + api_uri
        headers = {
            "X-auth-access-token": token_auth
        }
        response = requests.get(url, headers=headers, verify=False)
        if "next" in json.loads(response.text)["paging"]:
            for rule in json.loads(response.text)["items"]:
                lista_de_rules[policy_id].append([rule["id"],rule["name"]])
            for fmc_url in json.loads(response.text)["paging"]["next"]:
                response = requests.get(fmc_url, headers=headers, verify=False)
                for rule in json.loads(response.text)["items"]:
                    lista_de_rules[policy_id].append([rule["id"],rule["name"]])
        else:
            #print(json.loads(response.text)["paging"])
            for rule in json.loads(response.text)["items"]:
                lista_de_rules[policy_id].append([rule["id"],rule["name"]])
    with open("new_1.json","a") as file:
        file.write(json.dumps(lista_de_rules))
    #print(lista_de_rules)
    return(lista_de_rules)

def get_rules_with_names_assignment(addr_fmc,uuid_fmc,lista_de_policy_with_names, token_auth):
    lista_de_rules = {}
    for policy_id in lista_de_policy_with_names:
        #print(policy_id)
        lista_de_rules[policy_id]=[]
        api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies/{lista_de_policy_with_names[policy_id]}/accessrules?limit=5000"
        url = "https://" + addr_fmc + api_uri
        headers = {
            "X-auth-access-token": token_auth
        }
        response = requests.get(url, headers=headers, verify=False)
        if "next" in json.loads(response.text)["paging"]:
            for rule in json.loads(response.text)["items"]:
                lista_de_rules[policy_id].append([rule["id"],rule["name"]])
            for fmc_url in json.loads(response.text)["paging"]["next"]:
                response = requests.get(fmc_url, headers=headers, verify=False)
                for rule in json.loads(response.text)["items"]:
                    lista_de_rules[policy_id].append([rule["id"],rule["name"]])
        else:
            #print(json.loads(response.text)["paging"])
            for rule in json.loads(response.text)["items"]:
                lista_de_rules[policy_id].append([rule["id"],rule["name"]])
    with open("new_1.json","a") as file:
        file.write(json.dumps(lista_de_rules))
    return(lista_de_rules)

def modify_all_rules(user_fmc,passwd_fmc,addr_fmc,uuid_fmc,lista_de_policy_with_names,lista_de_rules, lista_de_ips,lista_de_files,lista_de_variables, pol,ips_pol_name,file_pol_name, variable_set):
    startTime = datetime.now()
    respuesta_fmc = fmc_login(user_fmc,passwd_fmc,addr_fmc)
    token_auth = respuesta_fmc["X-auth-access-token"]
    token_refresh = respuesta_fmc['X-auth-refresh-token']
    uuid_fmc = respuesta_fmc["DOMAIN_UUID"]
    for policy_name in lista_de_policy_with_names:
        if policy_name.strip() == pol.strip():
            n_rules = 0
            print("................buscando.......")
            for rule_id in lista_de_rules[lista_de_policy_with_names[policy_name]]:
                midTime = datetime.now()
                if (midTime-startTime).total_seconds() > 1200:
                    respuesta_fmc = fmc_login(user_fmc,passwd_fmc,addr_fmc)
                    token_auth = respuesta_fmc["X-auth-access-token"]
                    token_refresh = respuesta_fmc['X-auth-refresh-token']
                    uuid_fmc = respuesta_fmc["DOMAIN_UUID"]
                api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies/{lista_de_policy_with_names[policy_name]}/accessrules/{rule_id[0]}"
                url = "https://" + addr_fmc + api_uri
                headers = {
                    "X-auth-access-token": token_auth
                }
                response = requests.get(url, headers=headers, verify=False)
                response_json = json.loads(response.text)
                response_json.pop("links",None)
                response_json.pop("metadata",None)
                #print("...........response...")
                #print(response_json)
                dict_de_attributos ={}

                dict_de_attributos["id"] = response_json["id"]
                dict_de_attributos["action"]=response_json["action"]
                dict_de_attributos["enabled"] = response_json["enabled"]
                dict_de_attributos["name"] = response_json["name"]
                dict_de_attributos["logBegin"] = response_json["logBegin"]
                dict_de_attributos["logEnd"] = response_json["logEnd"]
                dict_de_attributos["logFiles"] = response_json["logFiles"]
                dict_de_attributos["enableSyslog"] = response_json["enableSyslog"]
                dict_de_attributos["sendEventsToFMC"] = response_json["sendEventsToFMC"]


                if ips_pol_name!="":
                    for ids in lista_de_ips:
                        if ids.strip() == ips_pol_name.strip():
                            result_ips_id = lista_de_ips[ids]
                            result_ips_name = ids
                            dict_de_attributos["ipsPolicy"] ={
                                "name": result_ips_name,
                                 "id": result_ips_id,
                                 "type": "IntrusionPolicy"
                                }
                            if variable_set!="":
                                for var in lista_de_variables:
                                    if var.strip() == variable_set.strip():
                                        result_vars_id = lista_de_variables[var]
                                        result_vars_name = var
                                        #print(result_vars_id)
                                        #print(result_vars_name)
                                        dict_de_attributos["variableSet"] ={
                                            "name": result_vars_name,
                                            "id": result_vars_id,
                                            "type": "VariableSet"
                                        }
                            else:
                                dict_de_attributos["variableSet"] = response_json["variableSet"]

                elif response_json.get("ipsPolicy"):
                    dict_de_attributos["ipsPolicy"] = response_json["ipsPolicy"]
                    dict_de_attributos["variableSet"] = response_json["variableSet"]
                else:
                    pass


                if file_pol_name!="":
                    for files in lista_de_files:
                        if files.strip() == file_pol_name.strip():
                            result_files_id = lista_de_files[files]
                            result_files_name = files

                            dict_de_attributos["filePolicy"] ={
                                "name": result_files_name,
                                "id": result_files_id,
                                "type": "FilePolicy"
                           }
                elif response_json.get("filePolicy"):
                    dict_de_attributos["filePolicy"] = response_json["filePolicy"]
                else:
                    pass

                if not response_json.get("users"):
                    pass
                else:
                    rule_users = response_json["users"]
                    for users in rule_users["objects"]:
                        users.pop("realm")
                    dict_de_attributos["users"]=rule_users

                if not response_json.get("sourceZones"):
                    pass
                else:
                    dict_de_attributos["sourceZones"] = response_json["sourceZones"]

                if not response_json.get("destinationZones"):
                    pass
                else:
                    dict_de_attributos["destinationZones"] = response_json["destinationZones"]

                if not response_json.get("sourceNetworks"):
                    pass
                else:
                    dict_de_attributos["sourceNetworks"] = response_json["sourceNetworks"]

                if not response_json.get("destinationNetworks"):
                    pass
                else:
                    dict_de_attributos["destinationNetworks"] = response_json["destinationNetworks"]

                if not response_json.get("vlanTags"):
                    pass
                else:
                    dict_de_attributos["vlanTags"] = response_json["vlanTags"]



                if not response_json.get("applications"):
                    pass
                else:
                    dict_de_attributos["applications"] = response_json["applications"]

                if not response_json.get("sourcePorts"):
                    pass
                else:
                    dict_de_attributos["sourcePorts"] = response_json["sourcePorts"]

                if not response_json.get("destinationPorts"):
                    pass
                else:
                    dict_de_attributos["destinationPorts"] = response_json["destinationPorts"]

                if not response_json.get("urls"):
                    pass
                else:
                    dict_de_attributos["urls"] = response_json["urls"]


                if not response_json.get("sourceSecurityGroupTags"):
                    pass
                else:
                    dict_de_attributos["sourceSecurityGroupTags"] = response_json["sourceSecurityGroupTags"]

                #print("...........atributos ...")
                #print(dict_de_attributos)
                api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies/{lista_de_policy_with_names[policy_name]}/accessrules/{rule_id[0]}"
                url = "https://" + addr_fmc + api_uri

                headers1 = {
                    "X-auth-access-token": token_auth,
                    "Content-Type": "application/json"
                }
                if "result_ips_name" in locals():
                    if "result_vars_name" in locals():
                        if "result_files_name" in locals():
                            print(".........................................................................")
                            print("....agregando politica IPS "+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                            print("....agregando VariableSet "+result_vars_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                            print("....agregando politica Files "+result_files_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                            response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                            print("........................"+str(response)+"................................")
                            print(".........................................................................")
                            n_rules=n_rules+1
                        else:
                            print(".........................................................................")
                            print("....agregando politica IPS"+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                            print("....agregando VariableSet "+result_vars_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                            response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                            print("........................"+str(response)+"................................")
                            print(".........................................................................")
                            n_rules=n_rules+1
                    elif "result_files_name" in locals():
                        print(".........................................................................")
                        print("....agregando politica IPS "+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                        print("....agregando politica Files "+result_files_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                        response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                        print("........................"+str(response)+"................................")
                        print(".........................................................................")
                        n_rules=n_rules+1
                    else:
                        print(".........................................................................")
                        print("....agregando politica IPS "+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                        response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                        print("........................"+str(response)+"................................")
                        print(".........................................................................")
                        n_rules=n_rules+1
                elif "result_files_name" in locals():
                        print(".........................................................................")
                        print("....agregando politica Files "+result_files_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                        response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                        print("........................"+str(response)+"................................")
                        print(".........................................................................")
                        n_rules=n_rules+1
        else:
            pass
    stopTime = datetime.now()
    print("...............................................................")
    print("...............se modificaron "+str(n_rules)+" reglas.................")
    print("...............................................................")
    print("......tiempo de ejecucion "+str(stopTime-startTime)+" segundos........")
    print("...............................................................")

def modify_some_rules(user_fmc,passwd_fmc,addr_fmc,uuid_fmc,lista_de_policy_with_names,lista_de_rules, lista_de_ips,lista_de_files,lista_de_variables, pol,rules,ips_pol_name,file_pol_name,logBegin,logEnd, variable_set):
    startTime = datetime.now()
    n_rules = 0
    for rule in rules:
        for policy_name in lista_de_policy_with_names:
            if policy_name.strip() == pol.strip():
                print("................buscando.......")
                for rule_id in lista_de_rules[lista_de_policy_with_names[policy_name]]:
                    if rule == rule_id[1]:
                        respuesta_fmc = fmc_login(user_fmc,passwd_fmc,addr_fmc)
                        token_auth = respuesta_fmc["X-auth-access-token"]
                        token_refresh = respuesta_fmc['X-auth-refresh-token']
                        uuid_fmc = respuesta_fmc["DOMAIN_UUID"]
                        api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies/{lista_de_policy_with_names[policy_name]}/accessrules/{rule_id[0]}"
                        url = "https://" + addr_fmc + api_uri
                        headers = {
                            "X-auth-access-token": token_auth
                        }
                        response = requests.get(url, headers=headers, verify=False)
                        response_json = json.loads(response.text)
                        response_json.pop("links",None)
                        response_json.pop("metadata",None)

                        dict_de_attributos ={}

                        dict_de_attributos["id"] = response_json["id"]
                        dict_de_attributos["action"]=response_json["action"]
                        dict_de_attributos["enabled"] = response_json["enabled"]
                        dict_de_attributos["name"] = response_json["name"]
                        dict_de_attributos["logBegin"] = response_json["logBegin"]
                        dict_de_attributos["logEnd"] = response_json["logEnd"]


                        if logBegin !="" and logBegin=="YES":
                           dict_de_attributos["logBegin"] = "true"
                           dict_de_attributos["sendEventsToFMC"] = "true"
                        elif  logBegin !="" and logBegin=="NO":
                           dict_de_attributos["logBegin"] = "false"
                        elif  logBegin =="":
                            dict_de_attributos["logBegin"] = response_json["logBegin"]
                            dict_de_attributos["sendEventsToFMC"] = response_json["sendEventsToFMC"]

                        if logEnd !="" and logEnd=="YES":
                           dict_de_attributos["logEnd"] = "true"
                           dict_de_attributos["sendEventsToFMC"] = "true"
                        elif  logEnd !="" and logEnd=="NO":
                           dict_de_attributos["logEnd"] = "flase"
                        elif logEnd =="":
                            dict_de_attributos["logEnd"] = response_json["logEnd"]
                            dict_de_attributos["sendEventsToFMC"] = response_json["sendEventsToFMC"]

                        dict_de_attributos["logFiles"] = response_json["logFiles"]
                        dict_de_attributos["enableSyslog"] = response_json["enableSyslog"]


                        if ips_pol_name!="":
                            for ids in lista_de_ips:
                                if ids.strip() == ips_pol_name.strip():
                                    result_ips_id = lista_de_ips[ids]
                                    result_ips_name = ids
                                    dict_de_attributos["ipsPolicy"] ={
                                        "name": result_ips_name,
                                        "id": result_ips_id,
                                        "type": "IntrusionPolicy"
                                    }
                                    if variable_set!="":
                                        #print(variable_set)
                                        #print(lista_de_variables)
                                        for var in lista_de_variables:
                                            if var.strip() == variable_set.strip():
                                                result_vars_id = lista_de_variables[var]
                                                result_vars_name = var
                                                #print(result_vars_id)
                                                #
                                                # print(result_vars_name)
                                                dict_de_attributos["variableSet"] ={
                                                "name": result_vars_name,
                                                "id": result_vars_id,
                                                "type": "VariableSet"
                                                }
                        elif response_json.get("ipsPolicy"):
                            dict_de_attributos["ipsPolicy"] = response_json["ipsPolicy"]
                            dict_de_attributos["variableSet"] = response_json["variableSet"]
                        else:
                            pass

                        if file_pol_name!="":
                            for files in lista_de_files:
                                if files.strip() == file_pol_name.strip():
                                    result_files_id = lista_de_files[files]
                                    result_files_name = files

                                    dict_de_attributos["filePolicy"] ={
                                        "name": result_files_name,
                                        "id": result_files_id,
                                        "type": "FilePolicy"
                                }
                        elif response_json.get("filePolicy"):
                            dict_de_attributos["filePolicy"] = response_json["filePolicy"]
                        else:
                            pass

                        if not response_json.get("users"):
                            pass
                        else:
                            rule_users = response_json["users"]
                            for users in rule_users["objects"]:
                                users.pop("realm")
                            dict_de_attributos["users"]=rule_users



                        if not response_json.get("sourceZones"):
                            pass
                        else:
                            dict_de_attributos["sourceZones"] = response_json["sourceZones"]

                        if not response_json.get("destinationZones"):
                            pass
                        else:
                            dict_de_attributos["destinationZones"] = response_json["destinationZones"]

                        if not response_json.get("sourceNetworks"):
                            pass
                        else:
                            dict_de_attributos["sourceNetworks"] = response_json["sourceNetworks"]

                        if not response_json.get("destinationNetworks"):
                            pass
                        else:
                            dict_de_attributos["destinationNetworks"] = response_json["destinationNetworks"]

                        if not response_json.get("vlanTags"):
                            pass
                        else:
                            dict_de_attributos["vlanTags"] = response_json["vlanTags"]

                        if not response_json.get("applications"):
                            pass
                        else:
                            dict_de_attributos["applications"] = response_json["applications"]

                        if not response_json.get("sourcePorts"):
                            pass
                        else:
                            dict_de_attributos["sourcePorts"] = response_json["sourcePorts"]

                        if not response_json.get("destinationPorts"):
                            pass
                        else:
                            dict_de_attributos["destinationPorts"] = response_json["destinationPorts"]

                        if not response_json.get("urls"):
                            pass
                        else:
                            dict_de_attributos["urls"] = response_json["urls"]

                        if not response_json.get("sourceSecurityGroupTags"):
                            pass
                        else:
                            dict_de_attributos["sourceSecurityGroupTags"] = response_json["sourceSecurityGroupTags"]

                        #print(dict_de_attributos)
                        api_uri = f"/api/fmc_config/v1/domain/{uuid_fmc}/policy/accesspolicies/{lista_de_policy_with_names[policy_name]}/accessrules/{rule_id[0]}"
                        url = "https://" + addr_fmc + api_uri

                        headers1 = {
                            "X-auth-access-token": token_auth,
                            "Content-Type": "application/json"
                        }
                        if "result_ips_name" in locals():
                            if "result_vars_name" in locals():
                                if "result_files_name" in locals():
                                    print(".........................................................................")
                                    print("....agregando politica IPS "+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                    print("....agregando VariableSet "+result_vars_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                    print("....agregando politica Files "+result_files_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                    response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                                    print("........................"+str(response)+"................................")
                                    print(".........................................................................")
                                    n_rules=n_rules+1
                                else:
                                    print(".........................................................................")
                                    print("....agregando politica IPS"+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                    print("....agregando VariableSet "+result_vars_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                    response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                                    print("........................"+str(response)+"................................")
                                    print(".........................................................................")
                                    n_rules=n_rules+1
                            elif "result_files_name" in locals():
                                print(".........................................................................")
                                print("....agregando politica IPS "+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                print("....agregando politica Files "+result_files_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                                print("........................"+str(response)+"................................")
                                print(".........................................................................")
                                n_rules=n_rules+1
                            else:
                                print(".........................................................................")
                                print("....agregando politica IPS "+result_ips_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                                print("........................"+str(response)+"................................")
                                print(".........................................................................")
                                n_rules=n_rules+1
                        elif "result_files_name" in locals():
                                print(".........................................................................")
                                print("....agregando politica Files "+result_files_name+" a la regla "+ rule_id[1] + " de "+policy_name )
                                response = requests.put(url, headers=headers1, verify=False, data=json.dumps(dict_de_attributos))
                                print("........................"+str(response)+"................................")
                                print(".........................................................................")
                                n_rules=n_rules+1


                    else:
                        pass
            else:
                pass

    stopTime = datetime.now()
    print("...............................................................")
    print("...............se modificaron "+str(n_rules)+" regla(s).................")
    print("...............................................................")
    print("......tiempo de ejecucion "+str(stopTime-startTime)+" segundos........")
    print("...............................................................")



