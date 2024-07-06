import re
import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url):
    result = requests.get(url)
    content = result.text
    soup = BeautifulSoup(content, 'html.parser')

    data_all = []
    unique_data = {
        'Machine Name': set(),
        'Machine Date': set(),
        'Author': set()
    }

    cards = soup.find_all('div', class_='card')

    for card in cards:
        link = card.find('a', href=True)
        if link:
            href = link['href']
            link_text = link.get_text(strip=True)

            if "/entry/" in href:
                machine_date = ""
                machine_name = ""
                date_element = card.find('div', class_='card-date')
                name_element = card.find('div', class_='card-title')

                if date_element:
                    machine_date = date_element.get_text(strip=True)
                if name_element:
                    machine_name = name_element.get_text(strip=True)

                data_all.append({
                    'Machine Name': machine_name,
                    'Machine Date': machine_date,
                    'Author': "" 
                })
                unique_data['Machine Name'].add(machine_name)
                unique_data['Machine Date'].add(machine_date)

            elif "/author/" in href:
                machine_author = link_text.strip()

                if data_all:
                    data_all[-1]['Author'] = machine_author

                unique_data['Author'].add(machine_author)

    return data_all, unique_data

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
# patterns = {
#     'machine_name': {
#         'selector': 'div.card-title',  # Selector CSS
#         'list': []
#     },
#     'machine_date': {
#         'selector': 'div.card-date',  # Selector CSS
#         'list': []
#     },
#     'author': {
#         'selector': 'div.card-author',  # Selector CSS
#         'list': []
#     }
# }

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

# for key, info in patterns.items():
#     elements = soup.select(info['selector'])
#     for element in elements:
#         if key == 'machine_name':
#             link = element.find('a', href=True)
#             if link:
#                 info['list'].append(link.get_text(strip=True))
#         elif key == 'machine_date':
#             info['list'].append(element.get_text(strip=True))
#         elif key == 'author':
#             info['list'].append(element.get_text(strip=True))

# for info in patterns.values():
#     info['list'] = list(set(info['list']))

#final_machine_names = [name.replace("/entry/", "") for name in patterns[re.compile(r"/entry/[\w-]*")]['name_list']]
#last_machine = "noob-1"
#exist_last_machine = last_machine in final_machine_names

#print("Máquinas únicas:", patterns['machine_name'])
#print("Fechas únicas:", patterns[re.compile(r"/entry/[\w-]*")]['date_list'])
#print("Autores únicos:", patterns[re.compile(r"/author/[\w-]*")]['list'])

# if exist_last_machine == True:
#     print("***There is no new machine***")
# else:
#     print("***There are new machines***")

# Export in CSV
def export_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Machine Name', 'Machine Date', 'Author']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()

        for entry in data:
            csvwriter.writerow({
                'Machine Name': entry['Machine Name'],
                'Machine Date': entry['Machine Date'],
                'Author': entry['Author']
            })

def export_unique_to_csv(unique_data, filename_prefix):
    for key, values in unique_data.items():
        filename = f'{filename_prefix}_{key.lower().replace(" ", "_")}_unique.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([key])
            csvwriter.writerows([[value] for value in values])

if __name__ == "__main__":
    website = "https://www.vulnhub.com"
    data_all, unique_data = scrape_website(website)

    export_to_csv(data_all, 'data_all.csv')
    export_unique_to_csv(unique_data, 'unique_values')
    print(data_all)