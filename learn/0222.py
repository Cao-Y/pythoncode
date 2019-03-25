import requests
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

url= 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r=requests.get(url)
print("Status code:",r.status_code)
response = r.json()
#print(response)
print("Total repositories:", response['total_count'])

repos = response['items']
names, stars =[],[]
for repo in repos:
    names.append(repo['name'])
    stars.append(repo['stargazers_count'])

my_style = LS('#333366',base_style=LCS)
chart = pygal.Bar(x_label_rotation=45,style = my_style,show_legend =True)
chart.title = 'Most-star'
chart.x_labels=names

chart.add('',stars)
chart.render_to_file('python_repos.svg')