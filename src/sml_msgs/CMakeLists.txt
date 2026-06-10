cmake_minimum_required(VERSION 3.8)
project(sml_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Order.msg"
  "msg/Station.msg"
  "msg/Task.msg"
  "msg/Step.msg"
  "srv/GetPlan.srv"
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
