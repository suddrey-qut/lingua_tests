import rospy
import pymongo
from sensor_msgs.msg import JointState
from lingua_world.srv import GetObjectPose, GetObjectPoseRequest

from geometry_msgs.msg import PoseWithCovarianceStamped

client = pymongo.MongoClient()
db = client.lingua

collection = db.objects

def at(args):
  location_id = args[0]
  object_id = args[1]
  print('wtf')
  pose_covariance = rospy.wait_for_message('/amcl_pose', PoseWithCovarianceStamped)
  
  srv = rospy.ServiceProxy('/lingua/world/get_pose', GetObjectPose)
  srv.wait_for_service()

  ps = srv(location_id).pose_stamped
  print(ps)

  result = collection.find({'$and': [
    {'position.pose.position.x': {'$gte': ps.pose.position.x - 0.2}}, 
    {'position.pose.position.x': {'$lte': ps.pose.position.x + 0.2}}, 
    {'position.pose.position.y': {'$gte': ps.pose.position.y - 0.2}},
    {'position.pose.position.y': {'$lte': ps.pose.position.y + 0.2}},
    {'position.pose.position.z': {'$gte': -0.1}}, 
    {'position.pose.position.z': {'$lte': 0.1}}, 
  ]})

  ids = [item['object_id'] for item in result]
  
  if pose_covariance.pose.pose.position.x > ps.pose.position.x - 0.2 and pose_covariance.pose.pose.position.x < ps.pose.position.x + 0.2 and \
     pose_covariance.pose.pose.position.y > ps.pose.position.y - 0.2 and pose_covariance.pose.pose.position.y < ps.pose.position.y  + 0.2:
     print('Agent at location')
     ids.append('agent')

  if args[1] == '?':
    return ids
  
  return args[1] in ids