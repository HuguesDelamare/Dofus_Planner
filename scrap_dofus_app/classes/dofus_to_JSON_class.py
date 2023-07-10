"""
Module-level docstring briefly describing the purpose of the module.
"""

import base64
import time
import re
import json
import os
from bs4 import BeautifulSoup
import requests


# Class to scrap data from Dofus website and save it to JSON file
class DofusItemScrapping:
    """
    This is a sample class that demonstrates the usage of a class docstring.

    Attributes:
        page (int): This is the first attribute.

    Methods:
        get_data_from_url(): This is the first method.
        data_to_json_file(): This is the second method.
        scrapping_data(): This is the third method.
    """

    def __init__(self):
        self.page = 1

    def get_data_for_JSON(self, url):
        """
        This is the first method of DofusItemScrapping.

        Returns:
            str: A string representing the result of the method.
        """
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # Item id
            item_id = int("".join(re.findall(r"\d", url)))
            # Item name
            item_name = (
                soup.find(class_="ak-title-container ak-backlink")
                .find("h1")
                .text.replace("\n", "")
            )
            # Item image
            item_image = soup.find(class_="ak-encyclo-detail-illu").find("img")["src"]
            # Fetch the item image data
            image_response = requests.get(item_image)
            if image_response.status_code == 200:
                # Encode the image data to Base64
                item_image_data = base64.b64encode(image_response.content).decode('utf-8')
            else:
                print(f"Failed to retrieve item image. Status code: {image_response.status_code}")
                item_image_data = None

            item = {
                "id": item_id,
                "name": item_name,
                "image": item_image_data,
            }
            return item
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None

    def set_json_file(self):
        """
        This is the second method of DofusItemScrapping.

        Returns:
            str: A string representing the result of the method.
        """
        # Check if the JSON file exists
        if not os.path.isfile("items.json"):
            # Create an empty JSON file
            with open("items.json", "w", encoding='utf-8') as file:
                json.dump([], file)
        while self.page <= 102:
            url = (
                "https://www.dofus.com/fr/mmorpg/encyclopedie/equipements?page="
                + str(self.page)
            )
            response = requests.get(url, timeout=5)
            json_data = []

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # Find the table with the specified class name
                table = soup.find("table", class_="ak-table ak-responsivetable")

                # Find all the <tr> elements within the <tbody>
                tr_elements = table.tbody.find_all("tr")

                for tr in tr_elements:
                    if tr:
                        # Get the URL in the <a> tag
                        span = tr.find("span", class_="ak-linker")
                        if span:
                            link = span.find("a")
                            if link and "href" in link.attrs:
                                url = "https://www.dofus.com" + link["href"]
                                print(url)
                                # Get data from the item
                                item = self.get_data_for_JSON(url)
                                if item is None:
                                    print("Failed to retrieve data.)")
                                    continue
                                else:
                                    print("Data retrieved successfully.")
                                    # Append data to the JSON data list
                                    json_data.append(item)
                        else:
                            print("Link not found")
                    else:
                        print("No item available")

                # Save data to JSON file
                self.data_to_json_file(json_data)

                # Going to the next page
                self.page += 1
                # Timer to slow down and avoid getting banned by the website
                time.sleep(30)
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")

    def data_to_json_file(self, items):
        """
        This is the second method of DofusItemScrapping.

        Returns:
            str: A string representing the result of the method.
        """

        # Open JSON file
        with open("items.json", "r", encoding='utf-8') as file:
            data = json.load(file)

        # Add items to the JSON data list
        data.extend(items)

        # Save data to JSON file
        with open("items.json", "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        # Print the number of items scrapped
        print(f"Page {self.page} scrapped successfully.")

    def get_item_from_url(self, url):
        """
        This is the first method of DofusItemScrapping.

        Returns:
            str: A string representing the result of the method.
        """

        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # Item id
            item_id = int("".join(re.findall(r"\d", url)))
            # Item name
            item_name = (
                soup.find(class_="ak-title-container ak-backlink")
                .find("h1")
                .text.replace("\n", "")
            )
            # Item image
            item_image = soup.find(class_="ak-encyclo-detail-illu").find("img")["src"]
            # Fetch the item image data
            image_response = requests.get(item_image)
            if image_response.status_code == 200:
                # Encode the image data to Base64
                item_image_data = base64.b64encode(image_response.content).decode('utf-8')
            else:
                print(f"Failed to retrieve item image. Status code: {image_response.status_code}")
                item_image_data = None
            # Item type
            item_type = (
                soup.find(class_="ak-encyclo-detail-type col-xs-6")
                .find("span")
                .text.replace("\n", "")
            )
            # Item level
            item_level = soup.find(
                class_="ak-encyclo-detail-level col-xs-6 text-right"
            ).text.replace("\n", "")
            item_level = int(re.findall(r'\d+', item_level)[0])
            # Item description
            item_description = soup.findAll(class_="ak-panel-content")[1].text.replace(
                "\n", ""
            )
            # Item stats
            item_stats = []
            try:
                item_stats_container = soup.find(
                    class_="ak-container ak-content-list ak-displaymode-col"
                )
                div_elements = item_stats_container.find_all(class_="ak-list-element")

                for element in div_elements:
                    if element:
                        stat = element.find(class_="ak-title").text.strip()
                        stat = stat.replace("\n", "")
                        item_stats.append(stat)
                    else:
                        print("no stat available")
            except AttributeError:
                item_stats.append("No stat available")

            # Item recipe ingredients
            item_recipe = {}
            item_recipe["recipe"] = []
            try:
                item_recipe_container = soup.find(
                    class_="ak-container ak-content-list ak-displaymode-image-col"
                )
                row_containers = item_recipe_container.find(class_="row ak-container")
                for row_container in row_containers:
                    list_elements = row_container.findAll(class_="ak-list-element")
                    for list_element in list_elements:
                        try:
                            data = {"name": "", "quantity": "", "image": ""}
                            # Recipe ingredient name
                            data["name"] = (
                                list_element.find("div", class_="ak-content")
                                .find("span", class_="ak-linker")
                                .text
                                .strip()
                                .replace("\n", "")
                            )
                            # Recipe ingredient quantity
                            data["quantity"] = int(
                                list_element.find(class_="ak-front")
                                .text
                                .replace("x", "")
                                .strip()
                            )
                            # Recipe ingredient image
                            data["image"] = list_element.find(class_="ak-linker").find("img")["src"]
                            # Fetch the image data from the URL
                            response = requests.get(data["image"])
                            if response.status_code == 200:
                                # Encode the image data as Base64 and store it in the JSON
                                data["image"] = base64.b64encode(response.content).decode("utf-8")
                            else:
                                # If fetching the image fails, set it to an empty string or handle the error as desired
                                data["image"] = ""
                            # Append the data to the item_recipe dictionary
                            item_recipe["recipe"].append(data)
                        except AttributeError:
                            continue
            except AttributeError:
                print("No recipe available")
                item_recipe["recipe"] = "No recipe available"
            except TypeError:
                print("No recipe available")
                item_recipe["recipe"] = "No recipe available"
            item = {
                "id": item_id,
                "name": item_name,
                "image": item_image_data,
                "type": item_type,
                "level": item_level,
                "description": item_description,
                "stats": item_stats,
                "recipe": item_recipe["recipe"],
            }
            print(f"Item {item_id} scrapped successfully.")
            return item
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
