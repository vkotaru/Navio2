cmake_minimum_required(VERSION 2.8.3)
project(Navio2)

## Add support for C++11, supported in ROS Kinetic and newer
add_definitions(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
)


###################################
## catkin specific configuration ##
###################################
catkin_package(
 INCLUDE_DIRS include
 LIBRARIES Navio2
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########
## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(include
  ${catkin_INCLUDE_DIRS}
)

set(NAVIO_SRCS
	src/ADC_Navio2.cpp
	src/gpio.cpp
	src/I2Cdev.cpp
	src/Led_Navio2.cpp
	src/LSM9DS1.cpp
	src/MPU9250.cpp
	src/MS5611.cpp
	src/PWM.cpp
	src/RCInput_Navio2.cpp
	src/RCOutput_Navio2.cpp
	src/RGBled.cpp
	src/Ublox.cpp
	src/Util.cpp)

## Declare a C++ library
add_library(${PROJECT_NAME}
  ${NAVIO_SRCS}
)
target_include_directories(${PROJECT_NAME} PUBLIC . include)
target_link_libraries(qrotor_navio ${catkin_LIBRARIES})
add_dependencies(qrotor_navio ${catkin_EXPORTED_TARGETS})


#############
# end 