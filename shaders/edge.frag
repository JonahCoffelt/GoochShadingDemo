#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;
uniform sampler2D depthTexture;
uniform vec2 textureSize;

void main()
{ 
    vec2 offset = 1.0 / textureSize;  

    // List of offsets used for sampling the texture
    vec2 offsets[9] = vec2[](
        vec2(-1.0, -1.0) * offset,
        vec2(-1.0,  0.0) * offset,
        vec2(-1.0,  1.0) * offset,
        vec2( 0.0, -1.0) * offset,
        vec2( 0.0,  0.0) * offset,
        vec2( 0.0,  1.0) * offset,
        vec2( 1.0, -1.0) * offset,
        vec2( 1.0,  0.0) * offset,
        vec2( 1.0,  1.0) * offset 
    );

    float kernel[9] = float[](
        1, 1, 1,
        1,-8, 1,
        1, 1, 1
    );

    float total = 0.0;
    for (int i = 0; i < 9; i++)
    {
       total += texture(depthTexture, uv + offsets[i]).r * kernel[i];
    }

    float threshold = 0.05;
    if (total > threshold) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
    else {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
}