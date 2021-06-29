class Order:
    
    def __init__(self, record):
        self.foods = record['foods']
        self.time = record['time']
        self.restaurant = record['restaurant']
        self.customer = record['customer']
        self.status = record['status']
        self.sender = record['sender']
        self.id = str(record['_id'])


    def to_json(self):
        return {'foods': self.foods,
                'time': self.time,
                'restaurant' : self.restaurant,
                'customer' : self.customer,
                'status' : self.status,
                'sender' : self.sender,
                'id' : self.id}