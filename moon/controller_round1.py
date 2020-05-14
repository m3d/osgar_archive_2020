"""
  Space Robotics Challenge 2
"""
import zmq

from osgar.lib import quaternion
from moon.controller import SpaceRoboticsChallenge

class SpaceRoboticsChallengeRound1(SpaceRoboticsChallenge):
    def __init__(self, config, bus):
        super().__init__(config, bus)

    def on_object_reached(self, timestamp, data):
        object_type = data
        x,y,z = self.xyz
        print(self.time, "app: Object %s reached" % object_type)
        self.socket_out.send_string('artf %s %f %f 0.0\n' % (object_type, x, y))
        response = self.socket_out.recv().decode("ascii") 
        print(self.time, "app: Volatile report response: %s" % response)
        if response == 'ok':
            pass
        else:
            # do nothing, ie keep going around and try to match the view
            pass
        
    def run(self):
        self.socket_out.send_string('request_origin')
        message = self.socket_out.recv().decode("ascii") 
        print ("controller round 1: origin received: %s" % message)

        super().run()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Space Robotics Challenge 2')
    args = parser.parse_args()

if __name__ == "__main__":
    main()

# vim: expandtab sw=4 ts=4
