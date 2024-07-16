#include "ScenePlay.h"
#include "Physics.h"
#include "Assets.h"
#include "GameEngine.h"
#include "Components.h"
#include "Action.h"

#include <fstream>
#include <sstream>
#include <iostream>

ScenePlay::ScenePlay(GameEngine * gameEngine, const std::string & levelPath)
    : Scene(gameEngine)
    , m_levelPath(levelPath)
{
    init(m_levelPath);
}


void ScenePlay::init(const std::string & levelPath)
{
    registerAction(sf::Keyboard::P,      "PAUSE");
    registerAction(sf::Keyboard::Escape, "QUIT");
    registerAction(sf::Keyboard::T,      "TOGGLE_TEXTURE");
    registerAction(sf::Keyboard::C,      "TOGGLE_COLLISION");
    registerAction(sf::Keyboard::G,      "TOGGLE_GRID");
    registerAction(sf::Keyboard::A,      "LEFT");
    registerAction(sf::Keyboard::D,      "RIGHT");
    registerAction(sf::Keyboard::W,      "JUMP");

    m_gridText.setCharacterSize(12);
    // m_gridText.setFont(m_game->getAssets().getFont("Tech"));
    
    loadLevel(levelPath);
}

void ScenePlay::spawnPlayer()
{
    // read player config from file
    std::ifstream inputFile("../bin/player.txt");
    if (!inputFile)
    {
        std::cerr << "Error opening file player.txt" << std::endl;
    }

    std::string line;
    if (std::getline(inputFile, line))  // skip first line
    {
        while (std::getline(inputFile, line))
        {
            std::istringstream iss(line);
            int X, Y, CX, CY, speed, speedJump, speedMax;
            float gravity;
            std::string bulletAnimation;
            iss >> X >> Y >> CX >> CY >> speed >> speedJump >> speedMax >> gravity;
            m_playerConfig.X = X;
            m_playerConfig.Y = Y;
            m_playerConfig.CX = CX;
            m_playerConfig.CY = CY;
            m_playerConfig.SPEED = speed;
            m_playerConfig.JUMPSPEED = speedJump;
            m_playerConfig.MAXSPEED = speedMax;
            m_playerConfig.GRAVITY = gravity;
            m_playerConfig.WEAPON = bulletAnimation;
        }
    }

    m_player = m_entityManager.addEntity("player");
    Animation animationPlayer = m_game->getAssets().getAnimation("Run");
    m_player->addComponent<CAnimation>(animationPlayer, true);
    m_player->addComponent<CTransform>(Vec2(m_playerConfig.X , m_playerConfig.Y));   
    m_player->addComponent<CBoundingBox>(Vec2(m_playerConfig.CX , m_playerConfig.CY));
    m_player->addComponent<CState>("run");
    m_player->addComponent<CGravity>(m_playerConfig.GRAVITY);

}

Vec2 ScenePlay::gridToMidPixel(float gridX, float gridY, std::shared_ptr<Entity> entity)
{
    Vec2 size = entity->getComponent<CAnimation>().animation.getSize();
    return Vec2(gridX*m_gridSize.x + size.x / 2, m_game->window().getSize().y - gridY*m_gridSize.y - size.y / 2);
}

void ScenePlay::loadLevel(const std::string & fileName)
{
    spawnPlayer();

    std::ifstream inputFile(fileName);
    if (!inputFile)
    {
        std::cerr << "Error opening file " << fileName << std::endl;
    }

    std::string line;
    while (std::getline(inputFile, line))
    {
        std::istringstream iss(line);
        std::string entityType;
        iss >> entityType;
        if (entityType == "Tile")
        {
            std::string tileName; 
            int gridX, gridY;
            iss >> tileName >> gridX >> gridY;
            auto brick = m_entityManager.addEntity("tile");
            Animation animationTile = m_game->getAssets().getAnimation(tileName);
            brick->addComponent<CAnimation>(animationTile, false);
            brick->addComponent<CBoundingBox>(animationTile.getSize());
            brick->addComponent<CTransform>(gridToMidPixel(gridX, gridY, brick));
        }
        if (entityType == "Dec")
        {
            std::string tileName; 
            int gridX, gridY;
            iss >> tileName >> gridX >> gridY;
            auto brick = m_entityManager.addEntity("dec");
            Animation animationTile = m_game->getAssets().getAnimation(tileName);
            brick->addComponent<CAnimation>(animationTile, false);
            brick->addComponent<CTransform>(gridToMidPixel(gridX, gridY, brick));
        }
    }
    
    inputFile.close();
}

