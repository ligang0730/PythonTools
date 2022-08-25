# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TargetAlert.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Cooperative_pb2 as Cooperative__pb2
import VxCommonDef_pb2 as VxCommonDef__pb2
import DefPosition_pb2 as DefPosition__pb2
import Participant_pb2 as Participant__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11TargetAlert.proto\x12\x04vxII\x1a\x11\x43ooperative.proto\x1a\x11VxCommonDef.proto\x1a\x11\x44\x65\x66Position.proto\x1a\x11Participant.proto\"\xa1\x01\n\tGreenWave\x12\x12\n\nlight_type\x18\x01 \x01(\r\x12\x10\n\x08phase_id\x18\x02 \x01(\x05\x12\'\n\x0cphase_status\x18\x03 \x01(\x0e\x32\x11.vxII.PhaseStatus\x12\x14\n\x0csurplus_time\x18\x04 \x01(\x05\x12\x14\n\x0c\x61\x64vice_speed\x18\x05 \x01(\x05\x12\x19\n\x11running_red_light\x18\x06 \x01(\x08\"\xc4\x01\n\x08Location\x12!\n\x02id\x18\x01 \x01(\x0b\x32\x15.vxII.NodeReferenceID\x12\x0f\n\x07lane_id\x18\x02 \x01(\x05\x12\x14\n\nover_speed\x18\x03 \x01(\x08H\x00\x12\x15\n\x0blower_speed\x18\x04 \x01(\x08H\x00\x12\x1d\n\x04wave\x18\x05 \x03(\x0b\x32\x0f.vxII.GreenWave\x12/\n\x0bsped_limits\x18\x06 \x03(\x0b\x32\x1a.vxII.RegulatorySpeedLimitB\x07\n\x05speed\"{\n\x03RTS\x12\x1a\n\x04sign\x18\x01 \x01(\x0e\x32\x0c.vxII.RTSign\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0c\n\x04\x64ist\x18\x03 \x01(\r\x12\x14\n\x0c\x61lert_radius\x18\x04 \x01(\r\x12\x1f\n\x05pos3D\x18\x05 \x01(\x0b\x32\x10.vxII.Position3D\"}\n\x03RTE\x12\x1c\n\x05\x65vent\x18\x01 \x01(\x0e\x32\r.vxII.RTEvent\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0c\n\x04\x64ist\x18\x03 \x01(\r\x12\x14\n\x0c\x61lert_radius\x18\x04 \x01(\r\x12\x1f\n\x05pos3D\x18\x05 \x01(\x0b\x32\x10.vxII.Position3D\"\\\n\x08VIThreat\x12\x16\n\x03rte\x18\x01 \x03(\x0b\x32\t.vxII.RTE\x12\x16\n\x03rts\x18\x02 \x03(\x0b\x32\t.vxII.RTS\x12 \n\x08location\x18\x03 \x03(\x0b\x32\x0e.vxII.Location\"\x80\x01\n\x0e\x44istanceTimeHT\x12\x14\n\x0c\x64ist_horizon\x18\x01 \x01(\x05\x12\x15\n\rdist_vertical\x18\x02 \x01(\x05\x12\x16\n\x0e\x64ist_collision\x18\x03 \x01(\x05\x12\x16\n\x0etime_collision\x18\x04 \x01(\x05\x12\x11\n\tdist_safe\x18\x05 \x01(\x05\"\xad\x01\n\rDistanceTimeI\x12\x13\n\x0binter_late7\x18\x01 \x01(\x05\x12\x13\n\x0binter_lone7\x18\x02 \x01(\x05\x12\x10\n\x08h2i_dist\x18\x03 \x01(\x05\x12\x10\n\x08r2i_dist\x18\x04 \x01(\x05\x12\x10\n\x08h2i_time\x18\x05 \x01(\x05\x12\x10\n\x08r2i_time\x18\x06 \x01(\x05\x12\x14\n\x0ch2i_col_dist\x18\x07 \x01(\x05\x12\x14\n\x0cr2i_col_dist\x18\x08 \x01(\x05\"`\n\x0cVVThreatItem\x12\'\n\x0cthreat_class\x18\x01 \x01(\x0e\x32\x11.vxII.ThreatClass\x12\'\n\x0cthreat_level\x18\x02 \x01(\x0e\x32\x11.vxII.ThreatLevel\"\xdf\x02\n\x08VVThreat\x12\x1d\n\x02rv\x18\x01 \x01(\x0b\x32\x11.vxII.Participant\x12\x0c\n\x04\x64ist\x18\x02 \x01(\x05\x12\x15\n\rdelta_heading\x18\x03 \x01(\x05\x12\"\n\x02ht\x18\x04 \x01(\x0b\x32\x14.vxII.DistanceTimeHTH\x00\x12$\n\x05inter\x18\x05 \x01(\x0b\x32\x13.vxII.DistanceTimeIH\x00\x12\'\n\tdir_class\x18\x06 \x01(\x0e\x32\x14.vxII.DirectionClass\x12\'\n\tele_class\x18\x07 \x01(\x0e\x32\x14.vxII.ElevationClass\x12#\n\nlane_class\x18\x08 \x01(\x0e\x32\x0f.vxII.LaneClass\x12&\n\tdis_class\x18\t \x01(\x0e\x32\x13.vxII.DistanceClass\x12 \n\x04item\x18\n \x01(\x0b\x32\x12.vxII.VVThreatItemB\x04\n\x02\x64t\"-\n\tVVThreats\x12 \n\x08vvThreat\x18\x01 \x03(\x0b\x32\x0e.vxII.VVThreat\"\xca\x02\n\x0bTargetAlert\x12\x0e\n\x06msgCnt\x18\x01 \x01(\r\x12\x0f\n\x07secMark\x18\x02 \x01(\r\x12\"\n\x08viThreat\x18\x03 \x01(\x0b\x32\x0e.vxII.VIThreatH\x00\x12$\n\tvvThreats\x18\x04 \x01(\x0b\x32\x0f.vxII.VVThreatsH\x00\x12\x30\n\tlaneLange\x18\x05 \x01(\x0b\x32\x1b.vxII.CooperativeLaneChangeH\x00\x12-\n\x08vehMerge\x18\x06 \x01(\x0b\x32\x19.vxII.CooperativeVehMergeH\x00\x12\x34\n\x04\x63hpp\x18\x07 \x01(\x0b\x32$.vxII.CooperativeHighPriorityPassingH\x00\x12\x30\n\x03ssm\x18\x08 \x01(\x0b\x32!.vxII.CooperativeSharingSensorMsgH\x00\x42\x07\n\x05\x61lert*z\n\x0bPhaseStatus\x12\x0e\n\nPS_UNKNOWN\x10\x00\x12\x0b\n\x07PS_DARK\x10\x01\x12\x10\n\x0cPS_RED_FLASH\x10\x02\x12\n\n\x06PS_RED\x10\x03\x12\x0c\n\x08PS_GREEN\x10\x06\x12\r\n\tPS_YELLOW\x10\x07\x12\x13\n\x0fPS_YELLOW_FLASH\x10\x08*\xbc\x15\n\x06RTSign\x12\x0e\n\nSIGN_START\x10\x00\x12\x15\n\x11SIGN_INTERSECTION\x10\x01\x12\x13\n\x0fSIGN_SHARP_BEND\x10\x02\x12\x16\n\x12SIGN_REVERSE_CURVE\x10\x03\x12\x15\n\x11SIGN_CURVES_AHEAD\x10\x04\x12\x1c\n\x18SIGN_STEEP_DESCENT_AHEAD\x10\x05\x12\x15\n\x11SIGN_LONG_DESCENT\x10\x06\x12\x14\n\x10SIGN_NARROW_ROAD\x10\x07\x12\x16\n\x12SIGN_NARROW_BRIDGE\x10\x08\x12\x18\n\x14SIGN_TWO_WAY_TRAFFIC\x10\t\x12\x1a\n\x16SIGN_WATCH_PEDESTRAINS\x10\n\x12\x17\n\x13SIGN_WATCH_CHILDREN\x10\x0b\x12\x18\n\x14SIGN_WATCH_LIVESTOCK\x10\x0c\x12\x17\n\x13SIGN_WATCH_WILDLIFE\x10\r\x12\x1a\n\x16SIGN_WATCH_SIGNAL_LAMP\x10\x0e\x12\x17\n\x13SIGN_WATCH_ROCKFALL\x10\x0f\x12\x18\n\x14SIGN_WATCH_CROSSWIND\x10\x10\x12\x16\n\x12SIGN_SLIPPERY_ROAD\x10\x11\x12\x1c\n\x18SIGN_STEEP_MOUNTAIN_ROAD\x10\x12\x12\x18\n\x14SIGN_EMBANDMENT_ROAD\x10\x13\x12\x15\n\x11SIGN_VILLAGE_ROAD\x10\x14\x12\x0f\n\x0bSIGN_TUNNEL\x10\x15\x12\x0e\n\nSIGN_FERRY\x10\x16\x12\x19\n\x15SIGN_CAMELBACK_BRIDGE\x10\x17\x12\x13\n\x0fSIGN_ROUGH_ROAD\x10\x18\x12\x13\n\x0fSIGN_BUMPY_ROAD\x10\x19\x12\x17\n\x13SIGN_LOW_LYING_ROAD\x10\x1a\x12\x1b\n\x17SIGN_LOW_WATER_CROSSING\x10\x1b\x12\x19\n\x15SIGN_RAILWAY_CROSSING\x10\x1c\x12$\n SIGN_RAILWAY_NO_PERSION_CROSSING\x10\x1d\x12\x12\n\x0eSIGN_FURCATION\x10\x1e\x12\x0e\n\nSIGN_SLASH\x10\x1f\x12\x1c\n\x18SIGN_WATCH_NON_MOTOR_VEH\x10 \x12\x17\n\x13SIGN_WATCH_DISABLED\x10!\x12\x1c\n\x18SIGN_ACCIDENT_BLACK_SPOT\x10\"\x12\x12\n\x0eSIGN_SLOW_DOWN\x10#\x12\x16\n\x12SIGN_WATCH_BARRIER\x10$\x12\x15\n\x11SIGN_WATCH_DANGER\x10%\x12\x11\n\rSIGN_ROADWORK\x10&\x12\x15\n\x11SIGN_ADVICE_SPEED\x10\'\x12\x15\n\x11SIGN_TUNNEL_LIGHT\x10(\x12\x1e\n\x1aSIGN_WATCH_REVERSIBLE_LANE\x10)\x12\x16\n\x12SIGN_KEEP_DISTANCE\x10*\x12\x12\n\x0eSIGN_FORK_ROAD\x10+\x12\x13\n\x0fSIGN_MERGE_ROAD\x10,\x12\x14\n\x10SIGN_ESCAPE_RAMP\x10-\x12\x17\n\x13SIGN_WATCH_ICY_ROAD\x10.\x12\x1e\n\x1aSIGN_WATCH_RAINY_AND_SNOWY\x10.\x12\x14\n\x10SIGN_WATCH_FOGGY\x10.\x12\x1a\n\x16SIGN_WATCH_BAD_WEATHER\x10.\x12\x1c\n\x18SIGN_WATCH_QUEEN_VEHICLE\x10/\x12\x18\n\x14\x42\x41N_STOP_TO_GIVE_WAY\x10\x30\x12\x18\n\x14\x42\x41N_SLOW_TO_GIVE_WAY\x10\x31\x12 \n\x1c\x42\x41N_GIVE_WAY_TO_ONCOMING_VEH\x10\x32\x12\x10\n\x0c\x42\x41N_NO_ENTRY\x10\x33\x12\x10\n\x0c\x42\x41N_NO_DRIVE\x10\x34\x12\x11\n\rBAN_VEH_ENTRY\x10\x35\x12\x13\n\x0f\x42\x41N_TRUCE_ENTRY\x10\x36\x12\x1e\n\x1a\x42\x41N_ELECTRO_TRICYCLE_ENTRY\x10\x37\x12\x17\n\x13\x42\x41N_LARGE_BUS_ENTRY\x10\x38\x12\x19\n\x15\x42\x41N_SEMITRAILER_ENTRY\x10:\x12\x16\n\x12\x42\x41N_TRACTORS_ENTRY\x10;\x12\x16\n\x12\x42\x41N_TRICYCLE_ENTRY\x10<\x12\x17\n\x13\x42\x41N_MOTORBIKE_ENTRY\x10=\x12\x19\n\x15\x42\x41N_TWO_WHEELER_ENTRY\x10>\x12\x1b\n\x17\x42\x41N_NON_MOTOR_VEH_ENTRY\x10?\x12\x1e\n\x1a\x42\x41N_ANIMAL_DRAWN_VEH_ENTRY\x10@\x12%\n!BAN_MANPOWER_TRICYCLE_GUEST_ENTRY\x10\x41\x12%\n!BAN_MANPOWER_TRICYCLE_CARGO_ENTRY\x10\x42\x12\x12\n\x0e\x42\x41N_BIKE_ENTRY\x10\x43\x12\x18\n\x14\x42\x41N_PEDESTRIAN_ENTRY\x10\x44\x12\x11\n\rBAN_LEFT_TURN\x10\x45\x12\x12\n\x0e\x42\x41N_RIGHT_TURN\x10\x46\x12\x13\n\x0f\x42\x41N_GO_STRAIGHT\x10G\x12\x17\n\x13\x42\x41N_LEFT_RIGHT_TURN\x10H\x12\x1d\n\x19\x42\x41N_GO_STRAIGHT_LEFT_TURN\x10I\x12\x1e\n\x1a\x42\x41N_GO_STRAIGHT_RIGHT_TURN\x10J\x12\x12\n\x0e\x42\x41N_TURN_ROUND\x10K\x12\x10\n\x0c\x42\x41N_OVERTAKE\x10L\x12\x13\n\x0f\x42\x41N_CANCEL_STOP\x10M\x12\x0c\n\x08\x42\x41N_STOP\x10N\x12\x16\n\x12\x42\x41N_LONG_TIME_STOP\x10O\x12\x0c\n\x08\x42\x41N_HONK\x10P\x12\x11\n\rBAN_MAX_WIDTH\x10Q\x12\x12\n\x0e\x42\x41N_MAX_HEIGHT\x10R\x12\x12\n\x0e\x42\x41N_NAX_WEIGHT\x10S\x12\x11\n\rBAN_AXLE_LOAD\x10T\x12\r\n\tBAN_SPEED\x10U\x12\x14\n\x10\x42\x41N_CANCEL_SPEED\x10V\x12\x10\n\x0cSTOP_EXAMINE\x10W\x12\x1b\n\x17\x42\x41N_DANGEROUS_VEH_ENTRY\x10X\x12\x0f\n\x0b\x42\x41N_CUSTOMS\x10Y\x12\x18\n\x14\x42\x41N_SPEED_LIMIT_AREA\x10Z\x12\x1f\n\x1b\x42\x41N_CANCEL_SPEED_LIMIT_AREA\x10[\x12\x16\n\x12\x42\x41N_LONG_STOP_AREA\x10\\\x12\x1d\n\x19\x42\x41N_CANCEL_LONG_STOP_AREA\x10]\x12\x11\n\rBAN_STOP_AREA\x10^\x12\x18\n\x14\x42\x41N_CANCEL_STOP_AREA\x10_\x12\x1b\n\x17SIGN_ROUNDABOUT_DRIVING\x10j\x12\x1c\n\x18SIGN_PEDESTRIAN_CROSSING\x10r\x12\x19\n\x14SIGN_EXPRESSWAY_EXIT\x10\xb7\x01\x12\x1a\n\x15SIGN_ETC_TOLL_STATION\x10\xc6\x01\x12\x10\n\x0bSIGN_SCHOOL\x10\xf2\x01\x12\x1b\n\x16SIGN_DRIVING_TEST_LINE\x10\xf7\x01\x12\x17\n\x12SIGN_TUNNEL_OUTPUT\x10\xcd\x08\x12\x18\n\x13SIGN_EMERGENCY_EXIT\x10\xce\x08\x12\x18\n\x13SIGN_ELEVATE_HEIGHT\x10\xcf\x08\x12\x15\n\x10SIGN_RAMP_CLOSED\x10\xdcV\x12\x17\n\x11SIGN_WELCOME_WORD\x10\xe4\xd4\x03\x12!\n\x1bSIGN_OVERSIZE_VEHICLE_RIGHT\x10\xe9\xd4\x03\x12\x11\n\x0bSIGN_BRIDGE\x10\xea\xd4\x03\x12\x12\n\x0cSIGN_TRAMCAR\x10\xf5\xd4\x03\x1a\x02\x10\x01*\x9e\x07\n\x07RTEvent\x12\r\n\tRTE_START\x10\x00\x12\x0b\n\x07RTE_ICE\x10.\x12\x14\n\x10RTE_ROAD_DAMAGED\x10\x64\x12\x19\n\x15RTE_VEHICLE_BREAKDOWN\x10\x65\x12\x1b\n\x17RTE_VEH_TO_VEH_ACCIDENT\x10g\x12\x15\n\x10RTE_VEH_FIRE_OUT\x10\xc9\x01\x12\x16\n\x11RTE_FIRE_DETECTED\x10\xca\x01\x12\x15\n\x10RTE_WEATHER_RAIN\x10\xad\x02\x12\x15\n\x10RTE_WEATHER_HAIL\x10\xae\x02\x12\x15\n\x10RTE_WEATHER_WIND\x10\xb0\x02\x12\x14\n\x0fRTE_WEATHER_FOG\x10\xb1\x02\x12\x1a\n\x15RTE_WEATHER_HIGH_TEMP\x10\xb2\x02\x12\x15\n\x10RTE_WEATHER_SNOW\x10\xb4\x02\x12\x15\n\x10RTE_WEATHER_HAZE\x10\xb7\x02\x12\x1b\n\x16RTE_WEATHER_SAND_STORM\x10\x8f\x03\x12\x19\n\x14RTE_SPILLED_MATERIAL\x10\x91\x03\x12\x1c\n\x17RTE_PEDESTRIAN_DETECTED\x10\x95\x03\x12\x18\n\x13RTE_ANIMAL_DETECTED\x10\x96\x03\x12\x15\n\x10RTE_ROAD_PONDING\x10\x97\x03\x12\x16\n\x11RTE_ROAD_SLIPPERY\x10\x98\x03\x12\x11\n\x0cRTE_ROAD_ICE\x10\x99\x03\x12\x11\n\x0cRTE_ROADWORK\x10\xf5\x03\x12\x11\n\x0cRTE_ROAD_JAM\x10\xc3\x05\x12\x17\n\x12RTE_VEH_OVER_SPEED\x10\x85\x07\x12\x16\n\x11RTE_VEH_LOW_SPEED\x10\x86\x07\x12\x11\n\x0cRTE_VEH_STOP\x10\x87\x07\x12\x16\n\x11RTE_VEH_WRONG_DIR\x10\x88\x07\x12\x1d\n\x18RTE_URGEN_VEH_PRECEDENCE\x10\x89\x07\x12\x17\n\x12RTE_TRUCK_DETECTED\x10\x8a\x07\x12\x13\n\x0eRTE_RAMP_MERGE\x10\xec\x07\x12\"\n\x1dRTE_OCCUPATION_EMERGENCY_LANE\x10\xfd\x07\x12\x18\n\x13RTE_GET_OUT_OF_LIEN\x10\x82\x08\x12\x17\n\x12RTE_VEHICLE_QUUEUE\x10\x9b\x08\x12\x12\n\rRTE_DARK_SMOK\x10\x9c\x08\x12\x1d\n\x18RTE_CARBONIC_OXIDE_ALERT\x10\x9d\x08\x12\x12\n\rRTE_ROAD_WORK\x10\x9e\x08\x12\x17\n\x12RTE_VISIBILITY_LOW\x10\xac\x46\x12\x1d\n\x18RTE_ROAD_AGGLOMERATE_FOG\x10\xb8M*`\n\x0bRoadRunType\x12\x15\n\x11ROAD_RUN_STRAIGHT\x10\x00\x12\x11\n\rROAD_RUN_LEFT\x10\x01\x12\x12\n\x0eROAD_RUN_RIGHT\x10\x02\x12\x13\n\x0fROAD_RUN_U_TURN\x10\x03*n\n\x0e\x44irectionClass\x12\x0e\n\nDC_UNKNOWN\x10\x00\x12\x0b\n\x07\x44\x43_SAME\x10\x01\x12\x13\n\x0f\x44\x43_INTERSECTION\x10\x02\x12\x0f\n\x0b\x44\x43_OPPOSITE\x10\x03\x12\x0c\n\x08\x44\x43_MERGE\x10\x04\x12\x0b\n\x07\x44\x43_FORK\x10\x05*[\n\x0e\x45levationClass\x12\x0b\n\x07\x45\x43_SAME\x10\x00\x12\t\n\x05\x45\x43_UP\x10\x01\x12\x10\n\x0c\x45\x43_UP_COMING\x10\x02\x12\x12\n\x0e\x45\x43_DOWN_COMING\x10\x04\x12\x0b\n\x07\x45\x43_DOWN\x10\x05*E\n\rDistanceClass\x12\x0e\n\nDC_FARAWAY\x10\x00\x12\n\n\x06\x44\x43_FAR\x10\x01\x12\x0b\n\x07\x44\x43_NEAR\x10\x02\x12\x0b\n\x07\x44\x43_SIDE\x10\x03*\xd9\x01\n\x0bThreatClass\x12\x0e\n\nTC_UNKNOWN\x10\x00\x12\x0b\n\x07TC_EEBL\x10\x01\x12\n\n\x06TC_FCW\x10\x02\x12\n\n\x06TC_BSW\x10\x03\x12\n\n\x06TC_LCW\x10\x04\x12\n\n\x06TC_IMA\x10\x05\x12\n\n\x06TC_LTA\x10\x06\x12\n\n\x06TC_CLW\x10\x07\x12\n\n\x06TC_EVA\x10\x08\x12\x0b\n\x07TC_DNPW\x10\t\x12\n\n\x06TC_AVW\x10\n\x12\x0e\n\nTC_I2V_PED\x10\x0b\x12\x13\n\x0fTC_I2V_NO_MOTOR\x10\x0c\x12\x10\n\x0cTC_I2V_MOTOR\x10\r\x12\t\n\x05TC_MA\x10\x1e*\xe8\x02\n\tLaneClass\x12\x0f\n\x0bLC_DETECTED\x10\x00\x12\x0c\n\x08LC_AHEAD\x10\x01\x12\x11\n\rLC_AHEAD_LEFT\x10\x05\x12\x15\n\x11LC_AHEAD_FAR_LEFT\x10\r\x12\x17\n\x13LC_INTERSETION_LEFT\x10%\x12\x16\n\x12LC_BEHIND_FAR_LEFT\x10\x1d\x12\x12\n\x0eLC_BEHIND_LEFT\x10\x15\x12\x0c\n\x08LC_BHIND\x10\x11\x12\x13\n\x0fLC_BEHIND_RIGHT\x10\x13\x12\x17\n\x13LC_BEHIND_FAR_RIGHT\x10\x1b\x12\x19\n\x15LC_INTERSECTION_RIGHT\x10#\x12\x16\n\x12LC_AHEAD_FAR_RIGHT\x10\x0b\x12\x12\n\x0eLC_AHEAD_RIGHT\x10\x03\x12\x10\n\x0cLC_FORK_LEFT\x10\x45\x12\x11\n\rLC_FORK_RIGHT\x10\x43\x12\x11\n\rLC_MERGE_LEFT\x10\x65\x12\x12\n\x0eLC_MERGE_RIGHT\x10g*Z\n\x0bThreatLevel\x12\x0e\n\nTL_UNKNOWN\x10\x00\x12\x0c\n\x08TL_FATAL\x10\x03\x12\x0e\n\nTL_WARNING\x10\x06\x12\x0c\n\x08TL_CAUSE\x10\t\x12\x0f\n\x0bTL_DETECTED\x10\nb\x06proto3')

