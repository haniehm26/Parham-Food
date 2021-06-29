from bson.objectid import ObjectId

class Food:

    def __init__(self, record, id):
        self.name = record['name']
        self.restaurant_id = record['restaurant_id']
        self.cost = record['cost']
        self.orderable = record['orderable']
        self.number = record['number']
        self.id = str(id)


    def to_json(self):
        return {'name': self.name,
                'restaurant_id': self.restaurant_id,
                'cost': self.cost,
                'orderable': self.orderable,
                'number': self.number,
                'id': self.id}