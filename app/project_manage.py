#-*- coding: UTF-8 -*- 
import os, datetime, bson.objectid, commands, time
from flask import Blueprint, request, redirect, render_template, url_for, flash, jsonify
from flask.views import MethodView
from wtforms import Form, TextField, validators, SelectField, TextAreaField, BooleanField, SelectMultipleField

from app.db_query import query_server, query_script, query_idc, query_module, query_deploy_info
from app.models import db
from app import app

project = Blueprint('project', __name__, template_folder='templates')
WTF_CSRF_SECRET_KEY = 'QPo3QVT0UyBrPmoqhf'

class ModuleForm(Form):
    module_name = TextField(u'模块名称', [validators.Required(), validators.Length(min=4, max=18)])
    module_type = SelectField(u'模块类型', choices=[(u"App", u"App"), (u"Kiss", u"Kiss"), (u"Service", u"Service"),\
        (u"Img", u"Img"), (u"Data", u"Data"), (u"Game", u"Game"), (u"Other", u"Other")])
    deploy_script = SelectField(u'部署脚本')
    host_list = SelectMultipleField(u'服务器列表')
    desc = TextAreaField(u'备注')

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        #kwargs.setdefault({'deploy_script': '', 'host_list': ''})
        #kwargs.setdefault('host_list', '')
        Form.__init__(self, formdata, obj, prefix, **kwargs)
        script_list = query_script()
        server_list = query_server()
        self.deploy_script.choices = zip(script_list, script_list)
        self.host_list.choices = zip(server_list, server_list)


class ProjectForm(Form):
    project_name = TextField(u'项目名称', [validators.Required(), validators.Length(min=3, max=18)])
    project_type = SelectField(u'项目类型', choices=[(u"P-OPS", u"P-OPS"), (u"GAME-SGYW", u"GAME-SGYW")])
    module_list = SelectMultipleField(u'模块列表')
    svn_list = TextField(u'svn列表')
    status = SelectField(u'状态', choices=[(u'running', u'running'), (u'closed', u'closed')])
    desc = TextAreaField(u'备注')

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        #kwargs.setdefault('host_list', '')
        Form.__init__(self, formdata, obj, prefix, **kwargs)
        module_list = query_module()
        self.module_list.choices = zip(module_list, module_list)


class module(MethodView):
    def get(self):
        db_module = db.Module.find()
        return render_template('project/module.html', title=(u'项目管理'), modules=list(db_module))


class module_add(MethodView):
    def get(self):
        form = ModuleForm(request.form)
        return render_template('project/module_add.html', title=(u'项目管理'), form=form)


    def post(self):
        form = ModuleForm(request.form)
        #app.logger.warning(form.host_list.data)
        if form.validate():
            db_module = db.Module.find({"module_name": form.module_name.data})
            if not db_module.count():
                db_module = db.Module()
                db_module["module_name"] = form.module_name.data
                db_module["module_type"] = form.module_type.data
                db_module["deploy_script"] = form.deploy_script.data
                try:
                    db_module["host_list"] = form.host_list.data
                except:
                    db_module["host_list"] = []
                db_module["desc"] = form.desc.data
                db_module["creation"] = datetime.datetime.now()
                db_module.save()
                flash(db_module["module_name"] + (u'添加成功！'))
            else:
                flash(form.module_name.data + (u'重复！'))
        else:
          flash(u"添加模块错误，请检查相关字段！")
        return render_template('project/module_add.html', title=(u'项目管理'), form=form)


