#version 330 core

in vec3 fragmentColor;

out vec4 color;

void main()
{
    //return pixel color
	color = vec4(fragmentColor,1.0);
}