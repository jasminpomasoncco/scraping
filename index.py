import re
import requests
from bs4 import BeautifulSoup
import csv

website = "https://www.vulnhub.com"

# example: <a href="/entry/web-machine-n7,756/">Web Machine: (N7)</a>
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'html.parser')

# Define patterns and associated lists
# patterns = {
#     re.compile(r"/entry/[\w-]*"): {
#         'date_pattern': re.compile(r'\d{2} \w{3} \d{4}'),
#         'name_list': [],
#         'date_list': []
#     },
#     re.compile(r"/author/[\w-]*"): {
#         'list': []
#     }
# }
# Define patterns and associated lists
patterns = {
    'machine_name': {
        'selector': 'div.card-title',  # Selector CSS
        'list': []
    },
    'machine_date': {
        'selector': 'div.card-date',  # Selector CSS
        'list': []
    },
    'author': {
        'selector': 'div.card-author',  # Selector CSS
        'list': []
    }
}

# links = soup.find_all('a', href=True)

# machine_names = []
# machine_dates = []
# machine_authors = []

# for link in links:
#     href = link['href']
#     link_text = link.get_text(strip=True)

#     for pattern, storage in patterns.items():
#         if pattern.match(href):
#             if 'date_pattern' in storage and storage['date_pattern'].match(link_text):
#                     storage['date_list'].append(link_text)
#             elif 'name_list' in storage:
#                     storage['name_list'].append(link_text)
#             elif 'list' in storage:
#                     storage['list'].append(link_text)

# for storage in patterns.values():
#     if 'name_list' in storage:
#             storage['name_list'] = list(set(storage['name_list']))
#     if 'date_list' in storage:
#             storage['date_list'] = list(set(storage['date_list']))
#     if 'list' in storage:
#             storage['list'] = list(set(storage['list']))

for key, info in patterns.items():
    elements = soup.select(info['selector'])
    for element in elements:
        if key == 'machine_name':
            link = element.find('a', href=True)
            if link:
                info['list'].append(link.get_text(strip=True))
        elif key == 'machine_date':
            info['list'].append(element.get_text(strip=True))
        elif key == 'author':
            info['list'].append(element.get_text(strip=True))

for info in patterns.values():
    info['list'] = list(set(info['list']))

#final_machine_names = [name.replace("/entry/", "") for name in patterns[re.compile(r"/entry/[\w-]*")]['name_list']]
#last_machine = "noob-1"
#exist_last_machine = last_machine in final_machine_names

print("Máquinas únicas:", patterns['machine_name'])
#print("Fechas únicas:", patterns[re.compile(r"/entry/[\w-]*")]['date_list'])
#print("Autores únicos:", patterns[re.compile(r"/author/[\w-]*")]['list'])

# if exist_last_machine == True:
#     print("***There is no new machine***")
# else:
#     print("***There are new machines***")

# Export in CSV
with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Machine Name', 'Machine Date', 'Author'])

    max_length = max(len(patterns['machine_name']['list']), len(patterns['machine_date']['list']), len(patterns['author']['list']))

    for i in range(max_length):
        name = patterns['machine_name']['list'][i] if i < len(patterns['machine_name']['list']) else ''
        date = patterns['machine_date']['list'][i] if i < len(patterns['machine_date']['list']) else ''
        author = patterns['author']['list'][i] if i < len(patterns['author']['list']) else ''
        csvwriter.writerow([name, date, author])