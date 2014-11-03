#-*- coding: UTF-8 -*- 
import os, datetime, bson.objectid
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from wtforms import Form, TextField, validators, SelectField, TextAreaField, BooleanField, SelectMultipleField

from app.models import db
from app import app
from app.db_query import query_server, query_script, query_idc, query_module

assets = Blueprint('assets', __name__, template_folder='templates')
WTF_CSRF_SECRET_KEY = 'QPo3QVT0UyBrPmoqhf'

class IdcForm(Form):
    idc_code = TextField(u'IDC编码', [validators.Required(), validators.Length(min=4, max=10)])
    bandwidth = TextField(u'带宽', [validators.NumberRange])
    rack_num = TextField(u'机柜数量', [validators.NumberRange])
    rack_code = TextField(u'机柜编号')
    lan_ip = TextField(u'内网IP段')
    wan_ip = TextField(u'公网IP段')
    location = TextField(u'地理位置')
    telephone = TextField(u'联系电话')
    auth_code = TextField(u'验证码')
    tax = TextField(u'传真')
    status = SelectField(u'状态', choices=[(u'running', u'running'), (u'closed', u'closed')])
    desc = TextAreaField(u'备注')

class ServerForm(Form):
    host = TextField(u'主机名', [validators.Required()])
    assetsnumber = TextField(u'资产编号')
    serialnumber = TextField(u'设备编号')
    osrelease = TextField(u'系统版本')
    cpu_model = TextField(u'CPU型号')
    cpu_num = TextField(u'CPU核数')
    mem_total = TextField(u'内存大小')
    type = TextField(u'设备类型')
    idc_code = SelectField(u'机房编号', )
    #idc_code = SelectField(u'机房编号', choices=[(u'SHT01', u'SHT01'), (u'JHT01', u'JHT01')])
    rack_code = TextField(u'机柜编号')
    ip = TextField(u'IP地址')
    vip = TextField(u'VIP地址')
    roles = TextField(u'角色')
    biosversion = TextField(u'BIOS版本')
    manufacturer = TextField(u'厂商')
    productname = TextField(u'设备型号')
    status = SelectField(u'状态', choices=[(u'running', u'running'), (u'closed', u'closed')])
    desc = TextAreaField(u'备注')
    clone = BooleanField(u'克隆')

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        #kwargs.setdefault('idc_code', 'some value')
        Form.__init__(self, formdata, obj, prefix, **kwargs)
        list_idc = query_idc()
        self.idc_code.choices = zip(list_idc, list_idc)

class idc(MethodView):
    def get(self):
        db_idc = db.Idc.find()
        return render_template('assets/idc.html', title=(u'资产管理'), IDC=list(db_idc))

class idc_add(MethodView):
    def get(self):
        form = IdcForm(request.form)
        return render_template('assets/idc_add.html', title=(u'资产管理'), form=form)

    def post(self):
        form = IdcForm(request.form)
        if form.validate():
            db_idc = db.Idc.find({"idc_code": form.idc_code.data})
            if not db_idc.count():
                db_idc = db.Idc()
                db_idc["idc_code"] = form.idc_code.data
                try:
                    db_idc["bandwidth"] = int(form.bandwidth.data) 
                except:
                    db_idc["bandwidth"] = 0
                try:
                    db_idc["rack_num"] = int(form.rack_num.data) 
                except:
                    db_idc["rack_num"] = 0
                db_idc["lan_ip"] = form.lan_ip.data
                db_idc["wan_ip"] = form.wan_ip.data
                db_idc["location"] = form.location.data
                db_idc["telephone"] = form.telephone.data
                db_idc["auth_code"] = form.auth_code.data
                db_idc["tax"] = form.tax.data
                db_idc["status"] = form.status.data
                db_idc["desc"] = form.desc.data
                db_idc["creation"] = datetime.datetime.now()
                db_idc.save()
                flash(db_idc["idc_code"] + (u'添加成功！'))
            else:
                flash(form.idc_code.data + (u'重复！'))
        else:
          flash(u"添加IDC错误，请检查添加字段！")
        return render_template('assets/idc_add.html', title=(u'资产管理'), form=form)

