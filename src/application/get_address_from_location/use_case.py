from src.application.common.use_case import UseCase
from src.application.get_address_from_location.dto import (
    GetAddressFromLocationDtoInput, GetAddressFromLocationDtoOutput,
)
from src.application.get_address_from_location.interfaces import AddressFromLocationService


class GetLocationFromAddressCase(UseCase[GetAddressFromLocationDtoInput, GetAddressFromLocationDtoOutput]):
    def __init__(self, address_service: AddressFromLocationService):
        self.address_service = address_service

    async def __call__(self, data: GetAddressFromLocationDtoInput) -> GetAddressFromLocationDtoOutput:
        address = await self.address_service.get_address(location=data.location)
        return GetAddressFromLocationDtoOutput(address=address)
