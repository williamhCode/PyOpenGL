#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec3 vertexColor;

uniform mat4 model;
uniform mat4 projView;

out vec3 fragmentColor;

void main()
{
    gl_Position = projView * model * vec4(vertexPos, 1.0);
    fragmentColor = vertexColor;
}