class module_edit(MethodView):
    def get(self, slug):
        form = ModuleForm(request.form)
        db_module = db.Module.find({"_id": bson.objectid.ObjectId(slug)})
        if db_module.count():
            form.module_name.data = db_module[0]["module_name"]
            form.module_type.data = db_module[0]["module_type"]
            form.deploy_script.data = db_module[0]["deploy_script"]
            form.host_list.data = ','.join(db_module[0]["host_list"])
            form.desc.data = db_module[0]["desc"]
        else:
            flash(u'您编辑的模块不存在！')
        return render_template('project/module_edit.html', title=(u'项目管理'), slug=slug, form=form)


    def post(self, slug):
        form = ModuleForm(request.form)
        if form.validate() :
            db_module = db.Module()
            db_module["module_name"] = form.module_name.data
            db_module["module_type"] = form.module_type.data
            db_module["deploy_script"] = form.deploy_script.data
            try:
                db_module["host_list"] = form.host_list.data
            except:
                db_module["host_list"] = []
            db_module["desc"] = form.desc.data
            db_module["creation"] = datetime.datetime.now()
            db.Module.find_and_modify({"_id": bson.objectid.ObjectId(slug)}, db_module)
            flash(form.module_name.data + (u'更新成功！'))
        else:
            flash(u"更新模块错误，请检查相关字段！")
        return redirect(url_for('project.module_edit', slug=slug))


class module_del(MethodView):
    def get(self, slug):
        db_module = db.Module.find({"_id": bson.objectid.ObjectId(slug)})
        module_name = db_module[0]["module_name"]
        if db_module.count():
            db.module.remove({"_id": bson.objectid.ObjectId(slug)})
            flash(u'删除模块' + module_name + u'成功！')
        else:
            flash(u'您要删除的模块' + module_name + u'不存在！')
        return redirect(url_for('project.module'))


class List(MethodView):
    def get(self):
        db_project = db.Project.find()
        return render_template('project/project.html', title=(u'项目管理'), projects=list(db_project))


class project_add(MethodView):
    def get(self):
        form = ProjectForm(request.form)
        return render_template('project/project_add.html', title=(u'项目管理'), form=form)


    def post(self):
        form = ProjectForm(request.form)
        if form.validate():
            db_project = db.Project.find({"project_name": form.project_name.data})
            if not db_project.count():
                db_project = db.Project()
                db_project["project_name"] = form.project_name.data
                db_project["project_type"] = form.project_type.data
                try:
                    db_project["module_list"] = form.module_list.data
                except:
                    db_project["module_list"] = []
                try:
                    db_project["svn_list"] = form.svn_list.data.split(',')
                except:
                    db_project["svn_list"] = []
                db_project["status"] = form.status.data
                db_project["desc"] = form.desc.data
                db_project["creation"] = datetime.datetime.now()
                db_project.save()
                flash(db_project["project_name"] + (u'添加成功！'))
            else:
                flash(form.project_name.data + (u'重复！'))
        else:
          flash(u"添加项目错误，请检查相关字段！")
        return render_template('project/project_add.html', title=(u'项目管理'), form=form)


class project_edit(MethodView):
    def get(self, slug):
        form = ProjectForm(request.form)
        db_project = db.Project.find({"_id": bson.objectid.ObjectId(slug)})
        if db_project.count():
            form.project_name.data = db_project[0]["project_name"]
            form.project_type.data = db_project[0]["project_type"]
            form.module_list.data = ','.join(db_project[0]["module_list"])
            form.svn_list.data = ','.join(db_project[0]["svn_list"])
            form.status.data = db_project[0]["status"]
            form.desc.data = db_project[0]["desc"]
        else:
            flash(u'您编辑的项目不存在！')
        return render_template('project/project_edit.html', title=(u'项目管理'), slug=slug, form=form)


    def post(self, slug):
        form = ProjectForm(request.form)
        if form.validate() :
            db_project = db.Project()
            db_project["project_name"] = form.project_name.data
            db_project["project_type"] = form.project_type.data
            try:
                db_project["module_list"] = form.module_list.data
            except:
                db_project["module_list"] = []
            try:
                db_project["svn_list"] = form.svn_list.data.split(',')
            except:
                db_project["svn_list"] = []
            db_project["status"] = form.status.data
            db_project["desc"] = form.desc.data
            db_project["creation"] = datetime.datetime.now()
            db.Project.find_and_modify({"_id": bson.objectid.ObjectId(slug)}, db_project)
            flash(form.project_name.data + (u'更新成功！'))
        else:
            flash(u"更新项目错误，请检查相关字段！")
        return redirect(url_for('project.project_edit', slug=slug))


