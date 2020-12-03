import rospy
from wire_msgs.msg import *
from problib.msg import *


if __name__ == '__main__':
  rospy.init_node('generate_evidence_py')

  publisher = rospy.Publisher('/world_evidence', WorldEvidence, queue_size=100)

  world_evidence = WorldEvidence()

  object_evidence = ObjectEvidence()

  x = 2
  y = 5
  z = 3

  covariance = 0.008
  
  object_evidence.properties.append(Property(attribute='class_label', pdf=PDF(
    type=PDF.DISCRETE,
    values=['ball'],
    probabilities=[0.7],
    domain_size=-1
  )))
  object_evidence.properties.append(Property(attribute='color', pdf=PDF(
    type=PDF.DISCRETE,
    values=['yellow'],
    probabilities=[0.7],
    domain_size=-1
  )))

  object_evidence.properties.append(Property(attribute='position', pdf=PDF(
    type=PDF.GAUSSIAN,
    dimensions=3,
    data=[PDF.GAUSSIAN, x, y, z, covariance, 0, 0, covariance, 0, covariance]
  )))

  world_evidence.header.stamp = rospy.Time.now()
  world_evidence.header.frame_id = '/map'

  world_evidence.object_evidence.append(object_evidence)

  while not rospy.is_shutdown():
    publisher.publish(world_evidence)
  