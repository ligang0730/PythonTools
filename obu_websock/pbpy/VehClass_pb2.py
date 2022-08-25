# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: VehClass.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eVehClass.proto\x12\x04vxII\"j\n\x15VehicleClassification\x12/\n\x0e\x63lassification\x18\x01 \x01(\x0e\x32\x17.vxII.BasicVehicleClass\x12 \n\x08\x66uelType\x18\x02 \x01(\x0e\x32\x0e.vxII.FuelType*\xef\x0c\n\x11\x42\x61sicVehicleClass\x12\x17\n\x13unknownVehicleClass\x10\x00\x12\x17\n\x13specialVehicleClass\x10\x01\x12!\n\x1dpassenger_Vehicle_TypeUnknown\x10\n\x12\x1f\n\x1bpassenger_Vehicle_TypeOther\x10\x0b\x12\"\n\x1elightTruck_Vehicle_TypeUnknown\x10\x14\x12 \n\x1clightTruck_Vehicle_TypeOther\x10\x15\x12\x1d\n\x19truck_Vehicle_TypeUnknown\x10\x19\x12\x1b\n\x17truck_Vehicle_TypeOther\x10\x1a\x12\x12\n\x0etruck_axleCnt2\x10\x1b\x12\x12\n\x0etruck_axleCnt3\x10\x1c\x12\x12\n\x0etruck_axleCnt4\x10\x1d\x12\x19\n\x15truck_axleCnt4Trailer\x10\x1e\x12\x19\n\x15truck_axleCnt5Trailer\x10\x1f\x12\x19\n\x15truck_axleCnt6Trailer\x10 \x12\x1e\n\x1atruck_axleCnt5MultiTrailer\x10!\x12\x1e\n\x1atruck_axleCnt6MultiTrailer\x10\"\x12\x1e\n\x1atruck_axleCnt7MultiTrailer\x10#\x12\x1a\n\x16motorcycle_TypeUnknown\x10(\x12\x18\n\x14motorcycle_TypeOther\x10)\x12\x1f\n\x1bmotorcycle_Cruiser_Standard\x10*\x12\x1a\n\x16motorcycle_SportUnclad\x10+\x12\x1b\n\x17motorcycle_SportTouring\x10,\x12\x19\n\x15motorcycle_SuperSport\x10-\x12\x16\n\x12motorcycle_Touring\x10.\x12\x14\n\x10motorcycle_Trike\x10/\x12\x1a\n\x16motorcycle_wPassengers\x10\x30\x12\x17\n\x13transit_TypeUnknown\x10\x32\x12\x15\n\x11transit_TypeOther\x10\x33\x12\x0f\n\x0btransit_BRT\x10\x34\x12\x16\n\x12transit_ExpressBus\x10\x35\x12\x14\n\x10transit_LocalBus\x10\x36\x12\x15\n\x11transit_SchoolBus\x10\x37\x12\x19\n\x15transit_FixedGuideway\x10\x38\x12\x17\n\x13transit_Paratransit\x10\x39\x12!\n\x1dtransit_Paratransit_Ambulance\x10:\x12\x19\n\x15\x65mergency_TypeUnknown\x10<\x12\x17\n\x13\x65mergency_TypeOther\x10=\x12 \n\x1c\x65mergency_Fire_Light_Vehicle\x10>\x12 \n\x1c\x65mergency_Fire_Heavy_Vehicle\x10?\x12$\n emergency_Fire_Paramedic_Vehicle\x10@\x12$\n emergency_Fire_Ambulance_Vehicle\x10\x41\x12\"\n\x1e\x65mergency_Police_Light_Vehicle\x10\x42\x12\"\n\x1e\x65mergency_Police_Heavy_Vehicle\x10\x43\x12\x1d\n\x19\x65mergency_Other_Responder\x10\x44\x12\x1d\n\x19\x65mergency_Other_Ambulance\x10\x45\x12\x1d\n\x19otherTraveler_TypeUnknown\x10P\x12\x1b\n\x17otherTraveler_TypeOther\x10Q\x12\x1c\n\x18otherTraveler_Pedestrian\x10R\x12#\n\x1fotherTraveler_Visually_Disabled\x10S\x12%\n!otherTraveler_Physically_Disabled\x10T\x12\x19\n\x15otherTraveler_Bicycle\x10U\x12\'\n#otherTraveler_Vulnerable_Roadworker\x10V\x12\x1e\n\x1ainfrastructure_TypeUnknown\x10Z\x12\x18\n\x14infrastructure_Fixed\x10[\x12\x1a\n\x16infrastructure_Movable\x10\\\x12\x19\n\x15\x65quipped_CargoTrailer\x10]*\x99\x01\n\x08\x46uelType\x12\x0f\n\x0bunknownFuel\x10\x00\x12\x0c\n\x08gasoline\x10\x01\x12\x0b\n\x07\x65thanol\x10\x02\x12\n\n\x06\x64iesel\x10\x03\x12\x0c\n\x08\x65lectric\x10\x04\x12\n\n\x06hybrid\x10\x05\x12\x0c\n\x08hydrogen\x10\x06\x12\x10\n\x0cnatGasLiquid\x10\x07\x12\x0e\n\nnatGasComp\x10\x08\x12\x0b\n\x07propane\x10\tb\x06proto3')

