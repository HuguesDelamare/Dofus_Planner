import requests
from bs4 import BeautifulSoup
import time
import re 
import csv

class Dofus_item_Scrapping:
    def __init__(self, page=1):
        self.page = page
        self.Scrapping_data()

    def Get_data_from_url(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Item id
            item_id = ''.join(re.findall(r'\d', url))

            # Item name
            item_name = soup.find(class_='ak-title-container ak-backlink').find('h1').text.replace('\n', '')

            # Item image
            item_image = soup.find(class_='ak-encyclo-detail-illu').find('img')['src']
            
            # Item type
            item_type = soup.find(class_='ak-encyclo-detail-type col-xs-6').find('span').text.replace('\n', '')

            # Item level
            item_level = soup.find(class_='ak-encyclo-detail-level col-xs-6 text-right').text.replace('\n', '')

            # Item description
            item_description = soup.findAll(class_='ak-panel-content')[1].text.replace('\n', '')

            # Item stats
            item_stats = []
            item_stats_container = soup.find(class_='ak-container ak-content-list ak-displaymode-col')
            div_elements = item_stats_container.find_all(class_='ak-list-element')

            for element in div_elements:
                if element:
                    stat = element.find(class_='ak-title').text.strip()
                    stat = stat.replace('\n', '')
                    item_stats.append(stat)
                else:
                    print('no stat available')
            
            # Item recipe ingredients
            item_recipe = {}
            item_recipe['recipe'] = []
            item_recipe_container = soup.find(class_='ak-container ak-content-list ak-displaymode-image-col')
            row_containers = item_recipe_container.find(class_='row ak-container')

            for row_container in row_containers:
                list_elements = row_container.findAll(class_='ak-list-element')
                
                for list_element in list_elements:
                    try:
                        data = {
                            'name': '',
                            'quantity': '',
                            'image': ''
                        }

                        # Recipe ingredient name
                        data['name'] = list_element.find('div', class_='ak-content').find('span', class_='ak-linker').text.strip().replace('\n', '')

                        # Recipe ingredient quantity
                        data['quantity'] = list_element.find(class_='ak-front').text.strip().replace('\n', '')
                        
                        # Recipe ingredient image
                        data['image'] = list_element.find(class_='ak-linker').find('img')['src']

                        # Append the data to the item_recipe dictionary
                        item_recipe['recipe'].append(data)
                    except AttributeError:
                        continue

            item = {
                'id': item_id,
                'name': item_name,
                'image': item_image,
                'type': item_type,
                'level': item_level,
                'description': item_description,
                'stats': item_stats,
                'recipe': item_recipe['recipe']
            }

            self.Data_to_CSV_file(item)

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            

    # Save data to CSV file
    def Data_to_CSV_file(self, item):
        with open('data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(item.values())


    def Scrapping_data(self):
        # Start at page 1 and stop at page 102
        while self.page <= 102:
            url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements?page='+str(self.page)
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the table with the specified class name
                table = soup.find('table', class_='ak-table ak-responsivetable')

                # Find all the <tr> elements within the <tbody>
                tr_elements = table.tbody.find_all('tr')

                for tr in tr_elements:
                    if tr:
                        # Get the URL in the <a> tag
                        span = tr.find('span', class_='ak-linker')
                        if span:
                            link = span.find('a')
                            if link and 'href' in link.attrs:
                                url = 'https://www.dofus.com'+link['href']
                                print(url)
                                # Get data from the item
                                self.Get_data_from_url(url)
                                
                        else:
                            print(f"Link not found")
                    else:
                        print(f"No item available")
                # Increment the page number
                self.page += 1

            # Timer to slow down and not get banned by website
            time.sleep(30)
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            