# -*- coding: utf-8 -*-
import copy
import os
import libconf

from xml.etree import ElementTree as ET
from collections import Counter
from xpinyin import Pinyin
from geographiclib.geodesic import Geodesic


class XmlParse(object):
    def __init__(self, parent=None):
        super(XmlParse, self).__init__()

    def osm2MapConf(self, osmFIle, nodeName, region, id):
        dict = {"V2XMAP": {"MAPTX": {"MsgContent": [{"msgCount": 0, "timeStamp": 0, "nodes": []}]}}}
        dictNode = {"desptName": nodeName, "nodeRefID": {"region": region, "id": id}, "refPoint": [0, 0], "links": []}
        wayTypeList = ['highway', 'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']
        tree = ET.parse(osmFIle)
        root = tree.getroot()
        bounds_object = root.find("bounds")
        node_refPoint = [0, 0]
        node_refPoint[0] = (float(bounds_object.attrib['minlat']) + float(bounds_object.attrib['maxlat'])) / 2
        node_refPoint[1] = (float(bounds_object.attrib['minlon']) + float(bounds_object.attrib['maxlon'])) / 2
        dictNode['refPoint'][0] = int(node_refPoint[0] * 10000000)
        dictNode['refPoint'][1] = int(node_refPoint[1] * 10000000)

        for way_child in root.iter('way'):
            tag_list = []
            nd_list = []
            for tag_child in way_child.iter('tag'):
                tag_list.append(tag_child.attrib)
            for nd_child in way_child.iter('nd'):
                nd_list.append(nd_child.attrib)

            for tag in tag_list:
                if tag['k'] == 'highway' and tag['v'] in wayTypeList:
                    break
            else:
                continue
            dictMovements = {"remoteNodeID": {"region": 0, "id": 0}, "signalGroup": 0}
            dictLink = {"desptName": "", "upstreamNodeId": {"region": 0, "id": 0},
                        "speedLimits": [{"type": 4, "speed": 0}, {"type": 5, "speed": 0}], "laneWidth": 0,
                        "points": [], "movements": [], "lanes": []}
            dictLanes = {"laneID": 0, "laneWidth": 0,
                         "laneAttributes": {"sharedWith": 0, "laneType": {"present": 1, "value": 1}}, "maneuvers": 1,
                         "points": [], "conctTo": [],
                         "speedLimits": [{"type": 4, "speed": 0}, {"type": 5, "speed": 0}]}
            dictConctTo = {"remoteNodeID": {"region": 0, "id": 2},
                           "connectingLane": {"laneID": 0, "maneuvers": 1}, "signalGroup": 1}
            lane_name = 'unknown'
            lane_num = 1
            for tag in tag_list:
                if tag['k'] == 'name':
                    p = Pinyin()
                    lane_name = p.get_pinyin(tag['v'])
                if tag['k'] == 'lanes':
                    lane_num = int(tag['v'])
            #print(lane_name, lane_num)
            pos_list = []
            pos_naked_list = []
            for nd in nd_list:
                dictPoint = {"present": 7, "value": [0, 0]}
                for node_child in root.iter('node'):
                    if node_child.attrib['id'] == nd['ref']:
                        #print(float(node_child.attrib['lat']), float(node_child.attrib['lon']))
                        dictPoint['value'][0] = int(float(node_child.attrib['lat']) * 10000000)
                        dictPoint['value'][1] = int(float(node_child.attrib['lon']) * 10000000)
                        pos_list.append(dictPoint)
                        pos_naked_list.append([float(node_child.attrib['lat']), float(node_child.attrib['lon'])])
            if len(pos_list) > 1:
                if lane_num == 1:
                    tmp_dictConctTo = copy.deepcopy(dictConctTo)
                    tmp_dictLanes = copy.deepcopy(dictLanes)
                    tmp_dictLanes['laneID'] = 1
                    tmp_dictLanes['conctTo'].append(tmp_dictConctTo)
                    tmp_dictLanes['points'] = pos_list
                    dictLink['lanes'].append(tmp_dictLanes)
                elif lane_num == 2:
                    lane_pos_list1 = []
                    lane_pos_list2 = []
                    for pi in range(len(pos_naked_list) - 1):
                        #print(pos_naked_list[pi], pos_naked_list[pi + 1])
                        geo = Geodesic.WGS84.Inverse(pos_naked_list[pi][0], pos_naked_list[pi][1],
                                                     pos_naked_list[pi + 1][0], pos_naked_list[pi + 1][1])

                        tarloc1 = Geodesic.WGS84.Direct(pos_naked_list[pi][0],
                                                        pos_naked_list[pi][1], geo['azi1'] - 90, 2)
                        lane_pos_list1.append([tarloc1['lat2'], tarloc1['lon2']])
                        tarloc2 = Geodesic.WGS84.Direct(pos_naked_list[pi][0],
                                                        pos_naked_list[pi][1], geo['azi1'] + 90, 2)
                        lane_pos_list2.append([tarloc2['lat2'], tarloc2['lon2']])
                        #print([tarloc1['lat2'], tarloc1['lon2']], [tarloc2['lat2'], tarloc2['lon2']])
                        if pi == (len(pos_naked_list) - 1):
                            tarloc1 = Geodesic.WGS84.Direct(pos_naked_list[pi + 1][0],
                                                            pos_naked_list[pi + 1][1], geo['azi1'] + 90, 2)
                            lane_pos_list1.append(tarloc1)
                            tarloc2 = Geodesic.WGS84.Direct(pos_naked_list[pi + 1][0],
                                                            pos_naked_list[pi + 1][1], geo['azi1'] - 90, 2)
                            lane_pos_list2.append(tarloc2)

                    tmp_dictConctTo1 = copy.deepcopy(dictConctTo)
                    tmp_dictLanes1 = copy.deepcopy(dictLanes)
                    tmp_dictLanes1['laneID'] = 1
                    tmp_dictLanes1['conctTo'].append(tmp_dictConctTo1)
                    tmp_dictLanes1['points'] = lane_pos_list1
                    dictLink['lanes'].append(tmp_dictLanes1)

                    tmp_dictConctTo2 = copy.deepcopy(dictConctTo)
                    tmp_dictLanes2 = copy.deepcopy(dictLanes)
                    tmp_dictLanes2['laneID'] = 2
                    tmp_dictLanes2['conctTo'].append(tmp_dictConctTo2)
                    tmp_dictLanes2['points'] = lane_pos_list2
                    dictLink['lanes'].append(tmp_dictLanes2)

                dictLink['desptName'] = lane_name
                dictLink['points'].append(pos_list[0])
                dictLink['points'].append(pos_list[-1])
                dictLink['movements'].append(dictMovements)
            else:
                continue
            dictNode['links'].append(dictLink)

        list_remote_attr = []
        for i, link in enumerate(dictNode['links']):
            dict_remote_attr = {'pos': link['points'][0]['value'], 'id': i * 2 + 1}
            list_remote_attr.append(dict_remote_attr)
            dict_remote_attr = {'pos': link['points'][1]['value'], 'id': i * 2 + 2}
            list_remote_attr.append(dict_remote_attr)
        for r1 in list_remote_attr:
            for r2 in list_remote_attr:
                if r1['pos'] == r2['pos']:
                    r2['id'] = r1['id']

        id_all_list = []
        for id_attr in list_remote_attr:
            id_all_list.append(id_attr['id'])
        id_cnt_dict = Counter(id_all_list)
        for id_key, id_value in id_cnt_dict.items():
            if id_value > 1:
                for id_attr in list_remote_attr:
                    if id_attr['id'] == id_key:
                        id_attr['id'] = dictNode['nodeRefID']['id']

        for i, link in enumerate(dictNode['links']):
            for rlist in list_remote_attr:
                if link['points'][0]['value'] == rlist['pos']:
                    link['upstreamNodeId']['id'] = rlist['id']
                    link['upstreamNodeId']['region'] = dictNode['nodeRefID']['region']
                if link['points'][1]['value'] == rlist['pos']:
                    link['movements'][0]['remoteNodeID']['id'] = rlist['id']
                    link['movements'][0]['remoteNodeID']['region'] = dictNode['nodeRefID']['region']
                    for llane in link['lanes']:
                        llane['conctTo'][0]['remoteNodeID']['region'] = dictNode['nodeRefID']['region']
                        llane['conctTo'][0]['remoteNodeID']['id'] = rlist['id']

        dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'].append(dictNode)

        if os.path.exists('v2xRsuGbMap.cfg.tmp'):
            os.remove('v2xRsuGbMap.cfg.tmp')
        if os.path.exists('v2xRsuGbMap.cfg'):
            os.rename('v2xRsuGbMap.cfg', 'v2xRsuGbMap.cfg.tmp')
        for node in dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']:
            for link in node['links']:
                link['speedLimits'] = libconf.LibconfList(link['speedLimits'])
                link['points'] = libconf.LibconfList(link['points'])
                link['movements'] = libconf.LibconfList(link['movements'])
                for lanes in link['lanes']:
                    lanes['points'] = libconf.LibconfList(lanes['points'])
                    lanes['conctTo'] = libconf.LibconfList(lanes['conctTo'])
                    lanes['speedLimits'] = libconf.LibconfList(lanes['speedLimits'])
                link['lanes'] = libconf.LibconfList(link['lanes'])
            node['links'] = libconf.LibconfList(node['links'])
        dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'] = \
            libconf.LibconfList(dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'])
        dict['V2XMAP']['MAPTX']['MsgContent'] = \
            libconf.LibconfList(dict['V2XMAP']['MAPTX']['MsgContent'])

        configText = libconf.dumps(dict)
        with open('v2xRsuGbMap.cfg', 'w') as fd_file:
            fd_file.write(configText)
            fd_file.close()

    def getLanesInfo(self, osmFIle, netFIle):
        lanesInfoList = []
        wayTypeList = ['highway', 'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']
        osmTree = ET.parse(osmFIle)
        osmRoot = osmTree.getroot()
        osmLaneInfoList = []
        for way_child in osmRoot.iter('way'):
            osmLaneInfoDict = {'laneName': 'unknown', 'laneNum': 1, 'id': ''}
            tag_list = []
            nd_list = []
            for tag_child in way_child.iter('tag'):
                tag_list.append(tag_child.attrib)
            for nd_child in way_child.iter('nd'):
                nd_list.append(nd_child.attrib)
            for tag in tag_list:
                if tag['k'] == 'highway' and tag['v'] in wayTypeList:
                    break
            else:
                continue
            osmLaneInfoDict['id'] = way_child.attrib['id']
            for tag in tag_list:
                if tag['k'] == 'name':
                    p = Pinyin()
                    osmLaneInfoDict['laneName'] = p.get_pinyin(tag['v'])
                if tag['k'] == 'lanes':
                    osmLaneInfoDict['laneNum'] = int(tag['v'])
            osmLaneInfoList.append(osmLaneInfoDict)
        #jiexi net file
        tree = ET.parse(netFIle)
        root = tree.getroot()
        for osmlaneinfo in osmLaneInfoList:
            laneInfoDict = {'laneName': 'unknown', 'laneNum': 1, 'id_list': []}
            for edge_child in root.iter('edge'):
                try:
                    lanesType = edge_child.attrib['type']
                    waylane = lanesType.split(".")[1]
                    if waylane not in wayTypeList:
                        continue
                except:
                    continue
                netId = edge_child.attrib['id']
                netidname = netId.split("#")[0]
                if osmlaneinfo['id'] == netidname:
                    laneInfoDict['laneNum'] = osmlaneinfo['laneNum']
                    laneInfoDict['laneName'] = osmlaneinfo['laneName']
                    laneInfoDict['id_list'].append(netId)
            lanesInfoList.append(laneInfoDict)
        return lanesInfoList

    def creatRouXmlFile(self, veh_dict_list):
        carType_list = ['passenger', 'bus', 'bicycle', 'pedestrian']
        root = ET.Element("routes")  # 创建一个标签tagName1
        root.text = '\n    '
        for carType in carType_list:
            string = ET.SubElement(root, 'vType')
            string.tail = '\n    '
            string.attrib = {'id': 'car', 'vClass': carType, 'accel': "2.6", 'decel': "4.5", 'sigma': "0.5",
                             'length': "5", 'maxSpeed': "20"}
        for veh_dict in veh_dict_list:
            print(veh_dict)
            string = ET.SubElement(root, 'flow')
            string.tail = '\n    '
            string.attrib = veh_dict
        tree = ET.ElementTree(root)
        tree.write("newCreate.xml", xml_declaration=True, encoding="utf-8", short_empty_elements=True)
        # xml_declaration是否包含声明文件， encoding编码方式，short_empty_elements 规定是短标签（单标签）还是双标签

