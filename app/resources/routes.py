from resources.manager.auth import SignupApi
# from resources.manager.auth import Alaki
from resources.restaurant.register import RegisterRestaurant

def initialize_routes(api):
    api.add_resource(SignupApi, '/manager/login')  # post
    api.add_resource(RegisterRestaurant, '/restaurant')  # post
    # api.add_resource(, '/restaurant/<id>')  # put
    # api.add_resource(, '/restaurant/<id>/foods')  # post
    # api.add_resource(, '/restaurant/<id>/foods/<id>')  # delete
    # api.add_resource(, '/restaurant/<id>/foods/<id>')  # put
    # api.add_resource(, '/orders/<id>')  # put
    # api.add_resource(, '/restaurant/<id>/foods/<id>/comments/<id>')  # put

    # api.add_resource(, '/user/login')  # post
    # api.add_resource(, '/user/<id>/profile')  # put
    # api.add_resource(, '/search/food')  # get
    # api.add_resource(, '/search/restaurant')  # get
    # api.add_resource(, '/search/area')  # get
    # api.add_resource(, '/orders')  # post
    # api.add_resource(, '/orders/<id>/status')  # get
    # api.add_resource(, '/restaurant/<id>/foods/<id>/comments')  # post
    # api.add_resource(Alaki, '/')  # get