_PHASESTATUS = DESCRIPTOR.enum_types_by_name['PhaseStatus']
PhaseStatus = enum_type_wrapper.EnumTypeWrapper(_PHASESTATUS)
_RTSIGN = DESCRIPTOR.enum_types_by_name['RTSign']
RTSign = enum_type_wrapper.EnumTypeWrapper(_RTSIGN)
_RTEVENT = DESCRIPTOR.enum_types_by_name['RTEvent']
RTEvent = enum_type_wrapper.EnumTypeWrapper(_RTEVENT)
_ROADRUNTYPE = DESCRIPTOR.enum_types_by_name['RoadRunType']
RoadRunType = enum_type_wrapper.EnumTypeWrapper(_ROADRUNTYPE)
_DIRECTIONCLASS = DESCRIPTOR.enum_types_by_name['DirectionClass']
DirectionClass = enum_type_wrapper.EnumTypeWrapper(_DIRECTIONCLASS)
_ELEVATIONCLASS = DESCRIPTOR.enum_types_by_name['ElevationClass']
ElevationClass = enum_type_wrapper.EnumTypeWrapper(_ELEVATIONCLASS)
_DISTANCECLASS = DESCRIPTOR.enum_types_by_name['DistanceClass']
DistanceClass = enum_type_wrapper.EnumTypeWrapper(_DISTANCECLASS)
_THREATCLASS = DESCRIPTOR.enum_types_by_name['ThreatClass']
ThreatClass = enum_type_wrapper.EnumTypeWrapper(_THREATCLASS)
_LANECLASS = DESCRIPTOR.enum_types_by_name['LaneClass']
LaneClass = enum_type_wrapper.EnumTypeWrapper(_LANECLASS)
_THREATLEVEL = DESCRIPTOR.enum_types_by_name['ThreatLevel']
ThreatLevel = enum_type_wrapper.EnumTypeWrapper(_THREATLEVEL)
PS_UNKNOWN = 0
PS_DARK = 1
PS_RED_FLASH = 2
PS_RED = 3
PS_GREEN = 6
PS_YELLOW = 7
PS_YELLOW_FLASH = 8
SIGN_START = 0
SIGN_INTERSECTION = 1
SIGN_SHARP_BEND = 2
SIGN_REVERSE_CURVE = 3
SIGN_CURVES_AHEAD = 4
SIGN_STEEP_DESCENT_AHEAD = 5
SIGN_LONG_DESCENT = 6
SIGN_NARROW_ROAD = 7
SIGN_NARROW_BRIDGE = 8
SIGN_TWO_WAY_TRAFFIC = 9
SIGN_WATCH_PEDESTRAINS = 10
SIGN_WATCH_CHILDREN = 11
SIGN_WATCH_LIVESTOCK = 12
SIGN_WATCH_WILDLIFE = 13
SIGN_WATCH_SIGNAL_LAMP = 14
SIGN_WATCH_ROCKFALL = 15
SIGN_WATCH_CROSSWIND = 16
SIGN_SLIPPERY_ROAD = 17
SIGN_STEEP_MOUNTAIN_ROAD = 18
SIGN_EMBANDMENT_ROAD = 19
SIGN_VILLAGE_ROAD = 20
SIGN_TUNNEL = 21
SIGN_FERRY = 22
SIGN_CAMELBACK_BRIDGE = 23
SIGN_ROUGH_ROAD = 24
SIGN_BUMPY_ROAD = 25
SIGN_LOW_LYING_ROAD = 26
SIGN_LOW_WATER_CROSSING = 27
SIGN_RAILWAY_CROSSING = 28
SIGN_RAILWAY_NO_PERSION_CROSSING = 29
SIGN_FURCATION = 30
SIGN_SLASH = 31
SIGN_WATCH_NON_MOTOR_VEH = 32
SIGN_WATCH_DISABLED = 33
SIGN_ACCIDENT_BLACK_SPOT = 34
SIGN_SLOW_DOWN = 35
SIGN_WATCH_BARRIER = 36
SIGN_WATCH_DANGER = 37
SIGN_ROADWORK = 38
SIGN_ADVICE_SPEED = 39
SIGN_TUNNEL_LIGHT = 40
SIGN_WATCH_REVERSIBLE_LANE = 41
SIGN_KEEP_DISTANCE = 42
SIGN_FORK_ROAD = 43
SIGN_MERGE_ROAD = 44
SIGN_ESCAPE_RAMP = 45
SIGN_WATCH_ICY_ROAD = 46
SIGN_WATCH_RAINY_AND_SNOWY = 46
SIGN_WATCH_FOGGY = 46
SIGN_WATCH_BAD_WEATHER = 46
SIGN_WATCH_QUEEN_VEHICLE = 47
BAN_STOP_TO_GIVE_WAY = 48
BAN_SLOW_TO_GIVE_WAY = 49
BAN_GIVE_WAY_TO_ONCOMING_VEH = 50
BAN_NO_ENTRY = 51
BAN_NO_DRIVE = 52
BAN_VEH_ENTRY = 53
BAN_TRUCE_ENTRY = 54
BAN_ELECTRO_TRICYCLE_ENTRY = 55
BAN_LARGE_BUS_ENTRY = 56
BAN_SEMITRAILER_ENTRY = 58
BAN_TRACTORS_ENTRY = 59
BAN_TRICYCLE_ENTRY = 60
BAN_MOTORBIKE_ENTRY = 61
BAN_TWO_WHEELER_ENTRY = 62
BAN_NON_MOTOR_VEH_ENTRY = 63
BAN_ANIMAL_DRAWN_VEH_ENTRY = 64
BAN_MANPOWER_TRICYCLE_GUEST_ENTRY = 65
BAN_MANPOWER_TRICYCLE_CARGO_ENTRY = 66
BAN_BIKE_ENTRY = 67
BAN_PEDESTRIAN_ENTRY = 68
BAN_LEFT_TURN = 69
BAN_RIGHT_TURN = 70
BAN_GO_STRAIGHT = 71
BAN_LEFT_RIGHT_TURN = 72
BAN_GO_STRAIGHT_LEFT_TURN = 73
BAN_GO_STRAIGHT_RIGHT_TURN = 74
BAN_TURN_ROUND = 75
BAN_OVERTAKE = 76
BAN_CANCEL_STOP = 77
BAN_STOP = 78
BAN_LONG_TIME_STOP = 79
BAN_HONK = 80
BAN_MAX_WIDTH = 81
BAN_MAX_HEIGHT = 82
BAN_NAX_WEIGHT = 83
BAN_AXLE_LOAD = 84
BAN_SPEED = 85
BAN_CANCEL_SPEED = 86
STOP_EXAMINE = 87
BAN_DANGEROUS_VEH_ENTRY = 88
BAN_CUSTOMS = 89
BAN_SPEED_LIMIT_AREA = 90
BAN_CANCEL_SPEED_LIMIT_AREA = 91
BAN_LONG_STOP_AREA = 92
BAN_CANCEL_LONG_STOP_AREA = 93
BAN_STOP_AREA = 94
BAN_CANCEL_STOP_AREA = 95
SIGN_ROUNDABOUT_DRIVING = 106
SIGN_PEDESTRIAN_CROSSING = 114
SIGN_EXPRESSWAY_EXIT = 183
SIGN_ETC_TOLL_STATION = 198
SIGN_SCHOOL = 242
SIGN_DRIVING_TEST_LINE = 247
SIGN_TUNNEL_OUTPUT = 1101
SIGN_EMERGENCY_EXIT = 1102
SIGN_ELEVATE_HEIGHT = 1103
SIGN_RAMP_CLOSED = 11100
SIGN_WELCOME_WORD = 60004
SIGN_OVERSIZE_VEHICLE_RIGHT = 60009
SIGN_BRIDGE = 60010
SIGN_TRAMCAR = 60021
RTE_START = 0
RTE_ICE = 46
RTE_ROAD_DAMAGED = 100
RTE_VEHICLE_BREAKDOWN = 101
RTE_VEH_TO_VEH_ACCIDENT = 103
RTE_VEH_FIRE_OUT = 201
RTE_FIRE_DETECTED = 202
RTE_WEATHER_RAIN = 301
RTE_WEATHER_HAIL = 302
RTE_WEATHER_WIND = 304
RTE_WEATHER_FOG = 305
RTE_WEATHER_HIGH_TEMP = 306
RTE_WEATHER_SNOW = 308
RTE_WEATHER_HAZE = 311
RTE_WEATHER_SAND_STORM = 399
RTE_SPILLED_MATERIAL = 401
RTE_PEDESTRIAN_DETECTED = 405
RTE_ANIMAL_DETECTED = 406
RTE_ROAD_PONDING = 407
RTE_ROAD_SLIPPERY = 408
RTE_ROAD_ICE = 409
RTE_ROADWORK = 501
RTE_ROAD_JAM = 707
RTE_VEH_OVER_SPEED = 901
RTE_VEH_LOW_SPEED = 902
RTE_VEH_STOP = 903
RTE_VEH_WRONG_DIR = 904
RTE_URGEN_VEH_PRECEDENCE = 905
RTE_TRUCK_DETECTED = 906
RTE_RAMP_MERGE = 1004
RTE_OCCUPATION_EMERGENCY_LANE = 1021
RTE_GET_OUT_OF_LIEN = 1026
RTE_VEHICLE_QUUEUE = 1051
RTE_DARK_SMOK = 1052
RTE_CARBONIC_OXIDE_ALERT = 1053
RTE_ROAD_WORK = 1054
RTE_VISIBILITY_LOW = 9004
RTE_ROAD_AGGLOMERATE_FOG = 9912
ROAD_RUN_STRAIGHT = 0
ROAD_RUN_LEFT = 1
ROAD_RUN_RIGHT = 2
ROAD_RUN_U_TURN = 3
DC_UNKNOWN = 0
DC_SAME = 1
DC_INTERSECTION = 2
DC_OPPOSITE = 3
DC_MERGE = 4
DC_FORK = 5
EC_SAME = 0
EC_UP = 1
EC_UP_COMING = 2
EC_DOWN_COMING = 4
EC_DOWN = 5
DC_FARAWAY = 0
DC_FAR = 1
DC_NEAR = 2
DC_SIDE = 3
TC_UNKNOWN = 0
TC_EEBL = 1
TC_FCW = 2
TC_BSW = 3
TC_LCW = 4
TC_IMA = 5
TC_LTA = 6
TC_CLW = 7
TC_EVA = 8
TC_DNPW = 9
TC_AVW = 10
TC_I2V_PED = 11
TC_I2V_NO_MOTOR = 12
TC_I2V_MOTOR = 13
TC_MA = 30
LC_DETECTED = 0
LC_AHEAD = 1
LC_AHEAD_LEFT = 5
LC_AHEAD_FAR_LEFT = 13
LC_INTERSETION_LEFT = 37
LC_BEHIND_FAR_LEFT = 29
LC_BEHIND_LEFT = 21
LC_BHIND = 17
LC_BEHIND_RIGHT = 19
LC_BEHIND_FAR_RIGHT = 27
LC_INTERSECTION_RIGHT = 35
LC_AHEAD_FAR_RIGHT = 11
LC_AHEAD_RIGHT = 3
LC_FORK_LEFT = 69
LC_FORK_RIGHT = 67
LC_MERGE_LEFT = 101
LC_MERGE_RIGHT = 103
TL_UNKNOWN = 0
TL_FATAL = 3
TL_WARNING = 6
TL_CAUSE = 9
TL_DETECTED = 10


