from resources.manager.auth import ManagerSignupApi, ManagerLoginApi
from resources.customer.auth import CustomerSignupApi, CustomerLoginApi
from resources.customer.profile import EditProfileApi, GetProfileApi
from resources.customer.search import SearchApi
from resources.restaurant.register import RegisterRestaurantApi
from resources.restaurant.edit import EditRestaurantApi
from resources.restaurant.get_all import AllRestaurantsApi
from resources.food.add_item import AddFoodItemApi
from resources.food.remove_item import RemoveFoodItemApi
from resources.food.edit_item import EditFoodItemApi

def initialize_routes(api):
    api.add_resource(ManagerSignupApi, '/manager/signup')  # post
    api.add_resource(ManagerLoginApi, '/manager/login')  # post
    api.add_resource(RegisterRestaurantApi, '/restaurant')  # post
    api.add_resource(AllRestaurantsApi, '/restaurant')  # get
    api.add_resource(EditRestaurantApi, '/restaurant/<id>')  # put
    api.add_resource(AddFoodItemApi, '/restaurant/<id>/foods')  # post
    api.add_resource(RemoveFoodItemApi, '/restaurant/foods/<id>')  # delete
    api.add_resource(EditFoodItemApi, '/restaurant/foods/<id>')  # put
    # api.add_resource(, '/orders/<id>')  # put
    # api.add_resource(, '/restaurant/<id>/foods/<id>/comments/<id>')  # put

    api.add_resource(CustomerSignupApi, '/user/signup')  # post
    api.add_resource(CustomerLoginApi, '/user/login')  # post
    api.add_resource(GetProfileApi, '/user/profile')  # get
    api.add_resource(EditProfileApi, '/user/profile')  # put
    api.add_resource(SearchApi, '/search/<tag>')  # get tag={food, restaurant, area}
    # api.add_resource(, '/orders')  # post
    # api.add_resource(, '/orders/<id>/status')  # get
    # api.add_resource(, '/restaurant/<id>/foods/<id>/comments')  # post