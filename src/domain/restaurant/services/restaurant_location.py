from src.domain.order.entities.order import Location
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import MenuProduct, RestaurantLocation

from math import sin, cos, acos, pi


class RestaurantService:
    def change_available_status(self, menu_product: MenuProduct) -> MenuProduct:
        if menu_product.status is MenuProductStatus.not_available:
            menu_product.status = MenuProductStatus.available
        else:
            menu_product.status = MenuProductStatus.not_available
        return menu_product

    def get_nearest_restaurant(
            self, user_location: Location,
            restaurants_locations: list[RestaurantLocation],
    ) -> RestaurantLocation:
        length = 0
        location = None
        for r_loc in restaurants_locations:
            calculate_length = self.length_between_user_location_and_restaurant(
                user_location=user_location,
                restaurant_location=Location(
                    latitude=r_loc.latitude,
                    longitude=r_loc.longitude,
                ),
            )
            if location is None:
                location = r_loc
                length = calculate_length
            if length > calculate_length:
                location = r_loc
                length = calculate_length
        return location

    def length_between_user_location_and_restaurant(
            self, user_location: Location, restaurant_location: Location,
    ) -> float:
        theta = user_location.longitude - restaurant_location.longitude

        distance = 60 * 1.1515 * self.rad2deg(
            acos(
                (sin(self.deg2rad(user_location.latitude)) *
                 sin(self.deg2rad(restaurant_location.latitude))) +
                (cos(self.deg2rad(user_location.latitude)) *
                 cos(self.deg2rad(restaurant_location.latitude)) *
                 cos(self.deg2rad(theta)))
            )
        )
        return round(distance * 1.609344, 2)

    def rad2deg(self, radians: float):
        degrees = radians * 180 / pi
        return degrees

    def deg2rad(self, degrees: float):
        radians = degrees * pi / 180
        return radians