_GREENWAVE = DESCRIPTOR.message_types_by_name['GreenWave']
_LOCATION = DESCRIPTOR.message_types_by_name['Location']
_RTS = DESCRIPTOR.message_types_by_name['RTS']
_RTE = DESCRIPTOR.message_types_by_name['RTE']
_VITHREAT = DESCRIPTOR.message_types_by_name['VIThreat']
_DISTANCETIMEHT = DESCRIPTOR.message_types_by_name['DistanceTimeHT']
_DISTANCETIMEI = DESCRIPTOR.message_types_by_name['DistanceTimeI']
_VVTHREATITEM = DESCRIPTOR.message_types_by_name['VVThreatItem']
_VVTHREAT = DESCRIPTOR.message_types_by_name['VVThreat']
_VVTHREATS = DESCRIPTOR.message_types_by_name['VVThreats']
_TARGETALERT = DESCRIPTOR.message_types_by_name['TargetAlert']
GreenWave = _reflection.GeneratedProtocolMessageType('GreenWave', (_message.Message,), {
  'DESCRIPTOR' : _GREENWAVE,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.GreenWave)
  })
_sym_db.RegisterMessage(GreenWave)

Location = _reflection.GeneratedProtocolMessageType('Location', (_message.Message,), {
  'DESCRIPTOR' : _LOCATION,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.Location)
  })
