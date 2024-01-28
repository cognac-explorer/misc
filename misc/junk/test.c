#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdio.h>
#include <math.h>

const double PI = 3.141592653589793;

void drawCircle(float centerX, float centerY, float radius, int segments) {
    glBegin(GL_TRIANGLE_FAN);
    glVertex2f(centerX, centerY);

    for (int i = 0; i <= segments; i++) {
        float theta = (float)(2.0 * PI * i / segments);
        float x = centerX + radius * cos(theta);
        float y = centerY + radius * sin(theta);
        glVertex2f(x, y);
    }

    glEnd();
}

void render(GLFWwindow* window) {
    glClear(GL_COLOR_BUFFER_BIT);

    // Draw a circle at the center of the window
    drawCircle(0.0f, 0.0f, 0.4f, 10);

    glfwSwapBuffers(window);
    glfwPollEvents();
}

int main() {
    if (!glfwInit()) {
        fprintf(stderr, "Failed to initialize GLFW\n");
        return -1;
    }

    GLFWwindow* window = glfwCreateWindow(800, 800, "Circle Drawing", NULL, NULL);
    if (!window) {
        fprintf(stderr, "Failed to create GLFW window\n");
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);

    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Failed to initialize GLEW\n");
        return -1;
    }

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);

    while (!glfwWindowShouldClose(window)) {
        render(window);
    }

    glfwTerminate();
    return 0;
}
