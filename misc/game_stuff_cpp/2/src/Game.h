#pragma once

#include "Entity.h"
#include "EntityManager.h"

#include "SFML/Graphics.hpp"

struct PlayerConfig {int shapeR, collisionR, fillCollorR, fillColorG, fillColorB, outlineColorR, outlineColorG, outlineColorB, outlineThickness, vertices; float speed;};
struct EnemyConfig {int shapeR, collisionR, outlineColorR, outlineColorG, outlineColorB, outlineThickness, verticesMin, verticesMax, smallEnemyLifespan, spawnInterval; float smallEnemySizeScale, speedMin, speedMax;};
struct BulletConfig {int shapeR, collisionR, fillCollorR, fillColorG, fillColorB, outlineColorR, outlineColorG, outlineColorB, outlineThickness, vertices, lifespan; float speed;};

class Game
{
    sf::RenderWindow m_window;
    EntityManager m_entities;
    sf::Font m_font;
    sf::Text m_text;
    PlayerConfig m_playerConfig;
    EnemyConfig m_enemyConfig;
    BulletConfig m_bulletConfig;
    int m_score = 0;
    int m_currentFrame = 0;
    int m_lastEnemySpawnTime = 0;
    int m_lastSpecial = 0;
    int m_specialInterval = 0;
    bool m_paused = false;
    bool m_running = true;
    std::shared_ptr<Entity> m_player;

    void init();
    void setPause(bool paused);

    void sMovement();
    void sUserInput();
    void sLifespan();
    void sRender();
    void sEnemySpawner();
    void sCollision();

    void spawnPlayer();
    void spawnEnemy();
    void spawnSmallEnemies(std::shared_ptr<Entity> entity);
    void spawnBullet(std::shared_ptr<Entity> entity, const Vec2 & mouse_pos);
    void spawnSpecialWeapon();

public:
    
    Game();
    void run();
};
