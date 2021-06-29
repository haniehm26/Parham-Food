class Restaurant:
    
    def __init__(self, name, area, address, service_areas, work_hour, deliver_cost, foods, id):
        self.name = name
        self.area = area
        self.address = address
        self.service_areas = service_areas
        self.work_hour = work_hour
        self.deliver_cost = deliver_cost
        self.foods = foods
        self.id = id

    def to_json(self):
        return {'name': self.name, 'area': self.area,
                'address' : self.address, 'service_areas' : self.service_areas,
                'work_hour' : self.work_hour, 'deliver_cost' : self.deliver_cost,
                'foods' : self.foods, 'id' : self.id}