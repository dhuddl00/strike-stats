import requests, json

github_url = "https://api.github.com/user/repos"
data = json.dumps({'name':'strike-stats', 'description':'App to keep track of pitcher performance.'}) 
r = requests.post(github_url, data, auth=('dhuddl00@gmail.com', '*****'))

print r.json
