import re
import requests
from bs4 import BeautifulSoup

website = "https://www.vulnhub.com"

# <a href="/entry/web-machine-n7,756/">Web Machine: (N7)</a>
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'html.parser')

#detectar todo lo que va depués de "/---/"
guide_machine = re.compile(r"/entry/[\w-]*")
guide_author = re.compile(r"/author/[\w-]*")

links = soup.find_all('a', href=True)

machine_names = []
machine_dates = []
machine_authors = []

for link in links:
    href = link['href']
    if guide_machine.match(href):
        link_text = link.get_text(strip=True)
        if re.match(r'\d{2} \w{3} \d{4}', link_text):
            machine_dates.append(link_text)
        else:
            machine_names.append(link_text)
    elif guide_author.match(href):
        machine_authors.append(link.get_text(strip=True))

not_repeated_machines = list(set(machine_names))
not_repeated_dates = list(set(machine_dates))
not_repeated_authors = list(set(machine_authors))

print("Máquinas únicas:", not_repeated_machines)
print("Fechas únicas:", not_repeated_dates)
print("Autores únicos:", not_repeated_authors)

# final_machines =[]
# for i in not_repeated:
#     name_m = i.replace("/entry/","")
#     final_machines.append(name_m)
#     print(name_m)

# last_machine = "noob-1"
# exist_last_machine = False

# for a in final_machines:
#     if a == last_machine:
#         exist_last_machine = True
#         break

# if exist_last_machine == True:
#     print("***There is no new machine***")
# else:
#     print("***There are new machines***")