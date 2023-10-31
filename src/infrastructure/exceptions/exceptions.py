class InfrastructureError(Exception):
    pass


class AddressError(InfrastructureError):
    pass


class WrongLocations(InfrastructureError):
    pass