class idc_edit(MethodView):
    def get(self, slug):
        db_idc = db.Idc.find({"idc_code": slug})
        form = IdcForm(request.form)
        if db_idc.count():
            form.idc_code.data = db_idc[0]["idc_code"]
            form.bandwidth.data = db_idc[0]["bandwidth"]
            form.rack_num.data = db_idc[0]["rack_num"]
            form.rack_code.data = db_idc[0]["rack_code"]
            form.lan_ip.data = db_idc[0]["lan_ip"]
            form.wan_ip.data = db_idc[0]["wan_ip"]
            form.location.data = db_idc[0]["location"]
            form.telephone.data = db_idc[0]["telephone"]
            form.auth_code.data = db_idc[0]["auth_code"]
            form.tax.data = db_idc[0]["tax"]
            form.status.data = db_idc[0]["status"]
            form.desc.data = db_idc[0]["desc"]
        else:
            flash(u'您编辑的idc编码不存在！')
        return render_template('assets/idc_edit.html', title=(u'资产管理'), slug=slug, form=form)

    def post(self, slug):
        form = IdcForm(request.form)
        if form.validate():
            db_idc = db.Idc()
            db_idc["idc_code"] = form.idc_code.data
            try:
                db_idc["bandwidth"] = int(form.bandwidth.data) 
            except:
                db_idc["bandwidth"] = 0
            try:
                db_idc["rack_num"] = int(form.rack_num.data) 
            except:
                db_idc["rack_num"] = 0
            db_idc["lan_ip"] = form.lan_ip.data
            db_idc["wan_ip"] = form.wan_ip.data
            db_idc["location"] = form.location.data
            db_idc["telephone"] = form.telephone.data
            db_idc["auth_code"] = form.auth_code.data
            db_idc["tax"] = form.tax.data
            db_idc["status"] = form.status.data
            db_idc["desc"] = form.desc.data
            db_idc["creation"] = datetime.datetime.now()
            db.Idc.find_and_modify({"idc_code": slug}, db_idc)
            flash(db_idc["idc_code"] + (u'更新成功！'))
        else:
            flash(u"更新IDC错误，请检查相关字段！")
        return redirect(url_for('assets.idc_edit', slug=slug))

class List(MethodView):
    def get(self):
        #salt_assets = eval(os.popen("""python scripts/salt_ext.py""").readlines()[0])
        salt_assets = query_server()
        return render_template('assets/list.html', title=(u'资产管理'), salt_assets=salt_assets)

class switch(MethodView):
    def get(self):
        #db_switch = db.Switch.find()
        db_switch = []
        return render_template('assets/switch.html', title=(u'资产管理'), IDC=list(db_switch))

class server(MethodView):
    def get(self):
        db_server = db.Device.find()
        return render_template('assets/server.html', title=(u'资产管理'), servers=list(db_server))

class server_add(MethodView):
    def get(self):
        form = ServerForm(request.form)
        return render_template('assets/server_add.html', title=(u'资产管理'), form=form)

    def post(self):
        form = ServerForm(request.form)
        if form.validate():
            db_server = db.Device.find({"host": form.host.data})
            if not db_server.count():
                db_server = db.Device()
                db_server["host"] = form.host.data
                db_server["assetsnumber"] = form.assetsnumber.data
                db_server["serialnumber"] = form.serialnumber.data
                db_server["osrelease"] = form.osrelease.data
                db_server["cpu_model"] = form.cpu_model.data
                try:
                    db_server["cpu_num"] = int(form.cpu_num.data)
                except:
                    db_server["cpu_num"] = 0
                try:
                    db_server["mem_total"] = int(form.mem_total.data)
                except:
                    db_server["mem_total"] = 0
                db_server["type"] = 'server'
                db_server["idc_code"] = form.idc_code.data
                db_server["rack_code"] = form.rack_code.data
                try:
                    db_server["ip"] = form.ip.data.split(',')
                except:
                    db_server["ip"] = []
                try:
                    db_server["vip"] = form.vip.data.split(',')
                except:
                    db_server["vip"] = []
                try:
                    db_server["roles"] = form.roles.data.split(',')
                except:
                    db_server["roles"] = []
                db_server["biosversion"] = form.biosversion.data
                db_server["manufacturer"] = form.manufacturer.data
                db_server["productname"] = form.productname.data
                db_server["status"] = form.status.data
                db_server["desc"] = form.desc.data
                db_server["creation"] = datetime.datetime.now()
                db_server.save()
                flash(db_server["host"] + (u'添加成功！'))
            else:
                flash(form.host.data + (u'重复！'))
        else:
          flash(u"添加服务器错误，请检查相关字段！")
        return render_template('assets/server_add.html', title=(u'资产管理'), form=form)

