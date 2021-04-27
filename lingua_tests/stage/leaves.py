import json
import rospy

from rv_trees.leaves_ros import ServiceLeaf, ActionLeaf
from rv_trees.leaves import Leaf
from lingua.types import Object

from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped

import lingua_tests.patrol.callbacks as callbacks

class SetObjectPoseAMCL(ServiceLeaf):
  def __init__(self, name=None, overwrite=False, *args, **kwargs):
    super(SetObjectPoseAMCL, self).__init__(
      name=name if name else 'Get Object Pose',
      service_name='/lingua/world/set_pose',
      load_fn=self.load_fn,
      *args,
      **kwargs
    )
    self.overwrite = overwrite

  def load_fn(self):
    frame = self._service_class._request_class()
    value = self._default_load_fn(False)
    
    ps_with_covariance = rospy.wait_for_message('/amcl_pose', PoseWithCovarianceStamped)
    ps = PoseStamped(header=ps_with_covariance.header)
    ps.pose.position = ps_with_covariance.pose.pose.position
    ps.pose.orientation = ps_with_covariance.pose.pose.orientation

    if not isinstance(value, Object):
      return False

    frame.object_id = value.get_id()[0] if value.get_id() and not self.overwrite else ''
    frame.class_label = value.get_name()

    frame.pose_stamped = ps
    frame.overwrite = self.overwrite
      
    return frame

class AtLocation(Leaf):
  def __init__(self, name=None, *args, **kwargs):
    super(AtLocation, self).__init__(
      name=name if name else 'Is At Location',
      eval_fn=self.eval_fn,
      *args,
      **kwargs
    )

  def eval_fn(self, value):
    location_id = value.get_id()[0]
    result = callbacks.at([location_id, 'agent'])
    return result

class RingBell(ActionLeaf):
  def __init__(self, name=None, *args, **kwargs):
    super(RingBell, self).__init__(
      name=name if name else 'Ring Bell',
      action_namespace='/count',
      load_fn=self.load_fn,
      *args,
      **kwargs
    )

  def load_fn(self):
    goal = self._default_load_fn()
    goal.time = 4
    return goal

class LockBrakes(ActionLeaf):
  def __init__(self, name=None, *args, **kwargs):
    super(LockBrakes, self).__init__(
      name=name if name else 'Lock Brakes',
      action_namespace='/brakes',
      load_fn=self.load_fn,
      *args,
      **kwargs
    )

  def load_fn(self):
    goal = self._default_load_fn()
    goal.enabled = True
    return goal

class UnlockBrakes(ActionLeaf):
  def __init__(self, name=None, *args, **kwargs):
    super(UnlockBrakes, self).__init__(
      name=name if name else 'Unlock Brakes',
      action_namespace='/brakes',
      load_fn=self.load_fn,
      *args,
      **kwargs
    )

  def load_fn(self):
    goal = self._default_load_fn()
    goal.enabled = False
    return goal
