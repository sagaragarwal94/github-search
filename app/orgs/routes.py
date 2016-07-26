from flask import render_template, request, g, session, redirect, url_for
from . import orgs
import requests
from ..apicode import apiresult

@orgs.route('/', methods=['GET', 'POST'])
def index():
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
    try:
        json_obj['message']
        context_dict = {"message":"No such organisation exists!"}
        return render_template('orgs/results.html',context_dict=context_dict)
    except:
        sorted_list = sorted(json_obj, key=lambda k: k['name'], reverse = False)
        return render_template('orgs/sortbyname.html',org_name=org_name,sorted_list=sorted_list)



@orgs.route('/SortByDate/<org_name>')
def sort_by_date(org_name):
    json_obj = apiresult(org_name)
    sorted_list = sorted(json_obj, key=lambda k: k['created_at'], reverse = True)
    return render_template('orgs/sortbydate.html',org_name=org_name,sorted_list=sorted_list)

@orgs.route('/SortByIssues/<org_name>')
def sort_by_issues(org_name):
    json_obj = apiresult(org_name)
    sorted_list = sorted(json_obj, key=lambda k: k['open_issues'], reverse = True)
    return render_template('orgs/sortbyissues.html',org_name=org_name,sorted_list=sorted_list)