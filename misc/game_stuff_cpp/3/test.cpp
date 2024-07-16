#include "Assets.h"
#include <iostream>

int main()
{
    Assets assets;
    assets.loadFromFile("../bin/assets.txt");
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Texture Example");
    
    sf::Texture texture;

    std::string t = "TexBrick";
    texture = assets.getTexture(t);

    sf::Sprite sprite(texture);
    sprite.setScale(1.5, 0.4);
    sprite.setColor(sf::Color::Green);

    std::string t2 = "TexRun";
    sf::Texture texture2;
    texture2 = assets.getTexture(t2);

    Animation animation = Animation(t2, texture2, 5, 10);

    int frame = 1;
    int cf = 0;
    sf::Sprite s = animation.getSprite();
    s.setPosition(sf::Vector2f(100.0, 300.0));
    
    int top = 0;
    // Main loop
    while (window.isOpen()) {
        // Event handling
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Clear the window
        window.clear();

        // Draw the sprite


        if (frame % 2000 == 0)
        {
            cf ++;
            s.setTextureRect(sf::IntRect(cf * animation.getSize().x, top, animation.getSize().x, animation.getSize().y));
            
        }

        if(cf % 4 == 0)
        {
            cf = 0;
            
            
        }
        if(frame % 4 == 0)
        {
            top = animation.getSize().y;
        }
        if(frame % 8 == 0)
        {
            top = 0;
        }
        window.draw(sprite);
        window.draw(s);

        // Display the window contents
        window.display();

        frame ++;
    }
    return 0;
}
