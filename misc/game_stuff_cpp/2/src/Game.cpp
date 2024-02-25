#include "Game.h"
#include <iostream>


Game::Game()
{
    init();
}

void Game::init()
{
    m_playerConfig.SR = 32;
    m_playerConfig.CR = 32;
    m_playerConfig.FB = 5;
    m_playerConfig.FG = 5;
    m_playerConfig.FB = 5;
    m_playerConfig.OR = 5;
    m_playerConfig.OG = 255;
    m_playerConfig.OB = 0;
    m_playerConfig.OT = 0;
    m_playerConfig.V = 7;
    m_playerConfig.S = 8;

    m_enemyConfig.SR = 32;
    m_enemyConfig.CR = 32;
    m_enemyConfig.OR = 3;
    m_enemyConfig.OG = 3;
    m_enemyConfig.OB = 255;
    m_enemyConfig.OT = 255;
    m_enemyConfig.VMIN =2;
    m_enemyConfig.VMAX = 3;
    m_enemyConfig.SR = 32;
    m_enemyConfig.L = 8;
    m_enemyConfig.SI = 3;
    m_enemyConfig.SMIN = 60;
    m_enemyConfig.SMAX = 90;

    m_bulletConfig.SR = 32;
    m_bulletConfig.CR = 32;
    m_bulletConfig.FR = 32;
    m_bulletConfig.FG = 32;
    m_bulletConfig.FB = 32;
    m_bulletConfig.OR = 32;
    m_bulletConfig.OG = 32;
    m_bulletConfig.OB = 32;
    m_bulletConfig.OT = 32;
    m_bulletConfig.V = 32;
    m_bulletConfig.L = 32;
    m_bulletConfig.S = 32;

    m_window.create(sf::VideoMode(1280, 720), "Circles");
    m_window.setFramerateLimit(60);
    
    spawnPlayer();
}

void Game::run()
{
    while(m_running)
    {
        m_entities.update();

        sEnemySpawner();
        sMovement();
        sCollision();
        sUserInput();
        sRender();

        m_currentFrame++;

    }
}

void Game::setPause(bool paused)
{

}

void Game::spawnPlayer()
{
    auto entity = m_entities.addEntity("player");

    float center_x = m_window.getSize().x / 2.0f;
    float center_y = m_window.getSize().y / 2.0f;

    entity -> cTransform = std::make_shared<CTransform>(Vec2(center_x, center_y), Vec2(), 0.0f);
    entity -> cShape = std::make_shared<CShape>(m_playerConfig.SR, m_playerConfig.V, sf::Color(10,10,10), sf::Color(255, 0, 0), 4.0f);
    entity -> cInput = std::make_shared<CInput>();
     m_player = entity;
}

void Game::spawnEnemy()
{
    auto entity = m_entities.addEntity("enemy");

    float ex = rand() % m_window.getSize().x;
    float ey = rand() % m_window.getSize().y;

    entity -> cTransform = std::make_shared<CTransform>(Vec2(ex, ey), Vec2(), 0.0f);
    entity -> cShape = std::make_shared<CShape>(m_enemyConfig.SR, 5, sf::Color(0,0,255), sf::Color(255, 0, 0), 4.0f);

    m_lastEnemySpawnTime = m_currentFrame;
}

void Game::sRender()
{
    m_window.clear();

    for (auto e : m_entities.getEntities())
    {
        e->cShape->circle.setPosition(e->cTransform->pos.x, e->cTransform->pos.y);
        e->cTransform->angle += 1.0f;
        e->cShape->circle.setRotation(e->cTransform->angle);
        m_window.draw(e->cShape->circle);
    }

    m_window.display(); 
}

void Game::sMovement()
{
    if(m_player->cInput->up)
    {
        m_player->cTransform->velocity.y = -5;
    }
    else if(m_player->cInput->down)
    {
        m_player->cTransform->velocity.y = 5;
    }
    else
    {
        m_player->cTransform->velocity.y = 0;
    }

    if(m_player->cInput->left)
    {
        m_player->cTransform->velocity.x = -5;
    }
    else if(m_player->cInput->right)
    {
        m_player->cTransform->velocity.x = 5;
    }
    else
    {
        m_player->cTransform->velocity.x = 0;
    }

    m_player->cTransform->pos.x += m_player->cTransform->velocity.x;
    m_player->cTransform->pos.y += m_player->cTransform->velocity.y;

    for (auto bullet : m_entities.getEntities("bullet"))
    {
        bullet->cTransform->pos.x += bullet->cTransform->velocity.x;
        bullet->cTransform->pos.y += bullet->cTransform->velocity.y;
    }
}

void Game::sCollision()
{
    // for(auto bullet : m_entities.getEntities("bullet"))
    // {
    //     for(auto enemy : m_entities.getEntities("enemy"))
    //     {
    //         if(bullet->cTransform->pos)
    //     }
    // }
}

void Game::sUserInput()
{
    sf::Event event;
    while (m_window.pollEvent(event))
    {
        if (event.type == sf::Event::Closed)
        {
            m_running = false;
        }

        if (event.type == sf::Event::KeyPressed)
        {
            switch (event.key.code)
            {
            case sf::Keyboard::W:
                m_player->cInput->up = true;
                break;
            case sf::Keyboard::S:
                m_player->cInput->down = true;
                break;
            case sf::Keyboard::A:
                m_player->cInput->left = true;
                break;
            case sf::Keyboard::D:
                m_player->cInput->right = true;
                break;
            default:
                break;
            }
        }

        if (event.type == sf::Event::KeyReleased)
        {
            switch (event.key.code)
            {
            case sf::Keyboard::W:
                m_player->cInput->up = false;
                break;
            case sf::Keyboard::S:
                m_player->cInput->down = false;
                break;
            case sf::Keyboard::A:
                m_player->cInput->left = false;
                break;
            case sf::Keyboard::D:
                m_player->cInput->right = false;
                break;

            default:
                break;
            }
        }

        if(event.type == sf::Event::MouseButtonPressed)
        {
            if(event.mouseButton.button == sf::Mouse::Left)
            {
                spawnBullet(m_player, Vec2(event.mouseButton.x, event.mouseButton.y));
            }
        }

    }
    
}

void Game::sLifespan()
{

}

void Game::sEnemySpawner()
{   
    if (m_currentFrame - m_lastEnemySpawnTime > 120)
    {
        spawnEnemy();
    }
}

void Game::spawnBullet(std::shared_ptr<Entity> entity, const Vec2 & mouse_pos)
{
    auto bullet = m_entities.addEntity("bullet");
    Vec2 bullet_velocity = mouse_pos - entity->cTransform->pos;
    bullet->cTransform = std::make_shared<CTransform>(entity->cTransform->pos, bullet_velocity.norm()*7.0, 0);
    bullet->cShape = std::make_shared<CShape>(7, 9, sf::Color(255,0,255), sf::Color(255, 0, 0), 1.0f);

}