class project_del(MethodView):
    def get(self, slug):
        db_project = db.Project.find({"_id": bson.objectid.ObjectId(slug)})
        project_name = db_project[0]["project_name"]
        if db_project.count():
            db.project.remove({"_id": bson.objectid.ObjectId(slug)})
            flash(u'删除项目' + project_name + u'成功！')
        else:
            flash(u'您要删除的项目' + project_name + u'不存在！')
        return redirect(url_for('project.project'))


class ops_deploy(MethodView):
    def get(self):
        return render_template('project/ops_deploy.html', title=(u'项目管理'))


class ops_deploy_json(MethodView):
    def get(self):
        ret_data = query_deploy_info()
        return jsonify(ret_data)


    def post(self):
        post_json = request.get_json()
        req_json = {}

        if post_json.has_key('deploy_module'):
            deploy_module = post_json["deploy_module"]
            req_json["deploy_module"] = deploy_module 
        else:
            req_json["deploy_module"] = ""
            req_json["error"] = "未知的模块名!"
            return jsonify(req_json)

        if post_json.has_key('deploy_host'):
            deploy_host = post_json["deploy_host"]
        else:
            req_json["error"] = "主机名不存在!"
            return jsonify(req_json)

        if post_json.has_key('deploy_script'):
            deploy_script = post_json["deploy_script"]
        else:
            req_json["error"] = "脚本名不存在!"
            return jsonify(req_json)

        if post_json.has_key('deploy_svn'):
            deploy_svn = post_json["deploy_svn"]
        else:
            req_json["error"] = "svn信息不存在!"
            return jsonify(req_json)

        deploy_info = commands.getstatusoutput("""python script/sys_ops_dlop.py -s """+deploy_host+" -t "+deploy_script+" -n "+deploy_svn)
        app.logger.warning("deploy_cmd: "+"""python script/sys_ops_dlop.py -s """+deploy_host+" -t "+deploy_script+" -n "+deploy_svn)
        app.logger.warning("deploy_info: "+str(deploy_info))
        #debug info 
        #time.sleep( 4 )
        #deploy_info = (0, deploy_module)
        #debug info """

        if deploy_info[0] != 0:
            req_json["error"] = "部署出现错误!"
            app.logger.warning("ops_deploy: "+str(deploy_info))
        req_json["deploy_info"] = deploy_info[1]
        #app.logger.warning(req_json)
        #app.logger.warning("deploy_module: "+deploy_module+" deploy_host: "+deploy_host+" deploy_script "+deploy_script+" deploy_svn "+deploy_svn)
        return jsonify(req_json)


# Register the urls
project.add_url_rule('/project/module/', view_func=module.as_view('module'))
project.add_url_rule('/project/module/add', view_func=module_add.as_view('module_add'))
project.add_url_rule('/project/module/edit_<slug>', view_func=module_edit.as_view('module_edit'))
project.add_url_rule('/project/module/del_<slug>', view_func=module_del.as_view('module_del'))

project.add_url_rule('/project/', view_func=List.as_view('project'))
project.add_url_rule('/project/add', view_func=project_add.as_view('project_add'))
project.add_url_rule('/project/edit_<slug>', view_func=project_edit.as_view('project_edit'))
project.add_url_rule('/project/del_<slug>', view_func=project_del.as_view('project_del'))

project.add_url_rule('/project/ops/deploy', view_func=ops_deploy.as_view('ops_deploy'))
project.add_url_rule('/project/ops/deploy_json', view_func=ops_deploy_json.as_view('ops_deploy_json'))
