# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: InjectRsu.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import RSI_pb2 as RSI__pb2
import SignalPhaseAndTiming_pb2 as SignalPhaseAndTiming__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fInjectRsu.proto\x12\x04vxII\x1a\tRSI.proto\x1a\x1aSignalPhaseAndTiming.proto\"M\n\tInjectRsu\x12&\n\x03rsi\x18\x01 \x01(\x0b\x32\x19.vxII.RoadSideInformation\x12\x18\n\x04spat\x18\x02 \x01(\x0b\x32\n.vxII.SPATb\x06proto3')



_INJECTRSU = DESCRIPTOR.message_types_by_name['InjectRsu']
InjectRsu = _reflection.GeneratedProtocolMessageType('InjectRsu', (_message.Message,), {
  'DESCRIPTOR' : _INJECTRSU,
  '__module__' : 'InjectRsu_pb2'
  # @@protoc_insertion_point(class_scope:vxII.InjectRsu)
  })
_sym_db.RegisterMessage(InjectRsu)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INJECTRSU._serialized_start=64
  _INJECTRSU._serialized_end=141
# @@protoc_insertion_point(module_scope)