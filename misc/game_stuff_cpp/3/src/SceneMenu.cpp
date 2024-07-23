#include "SceneMenu.h"
#include "ScenePlay.h"
#include "Scene.h"
#include "GameEngine.h"
#include <SFML/Graphics.hpp>


SceneMenu::SceneMenu(GameEngine * gameEngine)
    : Scene(gameEngine)
{
    init();
}

void SceneMenu::init()
{
    m_title = "Menu";
    m_menuStrings = {"Level 1", "Level 2"};
    m_levelPaths = {"../bin/level.txt", "../bin/level2.txt"};
    m_menuText.setString("Help yourself");

    registerAction(sf::Keyboard::W,      "UP");
    registerAction(sf::Keyboard::S,      "DOWN");
    registerAction(sf::Keyboard::Space,  "OK");
}

void SceneMenu::update()
{
    sRender();
}

void SceneMenu::onEnd()
{

}

void SceneMenu::sDoAction(const Action & action)
{
    if (action.name() == "UP")         { m_selectedMenuIndex++; }
    else if (action.name() == "DOWN")  { m_selectedMenuIndex--; }
    else if (action.name() == "OK")    { m_game->changeScene("PLAY", std::make_shared<ScenePlay>(m_game, "../bin/level.txt")); }
}

void SceneMenu::sRender()
{
    m_game->window().clear();
    m_menuText.setString(m_title);
    m_menuText.setFont(m_game->getAssets().getFont("Main"));
    m_menuText.setPosition(100, 50);
    m_game->window().draw(m_menuText);

    for (size_t i = 0; i < m_menuStrings.size(); ++i)
    {
        m_menuText.setString(m_menuStrings[i]);
        m_menuText.setPosition(100, 150 + i * 50);
        
        // Highlight the selected menu item
        if (i == m_selectedMenuIndex) 
        {
            m_menuText.setFillColor(sf::Color::Red);
        }
        else 
        {
            m_menuText.setFillColor(sf::Color::White);
        }

        m_game->window().draw(m_menuText);
    }

    m_game->window().display();
}
