"""
  Proxy for ROS sensors and effectors
  this is Python 2.7 code
"""

import sys
import rospy

from rospy_rover import RospyRover, RospyRoverReqRep, RospyRoverPushPull
from srcp2_msgs.msg import VolSensorMsg

class RospyScoutPushPull(RospyRoverPushPull):
    def __init__(self, robot_name, push_port, pull_port):
        super(RospyScoutPushPull, self).__init__(robot_name, push_port, pull_port)
        
    def register_handlers(self):
        super(RospyScoutPushPull, self).register_handlers()

        rospy.Subscriber('/' + self.robot_name + '/volatile_sensor', VolSensorMsg, self.callback_topic, '/' + self.robot_name + '/volatile_sensor')

class RospyScoutReqRep(RospyRoverReqRep):
    def __init__(self, robot_name, reqrep_port):
        super(RospyScoutReqRep, self).__init__(robot_name, reqrep_port)


class RospyScout(RospyRover):
        
    def launch(self, argv):
        super(RospyScout, self).launch(RospyScoutPushPull, RospyScoutReqRep, argv)
        
if __name__ == '__main__':
    rs = RospyScout()
    rs.launch(sys.argv[1:])
