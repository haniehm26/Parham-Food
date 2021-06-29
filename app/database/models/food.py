class Food:

    def __init__(self, record):
        self.name = record['name']
        self.restaurant_id = record['restaurant_id']
        self.address = record['address']
        self.cost = record['cost']
        self.orderable = record['orderable']
        self.number = record['number']
        self.id = str(record['_id'])


    def to_json(self):
        return {'name': self.name,
                'restaurant_id': self.restaurant_id,
                'address': self.address,
                'cost': self.cost,
                'orderable': self.orderable,
                'number': self.number,
                'id': self.id}