_sym_db.RegisterMessage(Location)

RTS = _reflection.GeneratedProtocolMessageType('RTS', (_message.Message,), {
  'DESCRIPTOR' : _RTS,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.RTS)
  })
_sym_db.RegisterMessage(RTS)

RTE = _reflection.GeneratedProtocolMessageType('RTE', (_message.Message,), {
  'DESCRIPTOR' : _RTE,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.RTE)
  })
_sym_db.RegisterMessage(RTE)

VIThreat = _reflection.GeneratedProtocolMessageType('VIThreat', (_message.Message,), {
  'DESCRIPTOR' : _VITHREAT,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.VIThreat)
  })
_sym_db.RegisterMessage(VIThreat)

DistanceTimeHT = _reflection.GeneratedProtocolMessageType('DistanceTimeHT', (_message.Message,), {
  'DESCRIPTOR' : _DISTANCETIMEHT,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.DistanceTimeHT)
  })
_sym_db.RegisterMessage(DistanceTimeHT)

DistanceTimeI = _reflection.GeneratedProtocolMessageType('DistanceTimeI', (_message.Message,), {
  'DESCRIPTOR' : _DISTANCETIMEI,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.DistanceTimeI)
  })
_sym_db.RegisterMessage(DistanceTimeI)

VVThreatItem = _reflection.GeneratedProtocolMessageType('VVThreatItem', (_message.Message,), {
  'DESCRIPTOR' : _VVTHREATITEM,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.VVThreatItem)
  })
