from filecmp import cmp


class Country:
    def __init__(self, name, year, population):
        self.name = name
        self.year = year
        self.population = population

    def __str__(self):
        return f"{self.name},{self.year},{self.population}"

    def __lt__(self, nxt):
        return self.population < nxt.population

    def __cmp__(self, nxt):
        return cmp(self.population, nxt.population)
