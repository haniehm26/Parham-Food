class Restaurant:
    
    def __init__(self, record):
        self.name = record['name']
        self.area = record['area']
        self.address = record['address']
        self.service_areas = record['service_areas']
        self.work_hour = record['work_hour']
        self.deliver_cost = record['deliver_cost']
        self.foods = record['foods']
        self.id = str(record['_id'])

    def to_json(self):
        return {'name': self.name,
                'area': self.area,
                'address' : self.address,
                'service_areas' : self.service_areas,
                'work_hour' : self.work_hour,
                'deliver_cost' : self.deliver_cost,
                'foods' : self.foods,
                'id' : self.id}