void ScenePlay::spawnBullet(std::shared_ptr<Entity> entity)
{

}

void ScenePlay::sMovement()
{
    Vec2 & playerVelocity = m_player->getComponent<CTransform>().velocity;
    if (m_player->getComponent<CInput>().right)
    {
        m_player->getComponent<CAnimation>().animation.getSprite().setScale(1, 1);
        // m_player->addComponent<CState>().state = "running";
        playerVelocity.x = m_playerConfig.SPEED;
    }
    else if (m_player->getComponent<CInput>().left)
    {
        m_player->getComponent<CAnimation>().animation.getSprite().setScale(-1, 1);
        // m_player->addComponent<CState>().state = "running";
        playerVelocity.x = -m_playerConfig.SPEED;
    }
    else
    {
        // m_player->addComponent<CState>().state = "standing";
        playerVelocity.x = 0;
    }
    if (m_player->getComponent<CInput>().up)
    {
        // m_player->addComponent<CState>().state = "jumping";
        playerVelocity.y = -m_playerConfig.JUMPSPEED;
        // m_player->getComponent<CInput>().canJump = false;
    }

    // don't allow player velocity to exceed max velocity
    if (playerVelocity.x > m_playerConfig.MAXSPEED)
    {
        playerVelocity.x = m_playerConfig.MAXSPEED;
    }
    else if (playerVelocity.x < -m_playerConfig.MAXSPEED)
    {
        playerVelocity.x = -m_playerConfig.MAXSPEED;
    }
    if (playerVelocity.y < -m_playerConfig.MAXSPEED)
    {
        playerVelocity.y = -m_playerConfig.MAXSPEED;
    }
    else if (playerVelocity.y < -m_playerConfig.MAXSPEED)
    {
        playerVelocity.y = -m_playerConfig.MAXSPEED;
    }

    for (auto e : m_entityManager.getEntities())
    {
        e->getComponent<CTransform>().prevPos = e->getComponent<CTransform>().pos;
        Vec2 & velocity = e->getComponent<CTransform>().velocity;
        if (e->hasComponent<CGravity>())
        {
            velocity.y += e->getComponent<CGravity>().gravity;
        }
        e->getComponent<CTransform>().pos += velocity;
    }
}

void ScenePlay::sRender()
{
    
    if (!m_paused)
    {
        m_game->window().clear(sf::Color(100, 100, 255));
    }
    else
    {
        m_game->window().clear(sf::Color(50, 50, 150));
    }

    auto & pPos = m_player->getComponent<CTransform>().pos;
    float windowCenterX = std::max(m_game->window().getSize().x / 2.0f, pPos.x);
    sf::View view = m_game->window().getView();
    view.setCenter(windowCenterX, m_game->window().getSize().y - view.getCenter().y);
    m_game->window().setView(view);

    if (m_drawTextures)
    {
        
        for (auto e : m_entityManager.getEntities())
        {
            auto & transform = e->getComponent<CTransform>();

            if (e->hasComponent<CAnimation>())
            {
                
                auto & animation = e->getComponent<CAnimation>().animation;
                animation.getSprite().setRotation(transform.angle);
                animation.getSprite().setPosition(transform.pos.x, transform.pos.y);
                m_game->window().draw(animation.getSprite());
            }
        }
        m_game->window().display();
    }

    // if (m_drawCollision)
    // {

    // }

    // if (m_drawGrid)
    // {

    // }
}

