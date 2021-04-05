def VertexShader() -> str:
    return \
"#version 330 core\n\
layout(location = 0) in vec3 a_Position;\n\
layout(location = 1) in vec4 a_Color;\n\
layout(location = 2) in vec2 a_TexCoord;\n\
layout(location = 3) in float a_TexIndex;\n\
\n\
uniform mat4 u_ViewProj;\n\
uniform mat4 u_Transform;\n\
\n\
out vec4 v_Color;\n\
out vec2 v_TexCoord;\n\
out float v_TexIndex;\n\
\n\
void main()\n\
{\n\
	v_Color = a_Color;\n\
	v_TexCoord = a_TexCoord;\n\
	v_TexIndex = a_TexIndex;\n\
	gl_Position = u_ViewProj * u_Transform * vec4(a_Position, 1.0);\n\
}"

def FragmentShader(MaxTexturesSlots=8) -> str:
    return \
"#version 330 core\n\
#define MAX_TEXTURES_SLOTS "+ str(MaxTexturesSlots) +"\n\
\n\
layout(location = 0) out vec4 o_Color;\n\
\n\
in vec4 v_Color;\n\
in vec2 v_TexCoord;\n\
in float v_TexIndex;\n\
\n\
uniform sampler2D u_Textures[MAX_TEXTURES_SLOTS];\n\
\n\
void main()\n\
{\n\
	int index = int(v_TexIndex);\n\
    o_Color = texture(u_Textures[index], v_TexCoord) * v_Color;\n\
}"

def VertexShaderText() -> str:
    return \
"#version 330 core\n\
layout(location = 0) in vec3 a_Position;\n\
layout(location = 1) in vec3 a_Color;\n\
layout(location = 2) in vec2 a_TexCoord;\n\
layout(location = 3) in float a_TexIndex; // <vec2 pos, vec2 tex>\n\
\n\
out vec3 v_Color;\n\
out vec2 v_TexCoord;\n\
out float v_TexIndex;\n\
\n\
uniform mat4 u_ViewProj;\n\
uniform mat4 u_Transform;\n\
\n\
void main()\n\
{\n\
	v_Color = a_Color;\n\
	v_TexCoord = a_TexCoord;\n\
	v_TexIndex = a_TexIndex;\n\
	gl_Position = u_ViewProj * u_Transform * vec4(a_Position.xy,0.0, 1.0);\n\
}"

def FragmentShaderText(MaxTexturesSlots=8) -> str:
    return \
"#version 330 core\n\
#define MAX_TEXTURES_SLOTS "+ str(MaxTexturesSlots) +"\n\
\n\
layout(location = 0) out vec4 o_Color;\n\
\n\
in vec3 v_Color;\n\
in vec2 v_TexCoord;\n\
in float v_TexIndex;\n\
\n\
uniform sampler2D u_Textures[MAX_TEXTURES_SLOTS];\n\
\n\
void main()\n\
{\n\
	int index = int(v_TexIndex);\n\
	vec4 sampled = vec4(1.0, 1.0, 1.0, texture(u_Textures[index], v_TexCoord).r);\n\
	o_Color = vec4(v_Color, 1.0) * sampled;\n\
}"