# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SensorSharing.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import RSI_pb2 as RSI__pb2
import RSM_pb2 as RSM__pb2
import VIR_pb2 as VIR__pb2
import DefMotion_pb2 as DefMotion__pb2
import Confidence_pb2 as Confidence__pb2
import DefPosition_pb2 as DefPosition__pb2
import VehSafetyExt_pb2 as VehSafetyExt__pb2
import DefAcceleration_pb2 as DefAcceleration__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13SensorSharing.proto\x12\x04vxII\x1a\tRSI.proto\x1a\tRSM.proto\x1a\tVIR.proto\x1a\x0f\x44\x65\x66Motion.proto\x1a\x10\x43onfidence.proto\x1a\x11\x44\x65\x66Position.proto\x1a\x12VehSafetyExt.proto\x1a\x15\x44\x65\x66\x41\x63\x63\x65leration.proto\x1a\x1egoogle/protobuf/wrappers.proto\"|\n\x08Planning\x12\x10\n\x08\x64uration\x18\x01 \x01(\r\x12\x16\n\x0eplanConfidence\x18\x02 \x01(\r\x12\x17\n\x0f\x64rivingBehavior\x18\x03 \x01(\r\x12-\n\x0cpathPlanning\x18\x04 \x03(\x0b\x32\x17.vxII.PathPlanningPoint\"4\n\x08\x41ttitude\x12\r\n\x05pitch\x18\x01 \x01(\x05\x12\x0c\n\x04roll\x18\x02 \x01(\x05\x12\x0b\n\x03yaw\x18\x03 \x01(\x05\"\xa5\x01\n\x12\x41ttitudeConfidence\x12\x30\n\x0fpitchConfidence\x18\x01 \x01(\x0e\x32\x17.vxII.HeadingConfidence\x12\x33\n\x12rollRateConfidence\x18\x02 \x01(\x0e\x32\x17.vxII.HeadingConfidence\x12(\n\x07yawRate\x18\x03 \x01(\x0e\x32\x17.vxII.HeadingConfidence\"G\n\x0f\x41ngularVelocity\x12\x11\n\tpitchRate\x18\x01 \x01(\x05\x12\x10\n\x08rollRate\x18\x02 \x01(\x05\x12\x0f\n\x07yawRate\x18\x03 \x01(\x05\"\x9f\x01\n\x19\x41ngularVelocityConfidence\x12+\n\tpitchRate\x18\x01 \x01(\x0e\x32\x18.vxII.AngularVConfidence\x12*\n\x08rollRate\x18\x02 \x01(\x0e\x32\x18.vxII.AngularVConfidence\x12)\n\x07yawRate\x18\x03 \x01(\x0e\x32\x18.vxII.AngularVConfidence\"\xea\x01\n\x12MotorDataExtension\x12\x0e\n\x06lights\x18\x01 \x01(\r\x12#\n\x0bvehAttitude\x18\x02 \x01(\x0b\x32\x0e.vxII.Attitude\x12\x37\n\x15vehAttitudeConfidence\x18\x03 \x01(\x0b\x32\x18.vxII.AttitudeConfidence\x12(\n\tvehAngVel\x18\x04 \x01(\x0b\x32\x15.vxII.AngularVelocity\x12<\n\x13vehAngVelConfidence\x18\x05 \x01(\x0b\x32\x1f.vxII.AngularVelocityConfidence\"/\n\x16Non_motorDataExtension\x12\x15\n\roverallRadius\x18\x01 \x01(\r\"\xf9\x03\n\x0f\x44\x65tectedPTCData\x12\"\n\x03ptc\x18\x01 \x01(\x0b\x32\x15.vxII.ParticipantData\x12\x35\n\x11objSizeConfidence\x18\x02 \x01(\x0b\x32\x1a.vxII.ObjectSizeConfidence\x12.\n\x0f\x64\x65tectedPTCType\x18\x03 \x01(\x0e\x32\x15.vxII.DetectedPTCType\x12\x16\n\x0etypeConfidence\x18\x04 \x01(\r\x12\x35\n\x11\x61\x63\x63\x34WayConfidence\x18\x05 \x01(\x0b\x32\x1a.vxII.AccSet4WayConfidence\x12\x16\n\x0estatusDuration\x18\x06 \x01(\r\x12&\n\x0bpathHistory\x18\x07 \x01(\x0b\x32\x11.vxII.PathHistory\x12 \n\x08planning\x18\x08 \x03(\x0b\x32\x0e.vxII.Planning\x12\x10\n\x08tracking\x18\t \x01(\r\x12!\n\x07polygon\x18\n \x03(\x0b\x32\x10.vxII.Position3D\x12,\n\x08motorExt\x18\x0b \x01(\x0b\x32\x18.vxII.MotorDataExtensionH\x00\x12\x34\n\x0cnon_motorExt\x18\x0c \x01(\x0b\x32\x1c.vxII.Non_motorDataExtensionH\x00\x42\x11\n\x0ftype_relatedExt\";\n\nObjectSize\x12\r\n\x05width\x18\x01 \x01(\r\x12\x0e\n\x06length\x18\x02 \x01(\r\x12\x0e\n\x06height\x18\x03 \x01(\r\"\xfd\x04\n\x14\x44\x65tectedObstacleData\x12#\n\x07obsType\x18\x01 \x01(\x0e\x32\x12.vxII.ObstacleType\x12\x37\n\x11objTypeConfidence\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\r\n\x05obsId\x18\x03 \x01(\r\x12 \n\x06source\x18\x04 \x01(\x0e\x32\x10.vxII.SourceType\x12\x0f\n\x07secMark\x18\x05 \x01(\r\x12\x1d\n\x03pos\x18\x06 \x01(\x0b\x32\x10.vxII.Position3D\x12\x32\n\rposConfidence\x18\x07 \x01(\x0b\x32\x1b.vxII.PositionConfidenceSet\x12\r\n\x05speed\x18\x08 \x01(\r\x12\'\n\x08speedCfd\x18\t \x01(\x0e\x32\x15.vxII.SpeedConfidence\x12\x0f\n\x07heading\x18\n \x01(\r\x12+\n\nheadingCfd\x18\x0b \x01(\x0e\x32\x17.vxII.HeadingConfidence\x12\x10\n\x08verSpeed\x18\x0c \x01(\r\x12\x31\n\x12verSpeedConfidence\x18\r \x01(\x0e\x32\x15.vxII.SpeedConfidence\x12+\n\x08\x61\x63\x63\x65lSet\x18\x0e \x01(\x0b\x32\x19.vxII.AccelerationSet4Way\x12\x1e\n\x04size\x18\x0f \x01(\x0b\x32\x10.vxII.ObjectSize\x12\x35\n\x11objSizeConfidence\x18\x10 \x01(\x0b\x32\x1a.vxII.ObjectSizeConfidence\x12\x10\n\x08tracking\x18\x11 \x01(\r\x12!\n\x07polygon\x18\x12 \x03(\x0b\x32\x10.vxII.Position3D\",\n\x07Polygon\x12!\n\x07polygon\x18\x01 \x03(\x0b\x32\x10.vxII.Position3D\"\xb0\x02\n\x10SensorSharingMsg\x12\x0e\n\x06msgCnt\x18\x01 \x01(\r\x12\n\n\x02id\x18\x02 \x01(\t\x12*\n\requipmentType\x18\x03 \x01(\x0e\x32\x13.vxII.EquipmentType\x12\x0f\n\x07secMark\x18\x04 \x01(\r\x12#\n\tsensorPos\x18\x05 \x01(\x0b\x32\x10.vxII.Position3D\x12%\n\x0e\x64\x65tectedRegion\x18\x06 \x03(\x0b\x32\r.vxII.Polygon\x12+\n\x0cparticipants\x18\x07 \x03(\x0b\x32\x15.vxII.DetectedPTCData\x12-\n\tobstacles\x18\x08 \x03(\x0b\x32\x1a.vxII.DetectedObstacleData\x12\x1b\n\x04rtes\x18\t \x03(\x0b\x32\r.vxII.RTEData*s\n\rEquipmentType\x12\x1a\n\x16unknown_equipment_type\x10\x00\x12\x16\n\x12rsu_equipment_type\x10\x01\x12\x16\n\x12obu_equipment_type\x10\x02\x12\x16\n\x12vru_equipment_type\x10\x03*\xf5\x02\n\x0f\x44\x65tectedPTCType\x12\x1d\n\x19unknown_detected_ptc_type\x10\x00\x12%\n!unknown_movable_detected_ptc_type\x10\x01\x12\'\n#unknown_unmovable_detected_ptc_type\x10\x02\x12\x19\n\x15\x63\x61r_detected_ptc_type\x10\x03\x12\x19\n\x15van_detected_ptc_type\x10\x04\x12\x1b\n\x17truck_detected_ptc_type\x10\x05\x12\x19\n\x15\x62us_detected_ptc_type\x10\x06\x12\x1d\n\x19\x63yclist_detected_ptc_type\x10\x07\x12\"\n\x1emotorcyclist_detected_ptc_type\x10\x08\x12 \n\x1ctricyclist_detected_ptc_type\x10\t\x12 \n\x1cpedestrian_detected_ptc_type\x10\n*\xd5\x03\n\x0cObstacleType\x12\x19\n\x15unknown_obstacle_type\x10\x00\x12\x1a\n\x16rockfall_obstacle_type\x10\x01\x12\x1b\n\x17landslide_obstacle_type\x10\x02\x12\"\n\x1e\x61nimal_intrusion_obstacle_type\x10\x03\x12\x1e\n\x1aliquid_spill_obstacle_type\x10\x04\x12!\n\x1dgoods_scattered_obstacle_type\x10\x05\x12\x1d\n\x19trafficcone_obstacle_type\x10\x06\x12!\n\x1dsafety_triangle_obstacle_type\x10\x07\x12#\n\x1ftraffic_roadblock_obstacle_type\x10\x08\x12\x30\n,inspection_shaft_without_cover_obstacle_type\x10\t\x12#\n\x1funknown_fragments_obstacle_type\x10\n\x12%\n!unknown_hard_object_obstacle_type\x10\x0b\x12%\n!unknown_soft_object_obstacle_type\x10\x0c\x62\x06proto3')

