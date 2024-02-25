#include <SFML/Graphics.hpp>
#include <iostream>

int width = 600;
int height = 400;

int main()
{
    sf::RenderWindow window(sf::VideoMode(width, height), "Bouncing shapes");
    window.setFramerateLimit(60);

    std::vector<sf::CircleShape> circles;
    std::vector<sf::Vector2f> speeds;

    sf::CircleShape circle1(10.f);
    circle1.setPosition(sf::Vector2f(100, 100));
    circle1.setFillColor(sf::Color::Green);
    circles.push_back(circle1);

    sf::CircleShape circle2(20.f);
    circle2.setPosition(sf::Vector2f(300, 200));
    circle2.setFillColor(sf::Color::Red);
    circles.push_back(circle2);

    sf::CircleShape circle3(15.f);
    circle3.setPosition(sf::Vector2f(200, 300));
    circle3.setFillColor(sf::Color::Blue);
    circles.push_back(circle3);

    speeds.push_back(sf::Vector2f(5.0f, 5.0f));
    speeds.push_back(sf::Vector2f(3.0f, -7.0f));
    speeds.push_back(sf::Vector2f(-4.0f, 4.0f));


    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))  // just for check several keys
        {
            if (event.type == sf::Event::Closed)
            {
                window.close();
            }
            if (event.type == sf::Event::KeyPressed)
            {
                std::cout << "Key code " << event.key.code << "\n";
            }
        }

        window.clear();
        
        for (size_t i=0; i<circles.size(); i++)
        {
            sf::CircleShape& shape = circles[i];
            sf::Vector2f& speed = speeds[i];

            if (shape.getPosition().x + 2 * shape.getRadius() >= width or shape.getPosition().x <= 0)
            {
                speed.x *= -1.0f;
            }
            if (shape.getPosition().y + 2 * shape.getRadius() >= height or shape.getPosition().y <= 0)
            {
                speed.y *= -1.0f;
            }
            
            shape.setPosition(shape.getPosition().x + speed.x, shape.getPosition().y + speed.y);
            shape.setRadius(shape.getRadius() + 0.01f);
        
            window.draw(shape);
        }

        window.display();
    }

    return 0;
}
