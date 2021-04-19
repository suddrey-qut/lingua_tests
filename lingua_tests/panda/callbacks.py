import rospy
import pymongo
from sensor_msgs.msg import JointState
from lingua_world.srv import GetObjectPose, GetObjectPoseRequest
from rv_msgs.msg import ManipulatorState

client = pymongo.MongoClient()
db = client.lingua

collection = db.objects


def gripper_open(args):
  if args[0] == '?':
    return ['g1'] if gripper_open('g1') else []
  
  msg = rospy.wait_for_message('/franka_gripper/joint_states', JointState)
  return msg.position[0] > 0.035 and msg.position[1] > 0.035

def on(args):
  location_id = args[0]
  object_id = args[1]
  
  ee_pose = rospy.wait_for_message('/arm/state', ManipulatorState)

  srv = rospy.ServiceProxy('/lingua/world/get_pose', GetObjectPose)
  srv.wait_for_service()

  ps = srv(location_id).pose_stamped
  
  result = collection.find({'$and': [
    {'position.pose.position.x': {'$gte': ps.pose.position.x - 0.2}}, 
    {'position.pose.position.x': {'$lte': ps.pose.position.x + 0.2}}, 
    {'position.pose.position.y': {'$gte': ps.pose.position.y - 0.2}},
    {'position.pose.position.y': {'$lte': ps.pose.position.y + 0.2}},
    {'position.pose.position.z': {'$gte': -0.1}}, 
    {'position.pose.position.z': {'$lte': 0.1}}, 
  ]})

  ids = [item['object_id'] for item in result]

  print('EE Pose')
  print(ee_pose)

  print('Target')
  print(ps)
  
  if ee_pose.pose.position.x > ps.pose.position.x - 0.2 and ee_pose.pose.position.x < ps.pose.position.x + 0.2 and \
     ee_pose.pose.position.y > ps.pose.position.y - 0.2 and ee_pose.pose.position.y < ps.pose.position.y  + 0.2:
     
     ids.append('g1')

  if object_id == '?':
    return ids
  
  return object_id in ids