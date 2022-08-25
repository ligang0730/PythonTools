# -*- coding: utf-8 -*-


import sys
import optparse
import random
import traci  # noqa
import sumolib
import threading
import json

from sumolib import checkBinary
from pynng import Pair0, Pair1
from multiprocessing import Process, Pipe


class QfSumo_Class(object):
    def __init__(self, parent=None):
        super(QfSumo_Class, self).__init__()
        global child_conn_vehState, parent_conn_vehState
        parent_conn_vehState, child_conn_vehState = Pipe()

    def get_options(self):
        optParser = optparse.OptionParser()
        optParser.add_option("--nogui", action="store_true",
                             default=False, help="run the commandline version of sumo")
        options, args = optParser.parse_args()
        return options

    def run(self, port, ip, startLane, endlane):
        global child_conn_vehState, parent_conn_vehState
        """execute the TraCI control loop"""
        #net = sumolib.net.readNet(netxml_file_name)
        PORT = port
        HOST_IP = ip
        nn_hostip = 'tcp://' + str(HOST_IP) + ':' + str(PORT)
        nn_pairA = Pair0(dial=nn_hostip, send_timeout=0)
        # nn_pairA.dial(nn_hostip)
        print(startLane, endlane)
        veh_startlaneid = startLane.split("@")[1]
        veh_endlaneid = endlane.split("@")[1]
        veh_startlanenum = startLane.split("@")[2]
        veh_endlanenum = endlane.split("@")[2]
        traci.route.add("trip", [veh_startlaneid, veh_endlaneid])
        traci.vehicle.add("0", "trip", typeID="car", departLane='1')

        # add(self, vehID, routeID, typeID='DEFAULT_VEHTYPE', depart='now', departLane='first', departPos='base',
        #     departSpeed='0', arrivalLane='current', arrivalPos='max', arrivalSpeed='current', fromTaz='', toTaz='',
        #     line='', personCapacity=0, personNumber=0)
        #for step in range(3600):
        while traci.simulation.getMinExpectedNumber() > 0 and self.t1_RunStatus == True:
            traci.simulationStep()
            carlist = traci.vehicle.getIDList()
            sendDict = {"data": []}

            if parent_conn_vehState.poll():
                msg_vehState = parent_conn_vehState.recv()
                veh_id = msg_vehState.split(':')[0]
                veh_state = msg_vehState.split(':')[1]
                print(veh_id, veh_state)
                veh_RoadID = traci.vehicle.getRoadID(veh_id)
                veh_edgeId = veh_RoadID.split('_')[0]
                print(veh_edgeId)
                if veh_id in carlist:
                    if veh_state == 'stop':
                        #roadid = traci.vehicle.getRoadID('0')
                        traci.vehicle.setStop('0', '618012187#1', 100)

            if '0' not in carlist:
                traci.vehicle.add("0", "trip", typeID="car")
            for cari, carid in enumerate(carlist):
            # for carid in carlist:
                dict = {"id": 0, "lat": 0, "lon": 0, "speed": 0, "brng": 0}
                sendDict['data'].append(dict)
                #current_position = traci.vehicle.getPosition(carid)
                #lng, lat = net.convertXY2LonLat(float(current_position[0]), float(current_position[1]))
                #print(lng, lat)
                x, y = traci.vehicle.getPosition(carid)
                lon, lat = traci.simulation.convertGeo(x, y)
                #print(lon, lat)
                #x2, y2 = traci.simulation.convertGeo(lon, lat, fromGeo=True)
                speed = traci.vehicle.getSpeed(carid)
                brng = traci.vehicle.getAngle(carid)
                dict['id'] = int(float(carid) * 10)
                dict['lon'] = float(lon) * 10000000
                dict['lat'] = float(lat) * 10000000
                dict['speed'] = speed
                dict['brng'] = brng
                try:
                    sendmsgjson = json.dumps(sendDict)
                    #print(sendmsgjson)
                    nn_pairA.send(sendmsgjson.encode())
                except:
                    pass


    def qfSumo_start(self, port, ip, startLane, endlane):
        options = self.get_options()
        if options.nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')
            traci.start([sumoBinary, "-c", "./test.sumocfg", "-S", "-d", "500"])

        self.t1_RunStatus = True
        self.t1 = threading.Thread(target=self.run, args=(port, ip, startLane, endlane))
        self.t1.setDaemon(True)
        self.t1.start()

    def qfSumo_stop(self):
        traci.close()
        self.t1_RunStatus = False

    def vehState_carryout(self, vehID, vehState):
        global child_conn_vehState, parent_conn_vehState
        child_conn_vehState.send(vehID + ':' + vehState)

        # roadid = traci.vehicle.getRoadID('0')
        # laneid = traci.vehicle.getLaneID('0')
        #print(roadid, laneid)
        #traci.vehicle.setStop('0', '618012187#1', 100)
        # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0, duration=-1073741824.0, flags=0, startPos=-1073741824.0,
        #         until=-1073741824.0)

