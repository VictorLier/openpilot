#!/usr/bin/env python3
import unittest
import numpy as np

from selfdrive.controls.lib.longitudinal_mpc_lib.long_mpc import RW
from selfdrive.test.longitudinal_maneuvers.maneuver import Maneuver


def run_following_distance_simulation(v_lead, t_end=100.0):
  man = Maneuver(
    '',
    duration=100.,
    initial_speed=float(v_lead),
    lead_relevancy=True,
    initial_distance_lead=160,
    speed_lead_values=[v_lead],
    speed_lead_breakpoints=[0.],
  )
  valid, output = man.evaluate()
  assert valid
  return output[-1,2] - output[-1,1]


class TestFollowingDistance(unittest.TestCase):
  def test_following_distanc(self):
    for speed in np.arange(0, 40, 5):
      print(f'Testing {speed} m/s')
      v_lead = float(speed)

      simulation_steady_state = run_following_distance_simulation(v_lead)
      correct_steady_state = RW(v_lead, v_lead) + 4.0

      self.assertAlmostEqual(simulation_steady_state, correct_steady_state, delta=(correct_steady_state*.1 + .3))


if __name__ == "__main__":
  unittest.main()
