class CsvContent:
    guid = ""
    name = ""
    first = ""
    last = ""
    email = ""
    value = ""
    date = ""
    phone = ""
    age = ""
    state = ""
    street = ""

    def __init__(self, guid, name, first, last, email, value, date, phone, age, state, street): 
        self.guid = guid
        self.name = name
        self.first = first
        self.last = last
        self.email = email
        self.value = value
        self.date = date
        self.phone = phone
        self.age = age
        self.state = state
        self.age = name
        self.state = state
        self.street = street

def createCsvContent(guid, name, first, last, email, value, date, phone, age, state, street):
    csvContent = CsvContent(guid, name, first, last, email, value, date, phone, age, state, street)
    return csvContent