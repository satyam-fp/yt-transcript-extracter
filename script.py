
import bpy

# Create a new material
material = bpy.data.materials.new(name="Scratched Plastic")
material.use_nodes = True

# Clear existing nodes
nodes = material.node_tree.nodes
nodes.clear()

# Create Node Group for the Scratched Plastic Material
def create_scratched_plastic_node_group():
    node_group = bpy.data.node_groups.new('ScratchedPlastic', 'ShaderNodeTree')

    # Create inputs
    node_group_inputs = node_group.nodes.new('NodeGroupInput')
    node_group_inputs.location = (-1000, 0)

    # Create outputs
    node_group_outputs = node_group.nodes.new('NodeGroupOutput')
    node_group_outputs.location = (1000, 0)

    inputs = node_group.inputs
    inputs.new('NodeSocketFloat', 'Scale')
    inputs.new('NodeSocketColor', 'Plastic Color')
    inputs.new('NodeSocketFloat', 'Subsurface')
    inputs.new('NodeSocketFloat', 'Roughness')
    inputs.new('NodeSocketFloat', 'Noise Roughness Scale')
    inputs.new('NodeSocketFloat', 'Noise Roughness Detail')
    inputs.new('NodeSocketColor', 'Scratches Color')
    inputs.new('NodeSocketFloat', 'Scratches Detail')
    inputs.new('NodeSocketFloat', 'Scratches Distortion')
    inputs.new('NodeSocketFloat', 'Scratches Scale 1')
    inputs.new('NodeSocketFloat', 'Scratches Thickness 1')
    inputs.new('NodeSocketFloat', 'Scratches Scale 2')
    inputs.new('NodeSocketFloat', 'Scratches Thickness 2')
    inputs.new('NodeSocketFloat', 'Scratches Bump Strength')
    inputs.new('NodeSocketFloat', 'Noise Bump Strength')

    outputs = node_group.outputs
    outputs.new('NodeSocketShader', 'Shader')

    nodes = node_group.nodes

    # Create and configure nodes
    # Principled BSDF Node
    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (300, 0)
    principled_bsdf.inputs['Metallic'].default_value = 0.0
    principled_bsdf.inputs['Specular'].default_value = 0.5
    principled_bsdf.inputs['Transmission'].default_value = 0.0

    # Magic Texture Node for Scratches 1
    magic_texture_1 = nodes.new('ShaderNodeTexMagic')
    magic_texture_1.location = (-800, 300)
    magic_texture_1.turbulence_depth = 5

    # Magic Texture Node for Scratches 2
    magic_texture_2 = nodes.new('ShaderNodeTexMagic')
    magic_texture_2.location = (-800, 100)
    magic_texture_2.turbulence_depth = 5

    # ColorRamp Node for Scratches 1
    color_ramp_1 = nodes.new('ShaderNodeValToRGB')
    color_ramp_1.location = (-600, 300)
    color_ramp_1.color_ramp.interpolation = 'CONSTANT'
    
    # ColorRamp Node for Scratches 2
    color_ramp_2 = nodes.new('ShaderNodeValToRGB')
    color_ramp_2.location = (-600, 100)
    color_ramp_2.color_ramp.interpolation = 'CONSTANT'

    # Mix Shader for joining scratches
    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (600, 0)

    # Bump Node
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -100)
    bump.inputs['Strength'].default_value = 0.1

    # Set node tree links
    links = node_group.links
    link = links.new

    # Connect nodes
    link(magic_texture_1.outputs['Color'], color_ramp_1.inputs['Fac'])
    link(magic_texture_2.outputs['Color'], color_ramp_2.inputs['Fac'])
    link(color_ramp_1.outputs['Color'], bump.inputs['Height'])
    link(color_ramp_2.outputs['Color'], principled_bsdf.inputs['Base Color'])
    link(principled_bsdf.outputs['BSDF'], node_group_outputs.inputs['Shader'])
    link(bump.outputs['Normal'], principled_bsdf.inputs['Normal'])

    return node_group

# Add the node group to the material
scratched_plastic_group = create_scratched_plastic_node_group()

# Add nodes to material's node tree
nodes = material.node_tree.nodes
group_node = nodes.new("ShaderNodeGroup")
group_node.node_tree = scratched_plastic_group
group_node.location = 0, 0

material_output = nodes.new('ShaderNodeOutputMaterial')
material_output.location = (200, 0)

# Connect material nodes
links = material.node_tree.links
links.new(group_node.outputs['Shader'], material_output.inputs['Surface'])

# Assign the material to active object
if bpy.context.active_object is not None:
    obj = bpy.context.active_object
    if obj.data is not None:
        if len(obj.data.materials):
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