class server_edit(MethodView):
    def get(self, slug):
        form = ServerForm(request.form)
        db_server = db.Device.find({"_id": bson.objectid.ObjectId(slug)})
        if db_server.count():
            form.host.data = db_server[0]["host"]
            form.assetsnumber.data = db_server[0]["assetsnumber"]
            form.serialnumber.data = db_server[0]["serialnumber"]
            form.osrelease.data = db_server[0]["osrelease"]
            form.cpu_model.data = db_server[0]["cpu_model"]
            form.cpu_num.data = db_server[0]["cpu_num"]
            form.mem_total.data = db_server[0]["mem_total"]
            form.type.data = db_server[0]["type"]
            form.idc_code.data = db_server[0]["idc_code"]
            form.rack_code.data = db_server[0]["rack_code"]
            form.ip.data = ','.join(db_server[0]["ip"])
            form.vip.data = ','.join(db_server[0]["vip"])
            form.roles.data = ','.join(db_server[0]["roles"])
            form.biosversion.data = db_server[0]["biosversion"]
            form.manufacturer.data = db_server[0]["manufacturer"]
            form.productname.data = db_server[0]["productname"]
            form.status.data = db_server[0]["status"]
            form.desc.data = db_server[0]["desc"]
        else:
            flash(u'您编辑的服务器不存在！')
        return render_template('assets/server_edit.html', title=(u'资产管理'), slug=slug, form=form)

    def post(self, slug):
        form = ServerForm(request.form)
        if form.validate() and ( not form.clone.data):
            db_server = db.Device()
            db_server["host"] = form.host.data
            db_server["assetsnumber"] = form.assetsnumber.data
            db_server["serialnumber"] = form.serialnumber.data
            db_server["osrelease"] = form.osrelease.data
            db_server["cpu_model"] = form.cpu_model.data
            try:
                db_server["cpu_num"] = int(form.cpu_num.data)
            except:
                db_server["cpu_num"] = 0
            try:
                db_server["mem_total"] = int(form.mem_total.data)
            except:
                db_server["mem_total"] = 0
            db_server["type"] = 'server'
            db_server["idc_code"] = form.idc_code.data
            db_server["rack_code"] = form.rack_code.data
            try:
                db_server["ip"] = form.ip.data.split(',')
            except:
                db_server["ip"] = []
            try:
                db_server["vip"] = form.vip.data.split(',')
            except:
                db_server["vip"] = []
            try:
                db_server["roles"] = form.roles.data.split(',')
            except:
                db_server["roles"] = []
            db_server["biosversion"] = form.biosversion.data
            db_server["manufacturer"] = form.manufacturer.data
            db_server["productname"] = form.productname.data
            db_server["status"] = form.status.data
            db_server["desc"] = form.desc.data
            db_server["creation"] = datetime.datetime.now()
            db.Device.find_and_modify({"_id": bson.objectid.ObjectId(slug)}, db_server)
            flash(form.host.data + (u'更新成功！'))
        elif form.validate() and form.clone.data:
            db_server = db.Device.find({"host": form.host.data})
            if not db_server.count():
                db_server = db.Device()
                db_server["host"] = form.host.data
                db_server["assetsnumber"] = form.assetsnumber.data
                db_server["serialnumber"] = form.serialnumber.data
                db_server["osrelease"] = form.osrelease.data
                db_server["cpu_model"] = form.cpu_model.data
                try:
                    db_server["cpu_num"] = int(form.cpu_num.data)
                except:
                    db_server["cpu_num"] = 0
                try:
                    db_server["mem_total"] = int(form.mem_total.data)
                except:
                    db_server["mem_total"] = 0
                db_server["type"] = 'server'
                db_server["idc_code"] = form.idc_code.data
                db_server["rack_code"] = form.rack_code.data
                try:
                    db_server["ip"] = form.ip.data.split(',')
                except:
                    db_server["ip"] = []
                try:
                    db_server["vip"] = form.vip.data.split(',')
                except:
                    db_server["vip"] = []
                try:
                    db_server["roles"] = form.roles.data.split(',')
                except:
                    db_server["roles"] = []
                db_server["biosversion"] = form.biosversion.data
                db_server["manufacturer"] = form.manufacturer.data
                db_server["productname"] = form.productname.data
                db_server["status"] = form.status.data
                db_server["desc"] = form.desc.data
                db_server["creation"] = datetime.datetime.now()
                db_server.save()
                flash(u'克隆' + form.host.data + (u'成功！'))
            else:
                flash(u'克隆' + form.host.data + (u'重复！'))
        else:
            flash(u"更新或克隆服务器错误，请检查相关字段！")
        return redirect(url_for('assets.server_edit', slug=slug))

