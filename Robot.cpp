#include "Robot.h"

#include <utility>
#include <cstdlib>
#include <ctime>
#include <iostream>


void Robot::fix_direction(){
    if (mDirection > 4){
        mDirection = 1;
    }
    else if (mDirection < 1){
        mDirection = 4;
    }

}

int Robot::update(){
    mIndex++;
    if (mIndex >= commands.size() - 1 ){
        mIndex -= commands.size()-1;
    }
    if (!commands.empty()){
        switch (commands[mIndex])
        {
            case (1): // Left
                mDirection--;
                fix_direction();

                return Nothing;

            case (2): // Right
                mDirection++;
                fix_direction();

                return Nothing;

            case (3):
                return Go;

            case(4):
                return Eat;

            case(5):
                mIndex++;
                return Nothing;
            case(6):
                mIndex += 2;
                return Nothing;
            case(7):
                mIndex += 3;
                return Nothing;
            case(8):
                mIndex += 4;
                return Nothing;
            case(9):
                mIndex += 5;
                return Nothing;

        }
    }


    return Nothing;
}

Robot::Robot(int commands_size, int health, std::pair<int, int> iCoordinates):
    commands(commands_size),
    mCoordinates(std::move(iCoordinates))
{
    mHealth = health;
    size = commands_size;
//    srand (time(NULL));
    for(auto& i: commands){
		i = rand()%10;
    }
}

