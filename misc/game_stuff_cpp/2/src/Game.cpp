#include "Game.h"
#include <iostream>


Game::Game()
{
    init();
}

void Game::init()
{
    m_playerConfig.shapeR = 32;
    m_playerConfig.collisionR = 35;
    m_playerConfig.fillCollorR = 50;
    m_playerConfig.fillColorG = 50;
    m_playerConfig.fillColorB = 50;
    m_playerConfig.outlineColorR = 0;
    m_playerConfig.outlineColorG = 255;
    m_playerConfig.outlineColorB = 0;
    m_playerConfig.outlineThickness = 7;
    m_playerConfig.vertices = 7;
    m_playerConfig.speed = 8;

    m_enemyConfig.shapeR = 32;
    m_enemyConfig.collisionR = 35;
    m_enemyConfig.outlineColorR = 255;
    m_enemyConfig.outlineColorG = 0;
    m_enemyConfig.outlineColorB = 0;
    m_enemyConfig.outlineThickness = 7;
    m_enemyConfig.verticesMin = 3;
    m_enemyConfig.verticesMax = 8;
    m_enemyConfig.spawnInterval = 100;
    m_enemyConfig.smallEnemyLifespan = 40;
    m_enemyConfig.smallEnemySizeScale = 2.5;
    m_enemyConfig.speedMin = 1;
    m_enemyConfig.speedMax = 5;

    m_bulletConfig.shapeR = 8;
    m_bulletConfig.collisionR = 7;
    m_bulletConfig.fillCollorR = 255;
    m_bulletConfig.fillColorG = 0;
    m_bulletConfig.fillColorB = 0;
    m_bulletConfig.outlineColorR = 255;
    m_bulletConfig.outlineColorG = 50;
    m_bulletConfig.outlineColorB = 0;
    m_bulletConfig.outlineThickness = 1;
    m_bulletConfig.vertices = 16;
    m_bulletConfig.lifespan = 70;
    m_bulletConfig.speed = 16;

    m_specialInterval = 500;

    m_window.create(sf::VideoMode(1280, 720), "Circles");
    m_window.setFramerateLimit(60);

    spawnPlayer();
}

