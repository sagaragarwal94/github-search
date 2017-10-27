import requests
#import json

def apiresult(org_name):
    #'https://api.github.com/orgs/mozilla/repos?page=2&per_page=100'
    #api_url = "https://api.github.com/orgs/"+ org_name + "/repos?per_page=5"
    #curl 'https://api.github.com/users/whatever?client_id=xxxx&client_secret=yyyy'
    api_url = "https://api.github.com/orgs/"+ org_name + "/repos"
    r= requests.get(api_url)
    json_data = r.json()
    return json_data

def userapiresult(user_name):
    api_url = "https://api.github.com/users/"+ user_name + "/repos"
    r= requests.get(api_url)
    json_obj = r.json()
    return json_obj
