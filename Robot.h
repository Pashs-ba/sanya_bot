#ifndef EVO_ROBOT_H
#define EVO_ROBOT_H
#include <vector>
#include "enums.h"


class Robot{
private:
    int mIndex = 0;
    void fix_direction();
    int size;
    
public:
	std::vector<int> commands;
    int mDirection = 4;
    int update();
    int mHealth;
    std::pair<int, int> mCoordinates;
    Robot(int commands_size, int health, std::pair<int, int> iCoordinates);
};

#endif //EVO_ROBOT_H
