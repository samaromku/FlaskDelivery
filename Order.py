class Order:
    id = None
    title = None
    description = None
    created = None
    dead_line = None
    address = None

    def __init__(self, title, description, created, dead_line, address):
        self.title = title
        self.description = description
        self.created = created
        self.dead_line = dead_line
        self.address = address