_EQUIPMENTTYPE = DESCRIPTOR.enum_types_by_name['EquipmentType']
EquipmentType = enum_type_wrapper.EnumTypeWrapper(_EQUIPMENTTYPE)
_DETECTEDPTCTYPE = DESCRIPTOR.enum_types_by_name['DetectedPTCType']
DetectedPTCType = enum_type_wrapper.EnumTypeWrapper(_DETECTEDPTCTYPE)
_OBSTACLETYPE = DESCRIPTOR.enum_types_by_name['ObstacleType']
ObstacleType = enum_type_wrapper.EnumTypeWrapper(_OBSTACLETYPE)
unknown_equipment_type = 0
rsu_equipment_type = 1
obu_equipment_type = 2
vru_equipment_type = 3
unknown_detected_ptc_type = 0
unknown_movable_detected_ptc_type = 1
unknown_unmovable_detected_ptc_type = 2
car_detected_ptc_type = 3
van_detected_ptc_type = 4
truck_detected_ptc_type = 5
bus_detected_ptc_type = 6
cyclist_detected_ptc_type = 7
motorcyclist_detected_ptc_type = 8
tricyclist_detected_ptc_type = 9
pedestrian_detected_ptc_type = 10
unknown_obstacle_type = 0
rockfall_obstacle_type = 1
landslide_obstacle_type = 2
animal_intrusion_obstacle_type = 3
liquid_spill_obstacle_type = 4
goods_scattered_obstacle_type = 5
trafficcone_obstacle_type = 6
safety_triangle_obstacle_type = 7
traffic_roadblock_obstacle_type = 8
inspection_shaft_without_cover_obstacle_type = 9
unknown_fragments_obstacle_type = 10
unknown_hard_object_obstacle_type = 11
unknown_soft_object_obstacle_type = 12


