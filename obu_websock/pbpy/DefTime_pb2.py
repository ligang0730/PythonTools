# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: DefTime.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rDefTime.proto\x12\x04vxII\"s\n\tDDateTime\x12\x0c\n\x04year\x18\x01 \x01(\r\x12\r\n\x05month\x18\x02 \x01(\r\x12\x0b\n\x03\x64\x61y\x18\x03 \x01(\r\x12\x0c\n\x04hour\x18\x04 \x01(\r\x12\x0e\n\x06minute\x18\x05 \x01(\r\x12\x0e\n\x06second\x18\x06 \x01(\r\x12\x0e\n\x06offset\x18\x07 \x01(\r*\xf8\x06\n\x0eTimeConfidence\x12\x0f\n\x0bunavailable\x10\x00\x12\x10\n\x0ctime_100_000\x10\x01\x12\x10\n\x0ctime_050_000\x10\x02\x12\x10\n\x0ctime_020_000\x10\x03\x12\x10\n\x0ctime_010_000\x10\x04\x12\x10\n\x0ctime_002_000\x10\x05\x12\x10\n\x0ctime_001_000\x10\x06\x12\x10\n\x0ctime_000_500\x10\x07\x12\x10\n\x0ctime_000_200\x10\x08\x12\x10\n\x0ctime_000_100\x10\t\x12\x10\n\x0ctime_000_050\x10\n\x12\x10\n\x0ctime_000_020\x10\x0b\x12\x10\n\x0ctime_000_010\x10\x0c\x12\x10\n\x0ctime_000_005\x10\r\x12\x10\n\x0ctime_000_002\x10\x0e\x12\x10\n\x0ctime_000_001\x10\x0f\x12\x12\n\x0etime_000_000_5\x10\x10\x12\x12\n\x0etime_000_000_2\x10\x11\x12\x12\n\x0etime_000_000_1\x10\x12\x12\x13\n\x0ftime_000_000_05\x10\x13\x12\x13\n\x0ftime_000_000_02\x10\x14\x12\x13\n\x0ftime_000_000_01\x10\x15\x12\x14\n\x10time_000_000_005\x10\x16\x12\x14\n\x10time_000_000_002\x10\x17\x12\x14\n\x10time_000_000_001\x10\x18\x12\x16\n\x12time_000_000_000_5\x10\x19\x12\x16\n\x12time_000_000_000_2\x10\x1a\x12\x16\n\x12time_000_000_000_1\x10\x1b\x12\x17\n\x13time_000_000_000_05\x10\x1c\x12\x17\n\x13time_000_000_000_02\x10\x1d\x12\x17\n\x13time_000_000_000_01\x10\x1e\x12\x18\n\x14time_000_000_000_005\x10\x1f\x12\x18\n\x14time_000_000_000_002\x10 \x12\x18\n\x14time_000_000_000_001\x10!\x12\x1a\n\x16time_000_000_000_000_5\x10\"\x12\x1a\n\x16time_000_000_000_000_2\x10#\x12\x1a\n\x16time_000_000_000_000_1\x10$\x12\x1b\n\x17time_000_000_000_000_05\x10%\x12\x1b\n\x17time_000_000_000_000_02\x10&\x12\x1b\n\x17time_000_000_000_000_01\x10\'b\x06proto3')

_TIMECONFIDENCE = DESCRIPTOR.enum_types_by_name['TimeConfidence']
TimeConfidence = enum_type_wrapper.EnumTypeWrapper(_TIMECONFIDENCE)
unavailable = 0
time_100_000 = 1
time_050_000 = 2
time_020_000 = 3
time_010_000 = 4
time_002_000 = 5
time_001_000 = 6
time_000_500 = 7
time_000_200 = 8
time_000_100 = 9
time_000_050 = 10
time_000_020 = 11
time_000_010 = 12
time_000_005 = 13
time_000_002 = 14
time_000_001 = 15
time_000_000_5 = 16
time_000_000_2 = 17
time_000_000_1 = 18
time_000_000_05 = 19
time_000_000_02 = 20
time_000_000_01 = 21
time_000_000_005 = 22
time_000_000_002 = 23
time_000_000_001 = 24
time_000_000_000_5 = 25
time_000_000_000_2 = 26
time_000_000_000_1 = 27
time_000_000_000_05 = 28
time_000_000_000_02 = 29
time_000_000_000_01 = 30
time_000_000_000_005 = 31
time_000_000_000_002 = 32
time_000_000_000_001 = 33
time_000_000_000_000_5 = 34
time_000_000_000_000_2 = 35
time_000_000_000_000_1 = 36
time_000_000_000_000_05 = 37
time_000_000_000_000_02 = 38
time_000_000_000_000_01 = 39


_DDATETIME = DESCRIPTOR.message_types_by_name['DDateTime']
DDateTime = _reflection.GeneratedProtocolMessageType('DDateTime', (_message.Message,), {
  'DESCRIPTOR' : _DDATETIME,
  '__module__' : 'DefTime_pb2'
  # @@protoc_insertion_point(class_scope:vxII.DDateTime)
  })
_sym_db.RegisterMessage(DDateTime)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TIMECONFIDENCE._serialized_start=141
  _TIMECONFIDENCE._serialized_end=1029
  _DDATETIME._serialized_start=23
  _DDATETIME._serialized_end=138
# @@protoc_insertion_point(module_scope)
