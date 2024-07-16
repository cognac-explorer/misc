#pragma once

#include <map>
#include "Animation.h"

class Assets
{
    std::map<std::string, sf::Texture> m_textures;
    std::map<std::string, Animation>   m_animations;
    std::map<std::string, sf::Font>    m_fonts;
public:
    Assets() {};
    void loadFromFile(std::string path);
    void addTexture(std::string & name, std::string & path);
    void addAnimation(std::string & name, Animation & animation);

    sf::Texture & getTexture(const std::string & name);
    const Animation & getAnimation(const std::string & name) const;
    // sf::Font getFont(std::string & name);
};