_PLANNING = DESCRIPTOR.message_types_by_name['Planning']
_ATTITUDE = DESCRIPTOR.message_types_by_name['Attitude']
_ATTITUDECONFIDENCE = DESCRIPTOR.message_types_by_name['AttitudeConfidence']
_ANGULARVELOCITY = DESCRIPTOR.message_types_by_name['AngularVelocity']
_ANGULARVELOCITYCONFIDENCE = DESCRIPTOR.message_types_by_name['AngularVelocityConfidence']
_MOTORDATAEXTENSION = DESCRIPTOR.message_types_by_name['MotorDataExtension']
_NON_MOTORDATAEXTENSION = DESCRIPTOR.message_types_by_name['Non_motorDataExtension']
_DETECTEDPTCDATA = DESCRIPTOR.message_types_by_name['DetectedPTCData']
_OBJECTSIZE = DESCRIPTOR.message_types_by_name['ObjectSize']
_DETECTEDOBSTACLEDATA = DESCRIPTOR.message_types_by_name['DetectedObstacleData']
_POLYGON = DESCRIPTOR.message_types_by_name['Polygon']
_SENSORSHARINGMSG = DESCRIPTOR.message_types_by_name['SensorSharingMsg']
Planning = _reflection.GeneratedProtocolMessageType('Planning', (_message.Message,), {
  'DESCRIPTOR' : _PLANNING,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.Planning)
  })
_sym_db.RegisterMessage(Planning)

Attitude = _reflection.GeneratedProtocolMessageType('Attitude', (_message.Message,), {
  'DESCRIPTOR' : _ATTITUDE,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.Attitude)
  })
_sym_db.RegisterMessage(Attitude)

