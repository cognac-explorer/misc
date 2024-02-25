#include "Vec2.h"
#include <iostream>
#include <cmath>


Vec2::Vec2() : x(0), y(0) {}
Vec2::Vec2(float xin, float yin):
  x(xin), y(yin) {}

bool Vec2::operator == (const Vec2 &rhs) const
{
    return (x == rhs.x) && (y == rhs.y);
}

bool Vec2::operator != (const Vec2 &rhs) const
{
    return (x != rhs.x) || (y != rhs.y);
}

Vec2 Vec2::operator + (const Vec2 &rhs) const
{
    return Vec2(x + rhs.x, y + rhs.y);
}

Vec2 Vec2::operator - (const Vec2 &rhs) const
{
    return Vec2(x - rhs.x, y - rhs.y);
}

Vec2 Vec2::operator * (const float val) const
{
    return Vec2(x*val, y*val);
}

Vec2 Vec2::operator / (const float val) const
{
    return Vec2(x/val, y/val);
}

void Vec2::operator += (const Vec2 &rhs)
{
    x += rhs.x;
    y += rhs.y;
}

void Vec2::operator -= (const Vec2 &rhs)
{
    x -= rhs.x;
    y -= rhs.y;
}

void Vec2::operator *= (const float val)
{
    x = x*val;
    y = y*val;
}

void Vec2::operator /= (const float val)
{
    x = x/val;
    y = y/val;
}

float Vec2::dist(const Vec2 & rhs) const
{
    return 0;
}

Vec2 Vec2::norm()
{
    float len = sqrt(x * x + y * y);
    return Vec2(x / len, y / len);
}

void Vec2::print() const
{
    std::cout << "Vec2 obj: x = " << this->x << "; y = " << this->y << std::endl;
}
