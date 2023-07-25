"""
Module-level docstring briefly describing the purpose of the module.
"""
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from models.almanax import Almanax


class ScrapAlmanax:
    def scheduler(self):
        today = datetime.now()
        last_day_of_month = today.replace(day=28) + timedelta(days=4)
        last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)

        if today == last_day_of_month or True:
            data_for_7_days = []
            for i in range(7):
                date_for_day = today + timedelta(days=i)
                date_string = date_for_day.strftime("%Y-%m-%d")
                url = f'https://www.krosmoz.com/en/almanax/{date_string}'
                almanax_data = self.scrap_data_from_url(url)
                if almanax_data is not None:
                    data_for_7_days.append(almanax_data)
            # Update the cache with the new data
            self.cache_almanax_data(data_for_7_days)
        return data_for_7_days

    def scrap_data_from_url(self, url):
        # Check if the data exist in the cache
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get the date infos from the page
            date = soup.find('div', id='almanax_day')
            date_number = date.find('span', class_='day-number').text
            date_month = date.find('span', class_='day-text').text
            date = date_number + ' ' + date_month

            # Get the bonus infos from the page
            bonus = soup.find('div', class_='mid').text.strip().split('\n', 1)[0]
            bonus = bonus.replace('Bonus:', '').strip()

            # Get the image of the item asked for alamanax
            image = soup.find('div', class_='more-infos-content').find('img')['src']

            # Get the bonus description
            bonus_description = soup.find('div', class_='more').text.strip().split('\n', 1)[0]

            # Create an instance of Almanax
            almanax = Almanax(date, bonus, image, bonus_description)
            return almanax
        else:
            return None