AttitudeConfidence = _reflection.GeneratedProtocolMessageType('AttitudeConfidence', (_message.Message,), {
  'DESCRIPTOR' : _ATTITUDECONFIDENCE,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.AttitudeConfidence)
  })
_sym_db.RegisterMessage(AttitudeConfidence)

AngularVelocity = _reflection.GeneratedProtocolMessageType('AngularVelocity', (_message.Message,), {
  'DESCRIPTOR' : _ANGULARVELOCITY,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.AngularVelocity)
  })
_sym_db.RegisterMessage(AngularVelocity)

AngularVelocityConfidence = _reflection.GeneratedProtocolMessageType('AngularVelocityConfidence', (_message.Message,), {
  'DESCRIPTOR' : _ANGULARVELOCITYCONFIDENCE,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.AngularVelocityConfidence)
  })
_sym_db.RegisterMessage(AngularVelocityConfidence)

MotorDataExtension = _reflection.GeneratedProtocolMessageType('MotorDataExtension', (_message.Message,), {
  'DESCRIPTOR' : _MOTORDATAEXTENSION,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.MotorDataExtension)
  })
_sym_db.RegisterMessage(MotorDataExtension)

Non_motorDataExtension = _reflection.GeneratedProtocolMessageType('Non_motorDataExtension', (_message.Message,), {
  'DESCRIPTOR' : _NON_MOTORDATAEXTENSION,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.Non_motorDataExtension)
  })
_sym_db.RegisterMessage(Non_motorDataExtension)

DetectedPTCData = _reflection.GeneratedProtocolMessageType('DetectedPTCData', (_message.Message,), {
  'DESCRIPTOR' : _DETECTEDPTCDATA,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.DetectedPTCData)
  })
_sym_db.RegisterMessage(DetectedPTCData)

ObjectSize = _reflection.GeneratedProtocolMessageType('ObjectSize', (_message.Message,), {
  'DESCRIPTOR' : _OBJECTSIZE,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.ObjectSize)
  })
_sym_db.RegisterMessage(ObjectSize)

DetectedObstacleData = _reflection.GeneratedProtocolMessageType('DetectedObstacleData', (_message.Message,), {
  'DESCRIPTOR' : _DETECTEDOBSTACLEDATA,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.DetectedObstacleData)
  })
_sym_db.RegisterMessage(DetectedObstacleData)

Polygon = _reflection.GeneratedProtocolMessageType('Polygon', (_message.Message,), {
  'DESCRIPTOR' : _POLYGON,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.Polygon)
  })
_sym_db.RegisterMessage(Polygon)

SensorSharingMsg = _reflection.GeneratedProtocolMessageType('SensorSharingMsg', (_message.Message,), {
  'DESCRIPTOR' : _SENSORSHARINGMSG,
  '__module__' : 'SensorSharing_pb2'
  # @@protoc_insertion_point(class_scope:vxII.SensorSharingMsg)
  })
_sym_db.RegisterMessage(SensorSharingMsg)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EQUIPMENTTYPE._serialized_start=2622
  _EQUIPMENTTYPE._serialized_end=2737
  _DETECTEDPTCTYPE._serialized_start=2740
  _DETECTEDPTCTYPE._serialized_end=3113
  _OBSTACLETYPE._serialized_start=3116
  _OBSTACLETYPE._serialized_end=3585
  _PLANNING._serialized_start=191
  _PLANNING._serialized_end=315
  _ATTITUDE._serialized_start=317
  _ATTITUDE._serialized_end=369
  _ATTITUDECONFIDENCE._serialized_start=372
  _ATTITUDECONFIDENCE._serialized_end=537
  _ANGULARVELOCITY._serialized_start=539
  _ANGULARVELOCITY._serialized_end=610
  _ANGULARVELOCITYCONFIDENCE._serialized_start=613
  _ANGULARVELOCITYCONFIDENCE._serialized_end=772
  _MOTORDATAEXTENSION._serialized_start=775
  _MOTORDATAEXTENSION._serialized_end=1009
  _NON_MOTORDATAEXTENSION._serialized_start=1011
  _NON_MOTORDATAEXTENSION._serialized_end=1058
  _DETECTEDPTCDATA._serialized_start=1061
  _DETECTEDPTCDATA._serialized_end=1566
  _OBJECTSIZE._serialized_start=1568
  _OBJECTSIZE._serialized_end=1627
  _DETECTEDOBSTACLEDATA._serialized_start=1630
  _DETECTEDOBSTACLEDATA._serialized_end=2267
  _POLYGON._serialized_start=2269
  _POLYGON._serialized_end=2313
  _SENSORSHARINGMSG._serialized_start=2316
  _SENSORSHARINGMSG._serialized_end=2620
# @@protoc_insertion_point(module_scope)
