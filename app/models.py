from datetime import datetime
from app import app
from flask.ext.mongokit import MongoKit, Document, Connection

class Idc(Document):
    __collection__ = 'idc'
    structure = {
        'idc_code': basestring,
        'bandwidth': int,
        'rack_num': int,
        'rack_code': basestring,
        'lan_ip': basestring,
        'wan_ip': basestring,
        'location': basestring,
        'telephone': basestring,
        'auth_code': basestring,
        'tax': basestring,
        'status': basestring,
        'desc': basestring,
        'creation': datetime,
    }
    required_fields = ['idc_code']
    default_values = {'creation': datetime.utcnow}
    use_dot_notation = True
#    indexes = [{'fields': 'idc_code', 'unique': True}]

class Device(Document):
    __collection__ = 'device'
    structure = {
        'host': basestring,
        'assetsnumber': basestring,
        'serialnumber': basestring,
        'osrelease': basestring,
        'cpu_model': basestring,
        'cpu_num': int,
        'mem_total': int,
        'type': basestring,
        'idc_code': basestring,
        'rack_code': basestring,
        'ip': [basestring],
        'vip': [basestring],
        'roles': [basestring],
        'biosversion': basestring,
        'manufacturer': basestring,
        'productname': basestring,
        'status': basestring,
        'desc': basestring,
        'creation': datetime,
    }
    required_fields = ['host', 'serialnumber']
    default_values = {'assetsnumber': '', 'idc_code': '', 'rack_code': '', 'desc':'', 'creation': datetime.utcnow}
    use_dot_notation = True
#    indexes = [{'fields': 'host', 'unique': True}]

class Module(Document):
    __collection__ = 'module'
    structure = {
        'module_name': basestring,
        'module_type': basestring,
        'deploy_script': basestring,
        'host_list': [basestring],
        'desc': basestring,
        'creation': datetime,
    }
    required_fields = ['module_name']
    default_values = {'creation': datetime.utcnow}
    use_dot_notation = True
#    indexes = [{'fields': 'module_name', 'unique': True}]

class Project(Document):
    __collection__ = 'project'
    structure = {
        'project_name': basestring,
        'project_type': basestring,
        'module_list': [basestring],
        'svn_list': [basestring],
        'status': basestring,
        'desc': basestring,
        'creation': datetime,
    }
    required_fields = ['project_name']
    default_values = {'creation': datetime.utcnow}
    use_dot_notation = True
#    indexes = [{'fields': 'project_name', 'unique': True}]

class Script(Document):
    __collection__ = 'script'
    structure = {
        'script_name': basestring,
        'script_argument': basestring,
        'script_content': basestring,
        'script_type': basestring,
        'desc': basestring,
        'creation': datetime,
        'modify': datetime,
    }
    required_fields = ['script_name']
    default_values = {'creation': datetime.utcnow, 'modify': datetime.utcnow}
    use_dot_notation = True
#    indexes = [{'fields': 'script_name', 'unique': True}]

db = MongoKit(app)
db.register([Device, Idc, Module, Script, Project])
