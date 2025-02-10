
import bpy
import mathutils

def worn_painted_metal_node_group():
    worn_painted_metal = bpy.data.node_groups.new(type='ShaderNodeTree', name="Worn Painted Metal")

    # Interface setup
    shader_socket = worn_painted_metal.inputs.new('NodeSocketShader', "Shader")
    scale_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Scale")
    scale_socket.default_value = 1.0
    paint_ware_1_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Paint Ware 1")
    paint_ware_1_socket.default_value = 1.0
    paint_ware_2_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Paint Ware 2")
    paint_ware_2_socket.default_value = 1.0
    rust_amount_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Rust Amount")
    rust_amount_socket.default_value = 5.0  # Increased rust amount
    
    paint_color_socket = worn_painted_metal.inputs.new('NodeSocketColor', "Paint Color")
    paint_color_socket.default_value = (1.0, 0.0, 0.0, 1.0)  # Red paint color
    metal_color_socket = worn_painted_metal.inputs.new('NodeSocketColor', "Metal Color")
    metal_color_socket.default_value = (0.19, 0.19, 0.19, 1.0)
    rust_color_socket = worn_painted_metal.inputs.new('NodeSocketColor', "Rust Color")
    rust_color_socket.default_value = (0.09, 0.005, 0.0, 1.0)
    
    metal_roughness_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Metal Roughness")
    metal_roughness_socket.default_value = 1.0
    paint_roughness_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Paint Roughness")
    paint_roughness_socket.default_value = 0.4
    rust_roughness_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Rust Roughness")
    rust_roughness_socket.default_value = 0.7
    rust_bump_strength_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Rust Bump Strength")
    rust_bump_strength_socket.default_value = 0.2
    metal_bump_strength_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Metal Bump Strength")
    metal_bump_strength_socket.default_value = 0.05
    worn_bump_strength_socket = worn_painted_metal.inputs.new('NodeSocketFloat', "Worn Bump Strength")
    worn_bump_strength_socket.default_value = 0.3

    # Nodes
    group_output = worn_painted_metal.nodes.new("NodeGroupOutput")
    group_input = worn_painted_metal.nodes.new("NodeGroupInput")
    principled_bsdf = worn_painted_metal.nodes.new("ShaderNodeBsdfPrincipled")
    noise_texture = worn_painted_metal.nodes.new("ShaderNodeTexNoise")
    mapping = worn_painted_metal.nodes.new("ShaderNodeMapping")
    texture_coordinate = worn_painted_metal.nodes.new("ShaderNodeTexCoord")
    color_ramp = worn_painted_metal.nodes.new("ShaderNodeValToRGB")
    hue_saturation_value = worn_painted_metal.nodes.new("ShaderNodeHueSaturation")
    bump = worn_painted_metal.nodes.new("ShaderNodeBump")
    mix_shader = worn_painted_metal.nodes.new("ShaderNodeMixShader")

    # Links
    worn_painted_metal.links.new(group_input.outputs["Scale"], mapping.inputs["Scale"])
    worn_painted_metal.links.new(mapping.outputs["Vector"], noise_texture.inputs["Vector"])
    worn_painted_metal.links.new(noise_texture.outputs["Fac"], hue_saturation_value.inputs["Color"])
    worn_painted_metal.links.new(hue_saturation_value.outputs["Color"], color_ramp.inputs["Fac"])
    worn_painted_metal.links.new(color_ramp.outputs["Color"], principled_bsdf.inputs["Base Color"])
    worn_painted_metal.links.new(bump.outputs["Normal"], principled_bsdf.inputs["Normal"])
    worn_painted_metal.links.new(principled_bsdf.outputs["BSDF"], mix_shader.inputs[1])
    worn_painted_metal.links.new(mix_shader.outputs[0], group_output.inputs[0])

    return worn_painted_metal


# Create new material
mat = bpy.data.materials.new(name="Worn Painted Metal")
mat.use_nodes = True

# Assign node group to material
def worn_painted_metal_1_node_group(mat):
    worn_painted_metal_1 = mat.node_tree
    
    # Cleaning node tree
    for node in worn_painted_metal_1.nodes:
        worn_painted_metal_1.nodes.remove(node)

    # Nodes
    material_output = worn_painted_metal_1.nodes.new("ShaderNodeOutputMaterial")
    group = worn_painted_metal_1.nodes.new("ShaderNodeGroup")
    group.node_tree = worn_painted_metal_node_group()

    # Connections
    worn_painted_metal_1.links.new(group.outputs[0], material_output.inputs[0])

    return worn_painted_metal_1

# Assign the material to an object
bpy.context.object.active_material = mat
worn_painted_metal_1_node_group(mat)