class server_del(MethodView):
    def get(self, slug):
        db_server = db.Device.find({"_id": bson.objectid.ObjectId(slug)})
        server_name = db_server[0]["host"]
        if db_server.count():
            db.device.remove({"_id": bson.objectid.ObjectId(slug)})
            flash(u'删除服务器' + server_name + u'成功！')
        else:
            flash(u'您要删除的服务器' + server_name + u'不存在！')
        return redirect(url_for('assets.server'))

class server_salt_import(MethodView):
    def get(self):
        db_server = eval(os.popen("""python script/sys_salt_ext.py""").read())
        return render_template('assets/server_salt_import.html', title=(u'资产管理'), servers=db_server)

    def post(self):
        re_host = []
        assets = eval(os.popen("""python script/sys_salt_ext.py""").read())
        servers = request.form.values()
        if "checkedAll" in servers:
            servers.remove("checkedAll")
        for i in servers:
            host = assets[i]
            db_server = db.Device.find({"host": host["host"]})
            if not db_server.count():
                db_server = db.Device()
                db_server["host"] = host["host"]
                db_server["assetsnumber"] = ""
                db_server["serialnumber"] = host["serialnumber"]
                db_server["osrelease"] = host["os"] + " " + host["osrelease"]
                db_server["cpu_model"] = host["cpu_model"]
                db_server["cpu_num"] = host["num_cpus"]
                db_server["mem_total"] = host["mem_total"]
                db_server["type"] = 'server'
                db_server["idc_code"] = ''
                db_server["rack_code"] = ''
                db_server["ip"] = host["ipv4"]
                db_server["vip"] = []
                if "roles" not in host:
                    db_server["roles"] = []
                else:
                    db_server["roles"] = host["roles"]
                db_server["biosversion"] = host["biosversion"]
                db_server["manufacturer"] = host["manufacturer"]
                db_server["productname"] = host["productname"]
                db_server["status"] = 'running'
                db_server["desc"] = ''
                db_server["creation"] = datetime.datetime.now()
                db_server.save()
                re_host.append(host["host"] + u'成功！')
            else:
                re_host.append(host["host"] + u'重复！')
        return render_template('assets/server_salt_import.html', title=(u'资产管理'), servers={}, host=re_host)

# Register the urls
assets.add_url_rule('/assets/', view_func=List.as_view('list'))

assets.add_url_rule('/assets/server/', view_func=server.as_view('server'))
assets.add_url_rule('/assets/server/add', view_func=server_add.as_view('server_add'))
assets.add_url_rule('/assets/server/edit_<slug>', view_func=server_edit.as_view('server_edit'))
assets.add_url_rule('/assets/server/del_<slug>', view_func=server_del.as_view('server_del'))
assets.add_url_rule('/assets/server_salt_import', view_func=server_salt_import.as_view('server_salt_import'))

assets.add_url_rule('/assets/switch/', view_func=switch.as_view('switch'))

assets.add_url_rule('/assets/idc/', view_func=idc.as_view('idc'))
assets.add_url_rule('/assets/idc/add', view_func=idc_add.as_view('idc_add'))
assets.add_url_rule('/assets/idc/edit_<slug>', view_func=idc_edit.as_view('idc_edit'))