_BASICVEHICLECLASS = DESCRIPTOR.enum_types_by_name['BasicVehicleClass']
BasicVehicleClass = enum_type_wrapper.EnumTypeWrapper(_BASICVEHICLECLASS)
_FUELTYPE = DESCRIPTOR.enum_types_by_name['FuelType']
FuelType = enum_type_wrapper.EnumTypeWrapper(_FUELTYPE)
unknownVehicleClass = 0
specialVehicleClass = 1
passenger_Vehicle_TypeUnknown = 10
passenger_Vehicle_TypeOther = 11
lightTruck_Vehicle_TypeUnknown = 20
lightTruck_Vehicle_TypeOther = 21
truck_Vehicle_TypeUnknown = 25
truck_Vehicle_TypeOther = 26
truck_axleCnt2 = 27
truck_axleCnt3 = 28
truck_axleCnt4 = 29
truck_axleCnt4Trailer = 30
truck_axleCnt5Trailer = 31
truck_axleCnt6Trailer = 32
truck_axleCnt5MultiTrailer = 33
truck_axleCnt6MultiTrailer = 34
truck_axleCnt7MultiTrailer = 35
motorcycle_TypeUnknown = 40
motorcycle_TypeOther = 41
motorcycle_Cruiser_Standard = 42
motorcycle_SportUnclad = 43
motorcycle_SportTouring = 44
motorcycle_SuperSport = 45
motorcycle_Touring = 46
motorcycle_Trike = 47
motorcycle_wPassengers = 48
transit_TypeUnknown = 50
transit_TypeOther = 51
transit_BRT = 52
transit_ExpressBus = 53
transit_LocalBus = 54
transit_SchoolBus = 55
transit_FixedGuideway = 56
transit_Paratransit = 57
transit_Paratransit_Ambulance = 58
emergency_TypeUnknown = 60
emergency_TypeOther = 61
emergency_Fire_Light_Vehicle = 62
emergency_Fire_Heavy_Vehicle = 63
emergency_Fire_Paramedic_Vehicle = 64
emergency_Fire_Ambulance_Vehicle = 65
emergency_Police_Light_Vehicle = 66
emergency_Police_Heavy_Vehicle = 67
emergency_Other_Responder = 68
emergency_Other_Ambulance = 69
otherTraveler_TypeUnknown = 80
otherTraveler_TypeOther = 81
otherTraveler_Pedestrian = 82
otherTraveler_Visually_Disabled = 83
otherTraveler_Physically_Disabled = 84
otherTraveler_Bicycle = 85
otherTraveler_Vulnerable_Roadworker = 86
infrastructure_TypeUnknown = 90
infrastructure_Fixed = 91
infrastructure_Movable = 92
equipped_CargoTrailer = 93
unknownFuel = 0
gasoline = 1
ethanol = 2
diesel = 3
electric = 4
hybrid = 5
hydrogen = 6
natGasLiquid = 7
natGasComp = 8
propane = 9


_VEHICLECLASSIFICATION = DESCRIPTOR.message_types_by_name['VehicleClassification']
VehicleClassification = _reflection.GeneratedProtocolMessageType('VehicleClassification', (_message.Message,), {
  'DESCRIPTOR' : _VEHICLECLASSIFICATION,
  '__module__' : 'VehClass_pb2'
  # @@protoc_insertion_point(class_scope:vxII.VehicleClassification)
  })
_sym_db.RegisterMessage(VehicleClassification)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BASICVEHICLECLASS._serialized_start=133
  _BASICVEHICLECLASS._serialized_end=1780
  _FUELTYPE._serialized_start=1783
  _FUELTYPE._serialized_end=1936
  _VEHICLECLASSIFICATION._serialized_start=24
  _VEHICLECLASSIFICATION._serialized_end=130
# @@protoc_insertion_point(module_scope)