_sym_db.RegisterMessage(VVThreatItem)

VVThreat = _reflection.GeneratedProtocolMessageType('VVThreat', (_message.Message,), {
  'DESCRIPTOR' : _VVTHREAT,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.VVThreat)
  })
_sym_db.RegisterMessage(VVThreat)

VVThreats = _reflection.GeneratedProtocolMessageType('VVThreats', (_message.Message,), {
  'DESCRIPTOR' : _VVTHREATS,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.VVThreats)
  })
_sym_db.RegisterMessage(VVThreats)

TargetAlert = _reflection.GeneratedProtocolMessageType('TargetAlert', (_message.Message,), {
  'DESCRIPTOR' : _TARGETALERT,
  '__module__' : 'TargetAlert_pb2'
  # @@protoc_insertion_point(class_scope:vxII.TargetAlert)
  })
_sym_db.RegisterMessage(TargetAlert)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RTSIGN._options = None
  _RTSIGN._serialized_options = b'\020\001'
  _PHASESTATUS._serialized_start=1951
  _PHASESTATUS._serialized_end=2073
  _RTSIGN._serialized_start=2076
  _RTSIGN._serialized_end=4824
  _RTEVENT._serialized_start=4827
  _RTEVENT._serialized_end=5753
  _ROADRUNTYPE._serialized_start=5755
  _ROADRUNTYPE._serialized_end=5851
  _DIRECTIONCLASS._serialized_start=5853
  _DIRECTIONCLASS._serialized_end=5963
  _ELEVATIONCLASS._serialized_start=5965
  _ELEVATIONCLASS._serialized_end=6056
  _DISTANCECLASS._serialized_start=6058
  _DISTANCECLASS._serialized_end=6127
  _THREATCLASS._serialized_start=6130
  _THREATCLASS._serialized_end=6347
  _LANECLASS._serialized_start=6350
  _LANECLASS._serialized_end=6710
  _THREATLEVEL._serialized_start=6712
  _THREATLEVEL._serialized_end=6802
  _GREENWAVE._serialized_start=104
  _GREENWAVE._serialized_end=265
  _LOCATION._serialized_start=268
  _LOCATION._serialized_end=464
  _RTS._serialized_start=466
  _RTS._serialized_end=589
  _RTE._serialized_start=591
  _RTE._serialized_end=716
  _VITHREAT._serialized_start=718
  _VITHREAT._serialized_end=810
  _DISTANCETIMEHT._serialized_start=813
  _DISTANCETIMEHT._serialized_end=941
  _DISTANCETIMEI._serialized_start=944
  _DISTANCETIMEI._serialized_end=1117
  _VVTHREATITEM._serialized_start=1119
  _VVTHREATITEM._serialized_end=1215
  _VVTHREAT._serialized_start=1218
  _VVTHREAT._serialized_end=1569
  _VVTHREATS._serialized_start=1571
  _VVTHREATS._serialized_end=1616
  _TARGETALERT._serialized_start=1619
  _TARGETALERT._serialized_end=1949
# @@protoc_insertion_point(module_scope)