#-*- coding: UTF-8 -*-
from app import app
from app.models import db

def query_server():
    re = []
    db_query = list(db.Device.find({"type": "server"},{"_id":0, "host":1}))
    for i in db_query:
        re.append(i.values()[0])
    return re

def query_script():
    re = []
    db_query = list(db.Script.find({},{"_id":0, "script_name":1}))
    for i in db_query:
        re.append(i.values()[0])
    return re

def query_idc():
    re = []
    db_query = list(db.idc.find({},{"_id":0, "idc_code":1}))
    for i in db_query:
        re.append(i.values()[0])
    return re

def query_module():
    re = []
    db_query = list(db.Module.find({},{"_id":0, "module_name":1}))
    for i in db_query:
        re.append(i.values()[0])
    return re

def query_deploy_info():
    project_query = list(db.Project.find({"status": "running"},{"_id":0, "project_name":1, "module_list":1, "svn_list":1}))
    module_query = list(db.Module.find({},{"_id":0, "module_name":1, "deploy_script":1, "host_list":1}))
    re = {"project":project_query, "module":module_query}
    return re
