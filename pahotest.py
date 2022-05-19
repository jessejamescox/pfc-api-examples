import paho.mqtt.client as mqtt #import the client1
import json
import time

def get_value(msg, module, channel):
    md = 'module' + str(module)
    ch = 'channel' + str(channel)

    # read the dictionary object
    myValue = msg.get('state').get('reported').get('modules').get(md).get('process_data').get('inputs').get(ch).get('value')

    # return the read value
    return myValue

############
def on_message(client, userdata, message):

    pub_topic = "PFCX00/controller/kbus/event/outputs"
    
    # read the payload into a string
    msg = json.loads(str(message.payload.decode("utf-8")))
    
    # parse the thermocouple value for module 3 channel 2
    tcValue = get_value(msg, 3, 2) / 10
    print(tcValue)

    # parse the di value for module 1 channel 1
    boolValue = get_value(msg, 2, 1)

    outMsg = {
            "state": {
                "desired": {
                    "modules": {
                        "module1": {
                            "process_data": {
                                "outputs": {
                                    "channel1": {
                                        "value": boolValue
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

    client.publish(pub_topic, json.dumps(outMsg))

    print(boolValue)
############

broker_address= "192.168.1.176"
sub_topic = "PFCX00/controller/status"

client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback

client.connect(broker_address) #connect to broker

# loop the subscribe
while 1:
    client.loop_start() #start the loop

    client.subscribe(sub_topic)

    #time.sleep(4) # wait

    client.loop_stop() #stop the loopls