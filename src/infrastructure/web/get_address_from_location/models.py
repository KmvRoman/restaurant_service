from pydantic import BaseModel


class Address(BaseModel):
    country_code: str
    formatted: str
    Components: list


class GeocoderMetaData(BaseModel):
    precision: str
    text: str
    kind: str
    Address: Address
    AddressDetails: dict


class metaDataProperty(BaseModel):
    GeocoderMetaData: GeocoderMetaData


class GeoObject(BaseModel):
    metaDataProperty: metaDataProperty
    name: str
    boundedBy: dict
    uri: str
    Point: dict


class Results(BaseModel):
    GeoObject: GeoObject