void Game::run()
{
    while(m_running)
    {
        m_entities.update();
        std::cout<<m_entities.len()<<std::endl;
        sEnemySpawner();
        sMovement();
        sCollision();
        sUserInput();
        sRender();
        sLifespan();

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

    entity->cTransform = std::make_shared<CTransform>(Vec2(center_x, center_y), Vec2(), 0.0f);
    entity->cShape     = std::make_shared<CShape>(m_playerConfig.shapeR, m_playerConfig.vertices, sf::Color(m_playerConfig.fillCollorR, m_playerConfig.fillColorG, m_playerConfig.fillColorB), sf::Color(m_playerConfig.outlineColorR, m_playerConfig.outlineColorG, m_playerConfig.outlineColorB), m_playerConfig.outlineThickness);
    entity->cInput     = std::make_shared<CInput>();
    entity->cCollision = std::make_shared<CCollision>(m_playerConfig.collisionR);
    m_player = entity;
}

void Game::spawnEnemy()
{
    auto entity = m_entities.addEntity("enemy");

    float ex = rand() % m_window.getSize().x;
    float ey = rand() % m_window.getSize().y;

    float vertices =  m_enemyConfig.verticesMin + rand() % (m_enemyConfig.verticesMax - m_enemyConfig.verticesMin + 1);

    float fillColorR = rand() % 255;
    float fillColorG = rand() % 255;
    float fillColorB = rand() % 255;

    Vec2 randomVelocity = Vec2(rand() % 100 - 50, rand() % 100 - 50);
    randomVelocity.norm();
    randomVelocity.scale(m_enemyConfig.speedMin, m_enemyConfig.speedMax);

    entity->cTransform = std::make_shared<CTransform>(Vec2(ex, ey), randomVelocity, 0.0f);
    entity->cShape     = std::make_shared<CShape>(m_enemyConfig.shapeR, vertices, sf::Color(fillColorR, fillColorG, fillColorB), sf::Color(m_enemyConfig.outlineColorR, m_enemyConfig.outlineColorG, m_enemyConfig.outlineColorB), m_enemyConfig.outlineThickness);
    entity->cCollision = std::make_shared<CCollision>(m_enemyConfig.collisionR);
    m_lastEnemySpawnTime = m_currentFrame;
}

void Game::spawnSmallEnemies(std::shared_ptr<Entity> e)
{
    int enemy_verts = e->cShape->circle.getPointCount();
    int shapeRadius = static_cast<int>(e->cShape->circle.getRadius() / m_enemyConfig.smallEnemySizeScale);
    Vec2 position = e->cTransform->pos;
    Vec2 velocity = e->cTransform->velocity;
    float angle = 360 / enemy_verts;

    for (int i = 0; i < enemy_verts; i++)
    {
        auto entity = m_entities.addEntity("smallenemy");
        Vec2 newVelocity = velocity.rotate(i * angle);
        entity->cTransform = std::make_shared<CTransform>(position, newVelocity, 0.0f);
        entity->cShape     = std::make_shared<CShape>(shapeRadius, enemy_verts, e->cShape->circle.getFillColor(), e->cShape->circle.getOutlineColor(), 1.0f);
        entity->cCollision = std::make_shared<CCollision>(shapeRadius);
        entity->cLifespan  = std::make_shared<CLifespan>(m_enemyConfig.smallEnemyLifespan);
    }
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
    
    sf::Font font;
    // font.loadFromFile("/usr/share/fonts/truetype/freefont/FreeMono.ttf");
    font.loadFromFile("arial.ttf");
    m_text.setFont(font);
    m_text.setCharacterSize(24);
    m_text.setFillColor(sf::Color::Red);
    m_text.setPosition(10.f, 10.f);
    std::string displayText = "Score: " + std::to_string(m_score);
    if(m_currentFrame - m_lastSpecial > m_specialInterval)
    {
        displayText += " Special weapon!";
    }
    m_text.setString(displayText);
    m_window.draw(m_text);
    m_window.display(); 
}

void Game::sMovement()
{
    if(m_player->cInput->up)
    {
        m_player->cTransform->velocity.y = -m_playerConfig.speed;
        if(m_player->cTransform->pos.y - m_player->cShape->circle.getRadius() <= 0)
        {
            m_player->cTransform->velocity.y = 0;
        }
    }
    else if(m_player->cInput->down)
    {
        m_player->cTransform->velocity.y = m_playerConfig.speed;
        if(m_player->cTransform->pos.y + m_player->cShape->circle.getRadius() >= m_window.getSize().y)
        {
            m_player->cTransform->velocity.y = 0;
        }
    }
    else
    {
        m_player->cTransform->velocity.y = 0;
    }

    if(m_player->cInput->left)
    {
        m_player->cTransform->velocity.x = -m_playerConfig.speed;
        if(m_player->cTransform->pos.x - m_player->cShape->circle.getRadius() <= 0)
        {
            m_player->cTransform->velocity.x = 0;
        }
    }
    else if(m_player->cInput->right)
    {
        m_player->cTransform->velocity.x = m_playerConfig.speed;
        if(m_player->cTransform->pos.x + m_player->cShape->circle.getRadius() >= m_window.getSize().x)
        {
            m_player->cTransform->velocity.x = 0;
        }
    }
    else
    {
        m_player->cTransform->velocity.x = 0;
    }

    for (auto e : m_entities.getEntities("enemy"))
    {
        if(e->cTransform->pos.x <= 0 or e->cTransform->pos.x >= m_window.getSize().x)
        {
            e->cTransform->velocity.x *= -1;
        }
        if(e->cTransform->pos.y <= 0 or e->cTransform->pos.y >= m_window.getSize().y)
        {
            e->cTransform->velocity.y *= -1;
        }
    }

    for (auto e : m_entities.getEntities())
    {
        e->cTransform->pos.x += e->cTransform->velocity.x;
        e->cTransform->pos.y += e->cTransform->velocity.y;
    }
}

void Game::sCollision()
{
    for(auto bullet : m_entities.getEntities("bullet"))
    {
        for(auto enemy : m_entities.getEntities("enemy"))
        {
            Vec2 dist = bullet->cTransform->pos - enemy->cTransform->pos;
            if(dist.len() < bullet->cCollision->radius + enemy->cCollision->radius)
            {
                enemy->destroy();
                bullet->destroy();
                spawnSmallEnemies(enemy);
                m_score += 1;
            }
        }
    }

    for(auto enemy : m_entities.getEntities("enemy"))
    {
        Vec2 dist = m_player->cTransform->pos - enemy->cTransform->pos;
        if(dist.len() < enemy->cCollision->radius + enemy->cCollision->radius)
        {
            m_player->destroy();
            spawnPlayer();
            m_score = 0;
        }
    }

    for(auto enemy : m_entities.getEntities("smallenemy"))
    {
        Vec2 dist = m_player->cTransform->pos - enemy->cTransform->pos;
        if(dist.len() < enemy->cCollision->radius + enemy->cCollision->radius)
        {
            m_player->destroy();
            spawnPlayer();
        }
    }

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
            if(event.mouseButton.button == sf::Mouse::Right)
            {
                if(m_currentFrame - m_lastSpecial > m_specialInterval)
                {
                    spawnSpecialWeapon();
                    m_lastSpecial = m_currentFrame;
                }
            }
        }

    }
    
}

