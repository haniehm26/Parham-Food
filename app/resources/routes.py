from resources.manager.auth import SignupApi, LoginApi
from resources.restaurant.register import RegisterRestaurantApi
from resources.restaurant.edit import EditRestaurantApi
from resources.restaurant.get_all import AllRestaurantsApi
from resources.food.add_item import AddFoodItemApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/manager/signup')  # post
    api.add_resource(LoginApi, '/manager/login')  # post
    api.add_resource(RegisterRestaurantApi, '/restaurant')  # post
    api.add_resource(AllRestaurantsApi, '/restaurant')  # get
    api.add_resource(EditRestaurantApi, '/restaurant')  # put
    # api.add_resource(AddFoodItemApi, '/restaurant/foods')  # post
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
