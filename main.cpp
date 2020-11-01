#include "Robot.h"
#include "Field.h"
#include<ctime>
#include "iostream"
#include <SFML/Graphics.hpp>

int main()
{
	srand(time(NULL));
	Field field({ 20, 20 }, 40, 64, 70, 100, 8);

	sf::RenderWindow window(sf::VideoMode(field.size.first * 10 + 10, field.size.second * 10 + 10), "SFML window");

	sf::Time sleep_long = sf::seconds(1);
	sf::Time sleep_short = sf::seconds(0.1);

	///PRINT ROBOTS
	std::vector<sf::RectangleShape> GR_Robots(field.robots.size(), sf::RectangleShape(sf::Vector2f(10, 10)));
	for (int i = 0; i < field.robots.size(); i++) {
		GR_Robots[i].setPosition(sf::Vector2f(field.robots[i].mCoordinates.first * 10,
			field.robots[i].mCoordinates.second * 10));

	}
	///PRINT EAT
	std::vector<sf::RectangleShape> GR_Eat(field.eat.size(), sf::RectangleShape(sf::Vector2f(10, 10)));
	for (int i = 0; i < field.eat.size(); i++) {
		GR_Eat[i].setPosition(sf::Vector2f(field.eat[i].first * 10,
			field.eat[i].second * 10));

		GR_Eat[i].setFillColor(sf::Color::Red);
	}

	///MAIN LOOP
	int steps = 0;
	while (window.isOpen())
	{
		// Process events
		sf::Event event;
		while (window.pollEvent(event))
		{
			// Close window: exit
			if (event.type == sf::Event::Closed)
				window.close();
		}


		window.clear();
		for (auto& i : GR_Eat) {
			window.draw(i);
		}
		for (auto& i : GR_Robots) {
			window.draw(i);
		}

		window.display();

		if (field.robots.size() > field.minR) {
			field.step();
			steps++;
			GR_Robots = std::vector<sf::RectangleShape>(field.robots.size(), sf::RectangleShape(sf::Vector2f(10, 10)));
			for (int i = 0; i < field.robots.size(); i++) {

				GR_Robots[i].setPosition(sf::Vector2f(field.robots[i].mCoordinates.first * 10,
					field.robots[i].mCoordinates.second * 10));

			}
			GR_Eat = std::vector<sf::RectangleShape>(field.eat.size(), sf::RectangleShape(sf::Vector2f(10, 10)));
			for (int i = 0; i < field.eat.size(); i++) {
				GR_Eat[i].setPosition(sf::Vector2f(field.eat[i].first * 10,
					field.eat[i].second * 10));
				GR_Eat[i].setFillColor(sf::Color::Red);
			}
			sf::sleep(sleep_short);
		}
		else {
			std::cout << steps << std::endl;
			steps = 0;
			//sf::sleep(sleep_long);
			field.eat.clear();
			field.new_era();

		}

	}
	return 0;
}