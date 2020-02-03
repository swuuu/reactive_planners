#!/usr/bin/env python

""" @namespace Controller using the dcm_vrp_planner.
@file
@copyright Copyright (c) 2017-2019,
           New York University and Max Planck Gesellschaft,
           License BSD-3-Clause
"""

import numpy as np
from reactive_planners import (
    StepperHead, DcmVrpPlanner, EndEffectorTrajectory3D)


class DcmReactiveStepper(object):
    def __init__(self, is_left_leg_in_contact, l_min, l_max, w_min, w_max,
                 t_min, t_max, l_p, com_height, weight, mid_air_foot_height,
                 control_period):
        self.control_period = control_period
        # Create the stepper head.
        self.stepper_head = StepperHead()
        # Create the dcm vrp planner and initialize it.
        self.dcm_vrp_planner = DcmVrpPlanner()
        self.dcm_vrp_planner.initialize(l_min, l_max, w_min, w_max, t_min,
                                        t_max, l_p, com_height, weight)
        # Create the end-effector trajecotry generator.
        self.end_eff_traj3d = EndEffectorTrajectory3D()
        self.end_eff_traj3d.set_mid_air_height(mid_air_foot_height)

        # Parameters
        self.is_left_leg_in_contact = is_left_leg_in_contact
        self.duration_before_step_landing = 0.0
        self.time_from_last_step_touchdown = 0.0
        self.previous_support_foot = np.array([0, 0, 0])
        self.current_support_foot = np.array([0, 0, 0])
        self.next_support_foot = np.array([0, 0, 0])
        self.des_com_vel = np.array([0, 0, 0])
        self.right_foot_position = np.matrix([[0, 0, 0]])
        self.right_foot_velocity = np.matrix([[0, 0, 0]])
        self.right_foot_acceleration = np.matrix([[0, 0, 0]])
        self.left_foot_position = np.matrix([[0, 0, 0]])
        self.flying_foot_position = np.array([0, 0, 0])
        self.left_foot_velocity = np.matrix([[0, 0, 0]])
        self.left_foot_acceleration = np.matrix([[0, 0, 0]])
        self.feasible_velocity = np.array([0, 0, 0])

    def set_des_com_vel(self, des_com_vel):
        self.des_com_vel = des_com_vel

    def run(self, time, current_flying_foot_position, com_position, com_velocity, base_yaw):
        self.stepper_head.run(
            self.duration_before_step_landing, current_flying_foot_position, time)

        self.time_from_last_step_touchdown = self.stepper_head.get_time_from_last_step_touchdown()
        self.current_support_foot = self.stepper_head.get_current_support_location()

        self.dcm_vrp_planner.update(
            self.stepper_head.get_current_support_location(),
            self.stepper_head.get_time_from_last_step_touchdown(),
            self.stepper_head.get_is_left_leg_in_contact(), self.des_com_vel,
            com_position,
            com_velocity, base_yaw)
        assert(self.dcm_vrp_planner.solve())

        self.duration_before_step_landing = self.dcm_vrp_planner.get_duration_before_step_landing()
        start_time = 0.0
        current_time = self.stepper_head.get_time_from_last_step_touchdown()
        end_time = self.dcm_vrp_planner.get_duration_before_step_landing()
        print(start_time, ":",current_time, ":", end_time)
        # check which foot is in contact
        if(self.stepper_head.get_is_left_leg_in_contact()):
            # flying foot is the right foot
            self.end_eff_traj3d.compute(
                self.stepper_head.get_previous_support_location(),
                self.right_foot_position, self.right_foot_velocity,
                self.right_foot_acceleration,
                self.dcm_vrp_planner.get_next_step_location(),
                start_time, current_time, end_time)

            self.end_eff_traj3d.get_next_state(
                current_time + self.control_period,
                self.right_foot_position,
                self.right_foot_velocity,
                self.right_foot_acceleration)
            self.flying_foot_position = self.right_foot_position
            # The current support foot does not move
            self.left_foot_position = (
                self.stepper_head.get_current_support_location())
            self.left_foot_velocity = np.array([0, 0, 0])
            self.left_foot_acceleration = np.array([0, 0, 0])
        else:
            # flying foot is the left foot
            # self.end_eff_traj3d.compute(
            #     self.stepper_head.get_previous_support_location(),
            #     self.left_foot_position, self.left_foot_velocity,
            #     self.left_foot_acceleration,
            #     self.dcm_vrp_planner.get_next_step_location(),
            #     start_time, current_time, end_time)

            self.end_eff_traj3d.get_next_state(
                current_time + self.control_period,
                self.left_foot_position,
                self.left_foot_velocity,
                self.left_foot_acceleration)
            self.flying_foot_position = self.left_foot_position
            # The current support foot does not move
            self.right_foot_position = (
                self.stepper_head.get_current_support_location())
            self.right_foot_velocity = np.array([0, 0, 0])
            self.right_foot_acceleration = np.array([0, 0, 0])

        # Compute the feasible velocity.
        self.feasible_velocity = (
            self.dcm_vrp_planner.get_next_step_location() -
            self.stepper_head.get_previous_support_location())
        self.feasible_velocity[2] = 0.0

        return


if __name__ == "__main__":

    is_left_leg_in_contact = True
    l_min = -0.5
    l_max = 0.5
    w_min = -0.5
    w_max = 0.5
    t_min = 0.1
    t_max = 0.2
    l_p = 0.1235 * 2
    com_height = 0.26487417
    weight = [1, 1, 5, 100, 100, 100, 100, 100, 100]
    mid_air_foot_height = 0.05
    control_period = 0.001
    dcm_reactive_stepper = DcmReactiveStepper(is_left_leg_in_contact, l_min,
                                              l_max, w_min, w_max, t_min, t_max,
                                              l_p, com_height, weight,
                                              mid_air_foot_height,
                                              control_period)

    time = 0.0
    current_support_foot = np.array([0, 0, 0])
    com_position = np.array([0, 0, com_height])
    com_velocity = np.array([0, 0, 0])
    base_yaw = 0.

    dcm_reactive_stepper.run(time, current_support_foot,
                             com_position, com_velocity, base_yaw)

    dcm_reactive_stepper.right_foot_position
    dcm_reactive_stepper.right_foot_velocity
    dcm_reactive_stepper.right_foot_acceleration
    dcm_reactive_stepper.left_foot_position
    dcm_reactive_stepper.left_foot_velocity
    dcm_reactive_stepper.left_foot_acceleration