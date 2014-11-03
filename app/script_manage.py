#-*- coding: UTF-8 -*- 
import os, datetime, bson.objectid
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from wtforms import Form, TextField, validators, SelectField, TextAreaField, BooleanField

from app.db_query import query_server, query_script, query_idc, query_module
from app.models import db
from app import app

myscript = Blueprint('script', __name__, template_folder='templates')
WTF_CSRF_SECRET_KEY = 'QPo3QVT0UyBrPmoqhf'

class ScriptForm(Form):
    script_name = TextField(u'脚本名称', [validators.Required(), validators.Length(min=4, max=25)])
    script_argument = TextField(u'脚本参数')
    script_content = TextAreaField(u'脚本内容')
    script_type = SelectField(u'脚本类型', choices=[('ops-deploy', 'ops-deploy'), ('ops-monitor', 'ops-monitor'), ('ops-log', 'ops-log'), ('ops-data', 'ops-data')])
    desc = TextAreaField(u'备注')

class script(MethodView):
    def get(self):
        db_script = db.Script.find()
        #app.logger.warning('A warning occurred (%d apples)', 42)
        return render_template('script/index.html', title=(u'脚本管理'), scripts=list(db_script))

class script_add(MethodView):
    def get(self):
        form = ScriptForm(request.form)
        return render_template('script/add.html', title=(u'脚本管理'), form=form)

    def post(self):
        form = ScriptForm(request.form)
        if form.validate():
            db_script = db.Script.find({"script_name": form.script_name.data})
            if not db_script.count():
                db_script = db.Script()
                db_script["script_name"] = form.script_name.data
                db_script["script_argument"] = form.script_argument.data
                db_script["script_content"] = form.script_content.data.replace("\r", "")
                db_script["script_type"] = form.script_type.data
                db_script["desc"] = form.desc.data
                db_script["creation"] = datetime.datetime.now()
                db_script["modify"] = datetime.datetime.now()

                #write script file
                with open(("script/" + db_script["script_name"]), 'wb') as f:
                   f.write(db_script["script_content"]) 
                db_script.save()
                flash(db_script["script_name"] + (u'添加成功！'))
            else:
                flash(form.script_name.data + (u'重复！'))
        else:
          flash(u"添加脚本错误，请检查相关字段！")
        return render_template('script/add.html', title=(u'脚本管理'), form=form)

class script_edit(MethodView):
    def get(self, slug):
        form = ScriptForm(request.form)
        db_script = db.Script.find({"_id": bson.objectid.ObjectId(slug)})
        if db_script.count():
            form.script_name.data = db_script[0]["script_name"]
            form.script_argument.data = db_script[0]["script_argument"]
            form.script_content.data = db_script[0]["script_content"]
            form.script_type.data = db_script[0]["script_type"]
            form.desc.data = db_script[0]["desc"]
        else:
            flash(u'您编辑的脚本不存在！')
        return render_template('script/edit.html', title=(u'脚本管理'), slug=slug, form=form)

    def post(self, slug):
        form = ScriptForm(request.form)
        if form.validate() :
            db_script = db.Script()
            db_script["script_name"] = form.script_name.data
            db_script["script_argument"] = form.script_argument.data
            db_script["script_content"] = form.script_content.data.replace("\r", "")
            db_script["script_type"] = form.script_type.data
            db_script["desc"] = form.desc.data
            db_script["modify"] = datetime.datetime.now()

            #write script file
            with open(("script/" + db_script["script_name"]), 'wb') as f:
               f.write(db_script["script_content"])
            db.Script.find_and_modify({"_id": bson.objectid.ObjectId(slug)}, {'$set': db_script})
            #app.logger.warning(dir(db_script.update.__doc__))
            #db_script.update({'$set': {"_id": bson.objectid.ObjectId(slug)}})
            flash(form.script_name.data + (u'更新成功！'))
        else:
            flash(u"更新脚本错误，请检查相关字段！")
        return redirect(url_for('script.script_edit', slug=slug))

class script_del(MethodView):
    def get(self, slug):
        db_script = db.Script.find({"_id": bson.objectid.ObjectId(slug)})
        script_name = db_script[0]["script_name"]
        if db_script.count():
            db.script.remove({"_id": bson.objectid.ObjectId(slug)})
            flash(u'删除脚本' + script_name + u'成功！')
        else:
            flash(u'您要删除的脚本' + script_name + u'不存在！')
        return redirect(url_for('script.script'))

# Register the urls
myscript.add_url_rule('/script/', view_func=script.as_view('script'))
myscript.add_url_rule('/script/add', view_func=script_add.as_view('script_add'))
myscript.add_url_rule('/script/edit_<slug>', view_func=script_edit.as_view('script_edit'))
myscript.add_url_rule('/script/del_<slug>', view_func=script_del.as_view('script_del'))