void Game::sLifespan()
{
    for(auto e : m_entities.getEntities("smallenemy"))
    {
        e->cLifespan->remaining -= 1;
        sf::Color fill_color = e->cShape->circle.getFillColor();
        sf::Color border_color = e->cShape->circle.getFillColor();
        float coeff = static_cast<float>(e->cLifespan->total - e->cLifespan->remaining) / e->cLifespan->total;
        int alpha = static_cast<int>(255.0f * (1 - coeff));

        e->cShape->circle.setFillColor(sf::Color(fill_color.r, fill_color.g, fill_color.b, alpha));
        e->cShape->circle.setOutlineColor(sf::Color(border_color.r, border_color.g, border_color.b, alpha));
        if(e->cLifespan->remaining == 0)
        {
            e->destroy();
        }
    }
    for(auto e : m_entities.getEntities("bullet"))
    {
        e->cLifespan->remaining -= 1;
        sf::Color fill_color = e->cShape->circle.getFillColor();
        sf::Color border_color = e->cShape->circle.getFillColor();
        float coeff = static_cast<float>(e->cLifespan->total - e->cLifespan->remaining) / e->cLifespan->total;
        int alpha = static_cast<int>(255.0f * (1 - coeff));

        e->cShape->circle.setFillColor(sf::Color(fill_color.r, fill_color.g, fill_color.b, alpha));
        e->cShape->circle.setOutlineColor(sf::Color(border_color.r, border_color.g, border_color.b, alpha));
        if(e->cLifespan->remaining == 0)
        {
            e->destroy();
        }
    }
}

void Game::sEnemySpawner()
{ 
    if (m_currentFrame - m_lastEnemySpawnTime > m_enemyConfig.spawnInterval)
    {
        spawnEnemy();
    }
}

void Game::spawnBullet(std::shared_ptr<Entity> entity, const Vec2 & mouse_pos)
{
    auto bullet = m_entities.addEntity("bullet");
    Vec2 bullet_velocity = mouse_pos - entity->cTransform->pos;
    bullet_velocity.norm();

    bullet->cTransform = std::make_shared<CTransform>(entity->cTransform->pos, bullet_velocity * m_bulletConfig.speed, 0);
    bullet->cShape     = std::make_shared<CShape>(m_bulletConfig.shapeR, m_bulletConfig.vertices, sf::Color(m_bulletConfig.fillCollorR, m_bulletConfig.fillColorG, m_bulletConfig.fillColorB), sf::Color(m_bulletConfig.outlineColorR, m_bulletConfig.outlineColorG, m_bulletConfig.outlineColorB), m_bulletConfig.outlineThickness);
    bullet->cCollision = std::make_shared<CCollision>(m_bulletConfig.collisionR);
    bullet->cLifespan  = std::make_shared<CLifespan>(m_bulletConfig.lifespan);
}

void Game::spawnSpecialWeapon()
{
    Vec2 position = m_player->cTransform->pos;
    int bullet_num = 24;
    int angle = 360 / bullet_num;
    Vec2 velocity = Vec2(10.0, 10.0);
    for (int i = 0; i < bullet_num; i++)
    {
        auto entity = m_entities.addEntity("bullet");
        Vec2 newVelocity = velocity.rotate(i * angle);
        entity->cTransform = std::make_shared<CTransform>(position, newVelocity, 0.0f);
        entity->cShape     = std::make_shared<CShape>(m_bulletConfig.shapeR, m_bulletConfig.vertices, sf::Color::Red, sf::Color::Red, 1.0f);
        entity->cCollision = std::make_shared<CCollision>(m_bulletConfig.collisionR);
        entity->cLifespan  = std::make_shared<CLifespan>(m_bulletConfig.lifespan + 20);
    }
}
