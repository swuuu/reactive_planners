/**
 * @file
 * @license BSD 3-clause
 * @copyright Copyright (c) 2020, New York University and Max Planck
 * Gesellschaft
 *
 * @brief Python bindings for the StepperHead class
 */

#include "reactive_planners/dcm_reactive_stepper.hpp"
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

using namespace reactive_planners;

void bind_dcm_reactive_stepper(pybind11::module &module)
{
    pybind11::class_<DcmReactiveStepper>(module, "DcmReactiveStepper")
        .def(pybind11::init<>())

        // Public methods.
        .def("initialize", &DcmReactiveStepper::initialize)
        .def("run", &DcmReactiveStepper::run)
        .def("start", &DcmReactiveStepper::start)
        .def("stop", &DcmReactiveStepper::stop)
        // Getters.
        .def("get_right_foot_position",
             &DcmReactiveStepper::get_right_foot_position)
        .def("get_right_foot_velocity",
             &DcmReactiveStepper::get_right_foot_velocity)
        .def("get_right_foot_acceleration",
             &DcmReactiveStepper::get_right_foot_acceleration)
        .def("get_left_foot_position",
             &DcmReactiveStepper::get_left_foot_position)
        .def("get_left_foot_velocity",
             &DcmReactiveStepper::get_left_foot_velocity)
        .def("get_left_foot_acceleration",
             &DcmReactiveStepper::get_left_foot_acceleration)
        .def("get_previous_support_foot_position",
             &DcmReactiveStepper::get_previous_support_foot_position)
        .def("get_current_support_foot_position",
             &DcmReactiveStepper::get_current_support_foot_position)
        .def("get_next_support_foot_position",
             &DcmReactiveStepper::get_next_support_foot_position)
        .def("get_step_duration", &DcmReactiveStepper::get_step_duration)
        .def("get_time_from_last_step_touchdown",
             &DcmReactiveStepper::get_time_from_last_step_touchdown)
        .def("get_flying_foot_position",
             &DcmReactiveStepper::get_flying_foot_position)
        // Setters
        .def("set_desired_com_velocity",
             &DcmReactiveStepper::set_desired_com_velocity);
}