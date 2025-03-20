#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv;
uniform sampler2D goochTexture;
uniform sampler2D outlineTexture;


void main()
{ 
    vec4 color = texture(goochTexture, uv);

    vec3 outline_1 = texture(outlineTexture, uv).rgb;
    vec3 outline_2 = texture(outlineTexture, uv + vec2(0.01, 0)).rgb;
    vec3 outline_3 = texture(outlineTexture, uv + vec2(0, 0.01)).rgb;

    outline_2 *= clamp(sin(uv.y * 50) * sin(uv.x * 20) - 0.1, 0.0, 1.0);
    outline_3 *= clamp(cos(uv.y * 30) * sin(uv.x * 40) - 0.3, 0.0, 1.0);

    color.rgb -= outline_1 + (outline_2 + outline_3) * .25;
    fragColor = color;
}