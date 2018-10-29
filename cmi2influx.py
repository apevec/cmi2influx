#!/usr/bin/python3

import json
import requests
from influxdb import InfluxDBClient 
import configparser
import sys

configfilename=sys.argv[1]
config = configparser.ConfigParser()
config.read(configfilename)

ip=config.get('main','ip')
can_node=config.get('main','can_node')
username=config.get('main','username')
password=config.get('main','password')
influxip=config.get('main','influxip')
influxdb=config.get('main','influxdb')
influxusername=config.get('main','influxusername')
influxpassword=config.get('main','influxusername')
influxtaghost=config.get('main','influxtaghost')
influxtagregion=config.get('main','influxtagregion')

url = "http://"+ip+"/INCLUDE/api.cgi?jsonnode="+can_node+"&jsonparam=I,O,Na";

result = requests.get(url, auth=(username, password)).text
data = json.loads(result) 

input_data = data["Data"]["Inputs"]
output_data = data["Data"]["Outputs"]
networkanalog_data = data["Data"]["Network Analog"]

inputs={}
for key in input_data:
 inputs[key["Number"]]=key["Value"]["Value"]

networkanalog={}
for key in networkanalog_data:
 networkanalog[key["Number"]]=key["Value"]["Value"] 

outputs={}
for key in output_data:
 outputs[key["Number"]]=key["Value"]["Value"]


#
# Adapt things below this for your own UVR1611 installation
# 

# EfG.de WP with WEM2
# TODO move parameter mapping to the config
##inputs:
#AussentemperaturS1
#SpeicherkuppelS2
#SpeicherkopfS3
#SpeicherHeizoneObenS4
#SpeicherHeizoneUntenS5
#SpeicherLadeleitungS6
#RaumtemperaturS8
#WA_VLT_S10
#WA_RLT_S11
#WE2_BT_S12
#SolareinspeisetemperaturS13
#SolarstrahlungS15
#WE2_RLT_S16
##outputs:
#AnforderungWE1
##networkanalog:
#WP_Zielspreizung
#WP_kWh
#WP_COP
#WP_Vorlauftemperatur
#WP_Ruecklauftemperatur
#WP_Systemtemperatur
AussentemperaturS1 = inputs[1]
SpeicherkuppelS2 = inputs[2]
SpeicherkopfS3 = inputs[3]
SpeicherHeizoneObenS4 = inputs[4]
SpeicherHeizoneUntenS5 = inputs[5]
SpeicherLadeleitungS6 = inputs[6]
RaumtemperaturS8 = inputs[8]
WA_VLT_S10 = inputs[10]
WA_RLT_S11 = inputs[11]
WE2_BT_S12 = inputs[12]
WE2_RLT_S16 = inputs[16]
AnforderungWE1 = outputs[5]
WP_Zielspreizung = networkanalog[1]
WP_kWh = networkanalog[2]
WP_COP = networkanalog[3]
WP_Vorlauftemperatur = networkanalog[4]
WP_Ruecklauftemperatur = networkanalog[5]
WP_Systemtemperatur = networkanalog[6]

client = InfluxDBClient(influxip,8086, influxusername, influxpassword, influxdb)
json_body = [
{
            "measurement": "heating",
            "tags": {
                "host": influxtaghost,
                "region": influxtagregion
            },
            "fields": {
                "AussentemperaturS1":     AussentemperaturS1,
                "SpeicherkuppelS2":       SpeicherkuppelS2,
                "SpeicherkopfS3":         SpeicherkopfS3,
                "SpeicherHeizoneObenS4":  SpeicherHeizoneObenS4,
                "SpeicherHeizoneUntenS5": SpeicherHeizoneUntenS5,
                "SpeicherLadeleitungS6":  SpeicherLadeleitungS6,
                "RaumtemperaturS8":       RaumtemperaturS8,
                "WA_VLT_S10":             WA_VLT_S10,
                "WA_RLT_S11":             WA_RLT_S11,
                "WE2_BT_S12":             WE2_BT_S12,
                "WE2_RLT_S16":            WE2_RLT_S16,
                "AnforderungWE1":         AnforderungWE1,
                "WP_Zielspreizung":       WP_Zielspreizung,
                "WP_kWh":                 WP_kWh,
                "WP_COP":                 WP_COP,
                "WP_Vorlauftemperatur":   WP_Vorlauftemperatur,
                "WP_Ruecklauftemperatur": WP_Ruecklauftemperatur,
                "WP_Systemtemperatur":    WP_Systemtemperatur
            }
        }
    ]
    
#
# Adapt things above this for your own UVR1611 installation
#

client.write_points(json_body)
