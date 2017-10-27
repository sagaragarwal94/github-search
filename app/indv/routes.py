from flask import render_template, request, g, session, redirect, url_for
from . import indv
import requests
from ..apicode import apiresult, userapiresult
from app import redis_store
import json, pickle

@indv.route('/', methods=['GET', 'POST'])
def index():
    redis_store.set('json_data', None)
    if request.method == 'POST':
        user_name = request.form['indvsearch'].strip()
        print user_name
        if not user_name:
            error = "What do you want to search?"
            return render_template('indv/index.html', error=error)
        return redirect(url_for('indv.sort_by_name',user_name=user_name))
    return render_template('indv/index.html')

@indv.route('/SortByName/<user_name>')
def sort_by_name(user_name):
    json_data = userapiresult(user_name)
    json_data = json.dumps(json_data)
    redis_store.set('json_data',json_data)
    json_obj = json.loads(redis_store.get('json_data'))
    if len(json_obj) !=0:
        try:
            json_obj['message']
            context_dict = {"message":"No such user exists!"}
            return render_template('indv/results.html',context_dict=context_dict)
        except:
            sorted_list = sorted(json_obj, key=lambda k: k['name'].title(), reverse = False)
            return render_template('indv/sortbyname.html',user_name=user_name,sorted_list=sorted_list)
    else:
        context_dict = {"message":"No such user exists!"}
        return render_template('indv/results.html',context_dict=context_dict)


@indv.route('/SortByDate/<user_name>')
def sort_by_date(user_name):
    json_obj = json.loads(redis_store.get('json_data'))
    sorted_list = sorted(json_obj, key=lambda k: k['created_at'], reverse = True)
    return render_template('indv/sortbydate.html',user_name=user_name,sorted_list=sorted_list)

@indv.route('/SortByIssues/<user_name>')
def sort_by_issues(user_name):
    json_obj = json.loads(redis_store.get('json_data'))
    sorted_list = sorted(json_obj, key=lambda k: k['open_issues_count'], reverse = True)
    return render_template('indv/sortbyissues.html',user_name=user_name,sorted_list=sorted_list)

@indv.route('/SortByStars/<user_name>')
def sort_by_stars(user_name):
    json_obj = json.loads(redis_store.get('json_data'))
    sorted_list = sorted(json_obj, key=lambda k: k['stargazers_count'], reverse = True)
    return render_template('indv/sortbystars.html',user_name=user_name,sorted_list=sorted_list)
