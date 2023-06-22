
class Scrapped_item_data():
    def __init__(self, id, image, name, type, level, description, stats, recipe):
        self.id = id
        self.image = image
        self.name = name
        self.type = type
        self.level = level
        self.description = description
        self.stats = stats
        self.recipe = recipe

    def __dict__(self):
        return self.__dict__