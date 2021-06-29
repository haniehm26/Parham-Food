class Customer:
    
    def __init__(self, record):
        self.first_name = record['first_name']
        self.last_name = record['last_name']
        self.area = record['area']
        self.address = record['address']
        self.creadit = record['credit']
        self.orders_history = record['orders_history']
        self.favorits = record['favorits']
        self.id = str(record['_id'])


    def to_json(self):
        return {'first_name':self.first_name,
                'last_name':self.last_name,
                'area':self.area,
                'address':self.address,
                'creadit':self.creadit,
                'orders_history':self.orders_history,
                'favorits':self.favorits,
                'id':self.id}