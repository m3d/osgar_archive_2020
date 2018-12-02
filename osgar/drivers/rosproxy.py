"""
  ROS (Robot Operating System) Proxy
"""

from threading import Thread
import struct
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

import socket


from osgar.bus import BusShutdownException

NODE_HOST, NODE_PORT = ('127.0.0.1', 8000)
PUBLISH_PORT = 8123


ROS_MESSAGE_TYPES = {
    'std_msgs/String': '992ce8a1687cec8c8bd883ec73ca41d1',
    'geometry_msgs/Twist': '9f195f881246fdfa2798d1d3eebca84a',
    'std_msgs/Imu': '6a62c6daae103f4ff57a132d6f95cec2',

    #hacked
    'sensor_msgs/LaserScan': '0002c6daae103f4ff57a132d6f95cec2',
    'sensor_msgs/Image': '0012c6daae103f4ff57a132d6f95cec2',
}


def prefix4BytesLen(s):
    "adding ROS length"
    if type(s) == str:
        s = bytes(s, encoding='ascii')
    return struct.pack("I", len(s)) + s


def packCmdVel(speed, angularSpeed):
    return struct.pack("dddddd", speed,0,0, 0,0,angularSpeed)


def publisherUpdate(caller_id, topic, publishers):
    print("called 'publisherUpdate' with", (caller_id, topic, publishers))
    return (1, "Hi, I am fine", 42) # (code, statusMessage, ignore) 

def requestTopic(caller_id, topic, publishers):
    print("REQ", (caller_id, topic, publishers))
    return 1, "ready on martind-blabla", ['TCPROS', NODE_HOST, PUBLISH_PORT]


class MyXMLRPCServer( Thread ):
    def __init__( self, nodeAddrHostPort ):
        Thread.__init__( self )
        self.setDaemon( True )
        self.server = SimpleXMLRPCServer( nodeAddrHostPort )
        print("Listening on port %d ..." % nodeAddrHostPort[1])
        self.server.register_function(publisherUpdate, "publisherUpdate")
        self.server.register_function(requestTopic, "requestTopic")
        self.start()

    def run( self ):
        self.server.serve_forever()


class ROSProxy(Thread):
    def __init__(self, config, bus):
        Thread.__init__(self)
        self.setDaemon(True)

        self.bus = bus
        self.ros_master_uri = config['ros_master_uri']
        self.ros_client_uri = config['ros_client_uri']
        self.topic = config['topic']
        self.topic_type = config['topic_type']
        self.subscribe_list = config.get('subscribe', [])
        self.caller_id = "/osgar_node"  # do we need this in configuration? (Yes for more ROSProxy nodes)

    def subscribe_topic(self, topic, topic_type, publish_name):
        print('Subscribe', topic)
        code, status_message, publishers = self.master.registerSubscriber(
                self.caller_id, topic, topic_type, self.ros_client_uri)
        assert code == 1, (code, status_message)
        assert len(publishers) == 1, (topic, publishers) # i.e. fails if publisher is not ready now
        print(publishers)

        publisher = ServerProxy(publishers[0])
        code, status_message, protocol_params = publisher.requestTopic(self.caller_id, topic, [["TCPROS"]])
        assert code == 1, (code, status_message)
        assert len(protocol_params) == 3, protocol_params
        print(code, status_message, protocol_params)
        
        # define TCP connection
        #self.bus.publish('imu_data', [protocol_params[1], protocol_params[2]])
        self.bus.publish(publish_name, ['127.0.0.1', protocol_params[2]])        

        # initialize connection
        header = prefix4BytesLen(
            prefix4BytesLen('callerid=' + self.caller_id) +
            prefix4BytesLen('topic=' + topic) +
            prefix4BytesLen('type=' + topic_type) +
            prefix4BytesLen('md5sum=' + ROS_MESSAGE_TYPES[topic_type])
            )
        self.bus.publish(publish_name, header)

    def run(self):
        self.server = MyXMLRPCServer( (NODE_HOST, NODE_PORT) )
        self.master = ServerProxy(self.ros_master_uri)
        code, status_message, system_state = self.master.getSystemState('/')
        assert code == 1, code
        assert len(system_state) == 3, system_state
        print("Publishers:")
        for s in system_state[0]:
            print(s)

        for topic, topic_type, publish_name in self.subscribe_list:
            self.subscribe_topic(topic, topic_type, publish_name)

        code, status_message, subscribers = self.master.registerPublisher(
                self.caller_id, self.topic, self.topic_type, self.ros_client_uri)

        print("Subscribers:")
        print(subscribers)

#        NODE_HOST = '192.168.23.12'
#        PUBLISH_PORT = 8123

#        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#        serverSocket.bind((NODE_HOST, PUBLISH_PORT))
#        print("Waiting ...")
#        serverSocket.listen(1)
#        soc, addr = serverSocket.accept() 
#        print('Connected by', addr)
#        data = soc.recv(1024) # TODO properly load and parse/check
#        print(data)
#        print("LEN", len(data))

#        code, status_message, num_unreg = master.unregisterPublisher(
#                caller_id, self.topic, self.ros_client_uri)
#        print("Unregistered", code, status_message, num_unreg)

        header = prefix4BytesLen(
            prefix4BytesLen('callerid=' + self.caller_id) +
            prefix4BytesLen('topic=' + self.topic) +
            prefix4BytesLen('type=' + self.topic_type) +
            prefix4BytesLen('md5sum=' + ROS_MESSAGE_TYPES[self.topic_type])
            )

        try:
            ready = False
#            self.bus.publish('cmd_vel', header)  # TODO topic dependent!
            while True:
                timestamp, channel, data = self.bus.listen()
                if channel != 'tick':
                    print(timestamp, channel)
                if channel == 'cmd_vel':
                    self.bus.publish('cmd_vel', header)
                    ready = True
                if ready and channel == 'tick':
                    cmd = prefix4BytesLen(packCmdVel(-0.5, 0.0))
                    self.bus.publish('cmd_vel', cmd)
        except BusShutdownException:
            pass

    def request_stop(self):
        self.bus.shutdown()

# vim: expandtab sw=4 ts=4
