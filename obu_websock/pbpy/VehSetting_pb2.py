# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: VehSetting.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import VehSize_pb2 as VehSize__pb2
import VehClass_pb2 as VehClass__pb2
import VehBrake_pb2 as VehBrake__pb2
import VehStatus_pb2 as VehStatus__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10VehSetting.proto\x12\x04vxII\x1a\rVehSize.proto\x1a\x0eVehClass.proto\x1a\x0eVehBrake.proto\x1a\x0fVehStatus.proto\"\xa6\x01\n\nVehSetting\x12\x0e\n\x06msgCnt\x18\x01 \x01(\r\x12\x1b\n\x04size\x18\x02 \x01(\x0b\x32\r.vxII.VehSize\x12-\n\x08vehClass\x18\x03 \x01(\x0b\x32\x1b.vxII.VehicleClassification\x12,\n\x0b\x62rakeStatus\x18\x04 \x01(\x0b\x32\x17.vxII.BrakeSystemStatus\x12\x0e\n\x06lights\x18\x05 \x01(\rb\x06proto3')



_VEHSETTING = DESCRIPTOR.message_types_by_name['VehSetting']
VehSetting = _reflection.GeneratedProtocolMessageType('VehSetting', (_message.Message,), {
  'DESCRIPTOR' : _VEHSETTING,
  '__module__' : 'VehSetting_pb2'
  # @@protoc_insertion_point(class_scope:vxII.VehSetting)
  })
_sym_db.RegisterMessage(VehSetting)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _VEHSETTING._serialized_start=91
  _VEHSETTING._serialized_end=257
# @@protoc_insertion_point(module_scope)
