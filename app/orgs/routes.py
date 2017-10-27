from flask import render_template, request, g, session, redirect, url_for
from . import orgs
from ..apicode import apiresult
from app import redis_store
import json, pickle


@orgs.route('/', methods=['GET', 'POST'])
def index():
    redis_store.set('json_data', None)
    redis_store.set('newsortedlist',None)
    if request.method == 'POST':
        org_name = request.form['orgsearch'].strip().title()
        if not org_name:
            error = "What do you want to search?"
            return render_template('orgs/index.html', error=error)
        return redirect(url_for('orgs.sort_by_name',org_name=org_name))
    return render_template('orgs/index.html')


@orgs.route('/SortByName/<org_name>')
def sort_by_name(org_name):
    json_obj = apiresult(org_name)
    if len(json_obj) !=0:
        try:
            json_obj['message']
            context_dict = {"message":"No such organisation exists!"}
            return render_template('orgs/results.html',context_dict=context_dict)
        except:
            l = []
            sorted_list = sorted(json_obj, key=lambda k: k['name'].title(), reverse = False)
            for row in sorted_list:
                l.append(str(row['language']))
            newlist = list(set(l))
            if 'None' in newlist:
                newlist = ['Not Assigned' if x=='None' else x for x in newlist]
            newsortedlist = sorted(newlist)
            return render_template('orgs/sortbyname.html',org_name=org_name,sorted_list=sorted_list,newsortedlist=newsortedlist)
    else:
        context_dict = {"message":"No such organisation exists!"}
        return render_template('orgs/results.html',context_dict=context_dict)



@orgs.route('/SortByDate/<org_name>')
def sort_by_date(org_name):
    json_obj = json.loads(redis_store.get('json_data'))
    sorted_list = sorted(json_obj, key=lambda k: k['created_at'], reverse = True)
    for row in sorted_list:
        l.append(str(row['language']))
    newlist = list(set(l))
    if 'None' in newlist:
        newlist = ['Not Assigned' if x=='None' else x for x in newlist]
    newsortedlist = sorted(newlist)
    return render_template('orgs/sortbydate.html',org_name=org_name,sorted_list=sorted_list,newsortedlist=newsortedlist)

@orgs.route('/SortByIssues/<org_name>')
def sort_by_issues(org_name):
    json_obj = json.loads(redis_store.get('json_data'))
    sorted_list = sorted(json_obj, key=lambda k: k['open_issues'], reverse = True)
    for row in sorted_list:
        l.append(str(row['language']))
    newlist = list(set(l))
    if 'None' in newlist:
        newlist = ['Not Assigned' if x=='None' else x for x in newlist]
    newsortedlist = sorted(newlist)
    return render_template('orgs/sortbyissues.html',org_name=org_name,sorted_list=sorted_list,newsortedlist=newsortedlist)

@orgs.route('/SortByLanguage/<org_name>/<item>')
def sort_by_language(org_name,item):
    json_obj = json.loads(redis_store.get('json_data'))
    sorted_list = sorted(json_obj, key=lambda k: k['name'].title(), reverse = False)
    for row in sorted_list:
        l.append(str(row['language']))
    newlist = list(set(l))
    if 'None' in newlist:
        newlist = ['Not Assigned' if x=='None' else x for x in newlist]
    newsortedlist = sorted(newlist)
    return render_template('orgs/sortbylanguage.html',org_name=org_name,sorted_list=sorted_list,item=item,newsortedlist=newsortedlist)
