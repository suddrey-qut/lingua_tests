import rospy
from lingua_tests.srv import GetBrakeStatus

def locked(args):
  srv = rospy.ServiceProxy('/brakes/locked', GetBrakeStatus)
  result = srv()

  if args[0] == '?':
    return ['agent'] if result.enabled else []
  
  return result.enabled
