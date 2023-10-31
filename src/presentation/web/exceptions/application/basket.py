class WebApplicationError(Exception):
    pass


class BasketIsEmpty(WebApplicationError):
    def __init__(self):
        self.message = "Current basket is empty"


class LocationsInvalid(WebApplicationError):
    def __init__(self):
        self.message = "Route by locations not found"
