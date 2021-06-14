class DateData:
    name = ""
    date = ""

    def __init__(self, name, date): 
        self.name = name
        self.date = date

def createDateData(name, date):
    dateData = DateData(name, date)
    return dateData