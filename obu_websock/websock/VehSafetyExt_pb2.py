# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: VehSafetyExt.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import DefTime_pb2 as DefTime__pb2
import VehStatus_pb2 as VehStatus__pb2
import DefMotion_pb2 as DefMotion__pb2
import DefPosition_pb2 as DefPosition__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12VehSafetyExt.proto\x12\x04vxII\x1a\rDefTime.proto\x1a\x0fVehStatus.proto\x1a\x0f\x44\x65\x66Motion.proto\x1a\x11\x44\x65\x66Position.proto\"\xb2\x02\n\x12\x46ullPositionVector\x12 \n\x07utcTime\x18\x01 \x01(\x0b\x32\x0f.vxII.DDateTime\x12\x1d\n\x03pos\x18\x02 \x01(\x0b\x32\x10.vxII.Position3D\x12\x0f\n\x07heading\x18\x03 \x01(\r\x12-\n\x0ctransmission\x18\x04 \x01(\x0e\x32\x17.vxII.TransmissionState\x12\r\n\x05speed\x18\x05 \x01(\r\x12\x30\n\x0bposAccuracy\x18\x06 \x01(\x0b\x32\x1b.vxII.PositionConfidenceSet\x12,\n\x0etimeConfidence\x18\x07 \x01(\x0e\x32\x14.vxII.TimeConfidence\x12,\n\tmotionCfd\x18\x08 \x01(\x0b\x32\x19.vxII.MotionConfidenceSet\"\x9a\x01\n\x10PathHistoryPoint\x12 \n\x06points\x18\x01 \x01(\x0b\x32\x10.vxII.Position3D\x12\x12\n\ntimeOffset\x18\x02 \x01(\r\x12\r\n\x05speed\x18\x03 \x01(\r\x12\x30\n\x0bposAccuracy\x18\x04 \x01(\x0b\x32\x1b.vxII.PositionConfidenceSet\x12\x0f\n\x07heading\x18\x05 \x01(\x05\"\x92\x01\n\x0bPathHistory\x12\x31\n\x0finitialPosition\x18\x01 \x01(\x0b\x32\x18.vxII.FullPositionVector\x12(\n\x0e\x63urrGNSSstatus\x18\x02 \x01(\x0e\x32\x10.vxII.GNSSstatus\x12&\n\x06points\x18\x03 \x03(\x0b\x32\x16.vxII.PathHistoryPoint\";\n\x0ePathPrediction\x12\x15\n\rradiusOfCurve\x18\x01 \x01(\x05\x12\x12\n\nconfidence\x18\x02 \x01(\r\"\xbe\x01\n\x17VehicleSafetyExtensions\x12\'\n\x06\x65vents\x18\x01 \x01(\x0e\x32\x17.vxII.VehicleEventFlags\x12&\n\x0bpathHistory\x18\x02 \x01(\x0b\x32\x11.vxII.PathHistory\x12,\n\x0epathPrediction\x18\x03 \x01(\x0b\x32\x14.vxII.PathPrediction\x12$\n\x06lights\x18\x04 \x01(\x0e\x32\x14.vxII.ExteriorLights*\x95\x02\n\nGNSSstatus\x12\x1b\n\x17unavailable_gnss_status\x10\x00\x12\x19\n\x15isHealthy_gnss_status\x10\x01\x12\x1b\n\x17isMonitored_gnss_status\x10\x02\x12\x1f\n\x1b\x62\x61seStationType_gnss_status\x10\x03\x12\x1d\n\x19\x61PDOPofUnder5_gnss_status\x10\x04\x12\x1e\n\x1ainViewOfUnder5_gnss_status\x10\x05\x12\'\n#localCorrectionsPresent_gnss_status\x10\x06\x12)\n%networkCorrectionsPresent_gnss_status\x10\x07\x62\x06proto3')

_GNSSSTATUS = DESCRIPTOR.enum_types_by_name['GNSSstatus']
GNSSstatus = enum_type_wrapper.EnumTypeWrapper(_GNSSSTATUS)
unavailable_gnss_status = 0
isHealthy_gnss_status = 1
isMonitored_gnss_status = 2
baseStationType_gnss_status = 3
aPDOPofUnder5_gnss_status = 4
inViewOfUnder5_gnss_status = 5
localCorrectionsPresent_gnss_status = 6
networkCorrectionsPresent_gnss_status = 7


_FULLPOSITIONVECTOR = DESCRIPTOR.message_types_by_name['FullPositionVector']
_PATHHISTORYPOINT = DESCRIPTOR.message_types_by_name['PathHistoryPoint']
_PATHHISTORY = DESCRIPTOR.message_types_by_name['PathHistory']
_PATHPREDICTION = DESCRIPTOR.message_types_by_name['PathPrediction']
_VEHICLESAFETYEXTENSIONS = DESCRIPTOR.message_types_by_name['VehicleSafetyExtensions']
FullPositionVector = _reflection.GeneratedProtocolMessageType('FullPositionVector', (_message.Message,), {
  'DESCRIPTOR' : _FULLPOSITIONVECTOR,
  '__module__' : 'VehSafetyExt_pb2'
  # @@protoc_insertion_point(class_scope:vxII.FullPositionVector)
  })
_sym_db.RegisterMessage(FullPositionVector)

PathHistoryPoint = _reflection.GeneratedProtocolMessageType('PathHistoryPoint', (_message.Message,), {
  'DESCRIPTOR' : _PATHHISTORYPOINT,
  '__module__' : 'VehSafetyExt_pb2'
  # @@protoc_insertion_point(class_scope:vxII.PathHistoryPoint)
  })
_sym_db.RegisterMessage(PathHistoryPoint)

PathHistory = _reflection.GeneratedProtocolMessageType('PathHistory', (_message.Message,), {
  'DESCRIPTOR' : _PATHHISTORY,
  '__module__' : 'VehSafetyExt_pb2'
  # @@protoc_insertion_point(class_scope:vxII.PathHistory)
  })
_sym_db.RegisterMessage(PathHistory)

PathPrediction = _reflection.GeneratedProtocolMessageType('PathPrediction', (_message.Message,), {
  'DESCRIPTOR' : _PATHPREDICTION,
  '__module__' : 'VehSafetyExt_pb2'
  # @@protoc_insertion_point(class_scope:vxII.PathPrediction)
  })
_sym_db.RegisterMessage(PathPrediction)

VehicleSafetyExtensions = _reflection.GeneratedProtocolMessageType('VehicleSafetyExtensions', (_message.Message,), {
  'DESCRIPTOR' : _VEHICLESAFETYEXTENSIONS,
  '__module__' : 'VehSafetyExt_pb2'
  # @@protoc_insertion_point(class_scope:vxII.VehicleSafetyExtensions)
  })
_sym_db.RegisterMessage(VehicleSafetyExtensions)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GNSSSTATUS._serialized_start=966
  _GNSSSTATUS._serialized_end=1243
  _FULLPOSITIONVECTOR._serialized_start=97
  _FULLPOSITIONVECTOR._serialized_end=403
  _PATHHISTORYPOINT._serialized_start=406
  _PATHHISTORYPOINT._serialized_end=560
  _PATHHISTORY._serialized_start=563
  _PATHHISTORY._serialized_end=709
  _PATHPREDICTION._serialized_start=711
  _PATHPREDICTION._serialized_end=770
  _VEHICLESAFETYEXTENSIONS._serialized_start=773
  _VEHICLESAFETYEXTENSIONS._serialized_end=963
# @@protoc_insertion_point(module_scope)