# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SimulRvs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import HV_pb2 as HV__pb2
import Participant_pb2 as Participant__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eSimulRvs.proto\x12\x04vxII\x1a\x08HV.proto\x1a\x11Participant.proto\"E\n\x08SimulRvs\x12\x18\n\x02hv\x18\x01 \x01(\x0b\x32\x0c.vxII.HvInfo\x12\x1f\n\x03rvs\x18\x02 \x03(\x0b\x32\x12.vxII.Participantsb\x06proto3')



_SIMULRVS = DESCRIPTOR.message_types_by_name['SimulRvs']
SimulRvs = _reflection.GeneratedProtocolMessageType('SimulRvs', (_message.Message,), {
  'DESCRIPTOR' : _SIMULRVS,
  '__module__' : 'SimulRvs_pb2'
  # @@protoc_insertion_point(class_scope:vxII.SimulRvs)
  })
_sym_db.RegisterMessage(SimulRvs)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SIMULRVS._serialized_start=53
  _SIMULRVS._serialized_end=122
# @@protoc_insertion_point(module_scope)
