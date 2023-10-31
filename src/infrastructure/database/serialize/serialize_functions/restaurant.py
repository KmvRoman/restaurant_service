from src.domain.restaurant.entities.restaurant_view import RestaurantView, RestaurantLocation, RestaurantId, Category
from src.infrastructure.database.serialize.models.restaurant import ShowRestaurantInfo, ShowCategory


def serialize_restaurant_info(payload: list[tuple]) -> RestaurantView:
    restaurant_id: int | None = None
    name: str | None = None
    description: str | None = None
    locations = []
    for res in payload:
        res_info = ShowRestaurantInfo(*res)
        if restaurant_id is None:
            restaurant_id = res_info.restaurant_id
            name = res_info.name
            description = res_info.description
        location = RestaurantLocation(
            id=res_info.location_id, address=res_info.address,
            latitude=res_info.latitude, longitude=res_info.longitude,
        )
        if location not in locations:
            locations.append(location)
    return RestaurantView(id=RestaurantId(restaurant_id), name=name, description=description, location=locations)


def serialize_category(payload: list[tuple]) -> list[Category]:
    categories = []
    for category in payload:
        cat = ShowCategory(*category)
        categories.append(Category(id=cat.id, category=cat.category))
    return categories
