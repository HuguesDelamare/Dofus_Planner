class Almanax:
    def __init__(self, date: str, bonus: str, image: str, description: str) -> None:
        self.date = date
        self.bonus = bonus
        self.image = image
        self.description = description

    def __str__(self) -> str:
        return f'{self.date} {self.bonus} {self.image} {self.description}'