void ScenePlay::sAnimation()
{
    if (m_player->getComponent<CState>().state == "standing")
    {
        m_player->addComponent<CAnimation>(m_game->getAssets().getAnimation("Stand"), true);
    }
    else if (m_player->getComponent<CState>().state == "running")
    {
        m_player->addComponent<CAnimation>(m_game->getAssets().getAnimation("Run"), true);
    }
    else if (m_player->getComponent<CState>().state == "jumping")
    {
        m_player->addComponent<CAnimation>(m_game->getAssets().getAnimation("Jump"), true);
    }

    for (auto e : m_entityManager.getEntities())
    {
        
        if (e->hasComponent<CAnimation>())
        {
            Animation & entityAnimation = e->getComponent<CAnimation>().animation;
            entityAnimation.update();
            if (entityAnimation.hasEnded() && !e->getComponent<CAnimation>().repeat)
            {
                e->destroy();
            }
        }
    }

}

void ScenePlay::sLifespan()
{

}

void ScenePlay::sCollision()
{
    Physics ph;

    for (auto tile : m_entityManager.getEntities("tile"))
    {
        Vec2 overlap = ph.GetOverlap(m_player, tile);
        Vec2 prevOverlap = ph.GetPreviousOverlap(m_player, tile);
        
        if (overlap.x > 0 && overlap.y > 0)
        {
            if (prevOverlap.x > 0 && m_player->getComponent<CTransform>().pos.y < tile->getComponent<CTransform>().pos.y)
            {
                m_player->getComponent<CTransform>().pos.y -= overlap.y;
                m_player->getComponent<CTransform>().velocity.y = 0;
            }
            if (prevOverlap.x > 0 && m_player->getComponent<CTransform>().pos.y > tile->getComponent<CTransform>().pos.y)
            {
                m_player->getComponent<CTransform>().pos.y += overlap.y;
                m_player->getComponent<CTransform>().velocity.y = 0;
            }
            if (prevOverlap.y > 0 && m_player->getComponent<CTransform>().pos.x < tile->getComponent<CTransform>().pos.x)
            {
                m_player->getComponent<CTransform>().pos.x -= overlap.x;
            }
            if (prevOverlap.y > 0 && m_player->getComponent<CTransform>().pos.x > tile->getComponent<CTransform>().pos.x)
            {
                m_player->getComponent<CTransform>().pos.x += overlap.x;
            }
        }
    }
}

void ScenePlay::sDoAction(const Action & action)
{
    if (action.type() == "START")
    {
             if (action.name() == "TOGGLE_TEXTURE")    { m_drawTextures = !m_drawTextures; }
        else if (action.name() == "TOGGLE_COLLISION")  { m_drawCollision != m_drawCollision; }
        else if (action.name() == "TOGGLE_GRID")       { m_drawGrid != m_drawGrid; }
        else if (action.name() == "PAUSE" )            { setPaused(!m_paused); }
        else if (action.name() == "QUIT")              { onEnd(); }
        else if (action.name() == "RIGHT")
        {
            m_player->getComponent<CInput>().right = true;
        }
        else if (action.name() == "LEFT")
        {
            m_player->getComponent<CInput>().left = true;
        }
        else if (action.name() == "JUMP")
        {
            m_player->getComponent<CInput>().up = true;
            m_player->getComponent<CInput>().canJump = false;
        }
    }
    else if (action.type() == "END")
    {
        if (action.name() == "RIGHT")
        {
            m_player->getComponent<CInput>().right = false;
        }
        else if (action.name() == "LEFT")
        {
            m_player->getComponent<CInput>().left = false;
        }
        else if (action.name() == "JUMP")
        {
            m_player->getComponent<CInput>().up = false;
            m_player->getComponent<CInput>().canJump = true;
        }
    }
}

void ScenePlay::onEnd()
{
    m_game -> quit();
}

void ScenePlay::update()
{
    m_entityManager.update();

    // TODO paused

    sMovement();
    // sLifespan();
    sCollision();
    sAnimation();
    sRender();
}
