#include <SFML/Graphics.hpp>
#include <string>

class Vec2 {
public:
    float x, y;
    Vec2(float x = 1, float y = 1) : x(x), y(y) {}
};

class Animation {
    sf::Sprite m_sprite;
    size_t m_frameCount = 1;
    size_t m_currentFrame = 0;
    size_t m_speed;
    Vec2 m_size = {1, 1};
    std::string m_name = "none";
    size_t m_elapsedFrames = 0;

public:
    Animation() {}
    Animation(const std::string &name, const sf::Texture &t)
        : m_name(name), m_sprite(t), m_frameCount(1), m_speed(1), m_size(t.getSize().x, t.getSize().y) {
        m_sprite.setTexture(t);
        m_sprite.setTextureRect(sf::IntRect(0, 0, m_size.x, m_size.y));
    }

    Animation(const std::string &name, const sf::Texture &t, size_t frameCount, size_t speed)
        : m_name(name), m_sprite(t), m_frameCount(frameCount), m_speed(speed) {
        m_size = Vec2(t.getSize().x / frameCount, t.getSize().y);
        m_sprite.setTexture(t);
        m_sprite.setTextureRect(sf::IntRect(0, 0, m_size.x, m_size.y));
    }

    void update() {
        if (m_frameCount <= 1) return;

        m_elapsedFrames++;
        if (m_elapsedFrames >= m_speed) {
            m_elapsedFrames = 0;
            m_currentFrame = (m_currentFrame + 1) % m_frameCount;
            size_t frame = m_currentFrame;
            m_sprite.setTextureRect(sf::IntRect(frame * m_size.x, 0, m_size.x, m_size.y));
        }
    }

    bool hasEnded() const {
        return m_currentFrame >= m_frameCount - 1;
    }

    const std::string &getName() const {
        return m_name;
    }

    const Vec2 &getSize() const {
        return m_size;
    }

    sf::Sprite &getSprite() {
        return m_sprite;
    }
};

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Animation");

    sf::Texture texture;
    if (!texture.loadFromFile("bin/images/brick.png")) {
        return -1; // Handle error
    }

    Animation animation("walk", texture, 4, 10); // 4 frames, update every 10 ticks

    sf::Clock clock;
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        if (clock.getElapsedTime().asMilliseconds() > 100) { // Update animation every 100 ms
            animation.update();
            clock.restart();
        }

        window.clear();
        window.draw(animation.getSprite());
        window.display();
    }

    return 0;
}
