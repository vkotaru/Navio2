/*
    ROS node to publish imu raw data
*/


// system 
#include <ros/ros.h>
#include <sys/time.h>

#include "Common/MPU9250.h"
#include "Navio2/LSM9DS1.h"
#include "Common/Util.h"
#include <unistd.h>
#include <string>
#include <memory>

float FREQ = 500;

std::unique_ptr <InertialSensor> get_inertial_sensor( std::string sensor_name)
{
    if (sensor_name == "mpu") {
        printf("Selected: MPU9250\n");
        auto ptr = std::unique_ptr <InertialSensor>{ new MPU9250() };
        return ptr;
    }
    else if (sensor_name == "lsm") {
        printf("Selected: LSM9DS1\n");
        auto ptr = std::unique_ptr <InertialSensor>{ new LSM9DS1() };
        return ptr;
    }
    else {
        return NULL;
    }
}

void print_help()
{
    printf("Possible parameters:\nSensor selection: -i [sensor name]\n");
    printf("Sensors names: mpu is MPU9250, lsm is LSM9DS1\nFor help: -h\n");
}

std::string get_sensor_name(int argc, char *argv[])
{
    if (get_navio_version() == NAVIO2) {

        if (argc < 2) {
            printf("Enter parameter\n");
            print_help();
            return std::string();
        }

        // prevent the error message
        opterr = 0;
        int parameter;

        while ((parameter = getopt(argc, argv, "i:h")) != -1) {
            switch (parameter) {
            case 'i': return optarg;
            case 'h': print_help(); return "-1";
            case '?': printf("Wrong parameter.\n");
                      print_help();
                      return std::string();
            }
        }

    } else { //sensor on NAVIO+

        return "mpu";
    }

}
//=============================================================================

int main(int argc, char *argv[])
{

    if (check_apm()) {
        return 1;
    }

    MPU9250 sensor; 

    if (!sensor.probe()) {
        printf("Sensor not enabled\n");
        return EXIT_FAILURE;
    }

    sensor.initialize();

    float ax, ay, az;
    float gx, gy, gz;
    float mx, my, mz;

    ros::Rate run_ros_loop_at(FREQ);
    while(ros::ok()) {

        ros::spinOnce();
        /***************/

        sensor.update();
        sensor.read_accelerometer(&ax, &ay, &az);
        sensor.read_gyroscope(&gx, &gy, &gz);
        sensor.read_magnetometer(&mx, &my, &mz);
        printf("Acc: %+7.3f %+7.3f %+7.3f  ", ax, ay, az);
        printf("Gyr: %+8.3f %+8.3f %+8.3f  ", gx, gy, gz);
        printf("Mag: %+7.3f %+7.3f %+7.3f\n", mx, my, mz);



        /***************/
        run_ros_loop_at.sleep();
    }
    ros::shutdown();
    return 0;
}
