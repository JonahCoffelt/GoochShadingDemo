import basilisk as bsk

engine = bsk.Engine()
scene = bsk.Scene(engine)
# scene.sky  = None

# Load gooch the shader
goochShader  = bsk.Shader(engine, frag='shaders/gooch.frag')
scene.shader = goochShader

# Edge detection tools
edge_detect_shader = bsk.Shader(engine, vert='shaders/frame.vert', frag='shaders/edge.frag')
edge_detect_fbo = bsk.Framebuffer(engine, shader=edge_detect_shader)
edges = bsk.Framebuffer(engine)

# Texture combination tool
combine_shader = bsk.Shader(engine, vert='shaders/frame.vert', frag='shaders/combine.frag')
combine_fbo = bsk.Framebuffer(engine, shader=combine_shader)

# Set the lights (just looks better with this shader)
scene.light_handler.directional_lights = scene.light_handler.directional_lights[:-1]
scene.light_handler.write(goochShader)

# Load meshes
sphere_mesh   = bsk.Mesh('models/sphere.obj')
monkey_mesh   = bsk.Mesh('models/monkey.obj')
# john_mesh     = bsk.Mesh('models/john.obj')
# bunny_mesh    = bsk.Mesh('models/bunny.obj')
# cylinder_mesh = bsk.Mesh('models/cylinder.obj')

# Load materials
black = bsk.Material(color=(0, 0, 0))
white = bsk.Material(color=(255, 255, 255,))
red   = bsk.Material(color=(255, 0, 0))
green = bsk.Material(color=(0, 255, 0))
blue  = bsk.Material(color=(0, 0, 255))

# Add nodes
sphere0 = bsk.Node(position=(-5, 0, 10), mesh=sphere_mesh, material=black)
sphere1 = bsk.Node(position=(-2.5, 0, 10), mesh=sphere_mesh, material=red)
sphere2 = bsk.Node(position=(0, 0, 10),  mesh=monkey_mesh, material=green)
sphere3 = bsk.Node(position=(2.5, 0, 10),  mesh=sphere_mesh, material=blue)
sphere4 = bsk.Node(position=(5, 0, 10), mesh=sphere_mesh, material=white)


scene.add(sphere0, sphere1, sphere2, sphere3, sphere4)

while engine.running:
    scene.update()

    edge_detect_fbo.bind(scene.frame.input_buffer.depth, 'depthTexture', 0)
    edge_detect_fbo.bind(scene.frame.input_buffer.color_attachments[2], 'normalTexture', 1)
    edge_detect_fbo.render(edges, auto_bind=False)

    combine_fbo.bind(scene.frame.texture, 'goochTexture', 0)
    combine_fbo.bind(edges.texture, 'outlineTexture', 1)
    combine_fbo.render(auto_bind=False)
    
    engine.update(render=False)