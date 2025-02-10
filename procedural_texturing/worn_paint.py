# This Blender python script demonstrates how to create a 
# procedural worn painted metal material. The tutorial covers 
# setting up the material with adjustable parameters such as scale, 
# paint wear, rust amount, and color customizations for the paint, 
# metal, and rust. It also includes roughness and bump strength adjustments for a realistic look. 

import bpy, mathutils

mat = bpy.data.materials.new(name = "Worn Painted Metal")
mat.use_nodes = True
#initialize Worn Painted Metal node group
def worn_painted_metal_node_group():

    worn_painted_metal = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Worn Painted Metal")

    worn_painted_metal.color_tag = 'NONE'
    worn_painted_metal.description = ""
    worn_painted_metal.default_group_node_width = 140
    

    #worn_painted_metal interface
    #Socket Shader
    shader_socket = worn_painted_metal.interface.new_socket(name = "Shader", in_out='OUTPUT', socket_type = 'NodeSocketShader')
    shader_socket.attribute_domain = 'POINT'

    #Socket Scale
    scale_socket = worn_painted_metal.interface.new_socket(name = "Scale", in_out='INPUT', socket_type = 'NodeSocketFloat')
    scale_socket.default_value = 1.0
    scale_socket.min_value = -3.4028234663852886e+38
    scale_socket.max_value = 3.4028234663852886e+38
    scale_socket.subtype = 'NONE'
    scale_socket.attribute_domain = 'POINT'

    #Socket Paint Ware 1
    paint_ware_1_socket = worn_painted_metal.interface.new_socket(name = "Paint Ware 1", in_out='INPUT', socket_type = 'NodeSocketFloat')
    paint_ware_1_socket.default_value = 1.0
    paint_ware_1_socket.min_value = 0.0
    paint_ware_1_socket.max_value = 2.0
    paint_ware_1_socket.subtype = 'NONE'
    paint_ware_1_socket.attribute_domain = 'POINT'

    #Socket Paint Ware 2
    paint_ware_2_socket = worn_painted_metal.interface.new_socket(name = "Paint Ware 2", in_out='INPUT', socket_type = 'NodeSocketFloat')
    paint_ware_2_socket.default_value = 1.0
    paint_ware_2_socket.min_value = 0.0
    paint_ware_2_socket.max_value = 2.0
    paint_ware_2_socket.subtype = 'NONE'
    paint_ware_2_socket.attribute_domain = 'POINT'

    #Socket Rust Amount
    rust_amount_socket = worn_painted_metal.interface.new_socket(name = "Rust Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
    rust_amount_socket.default_value = 1.0
    rust_amount_socket.min_value = -10000.0
    rust_amount_socket.max_value = 10000.0
    rust_amount_socket.subtype = 'NONE'
    rust_amount_socket.attribute_domain = 'POINT'

    #Socket Paint Color
    paint_color_socket = worn_painted_metal.interface.new_socket(name = "Paint Color", in_out='INPUT', socket_type = 'NodeSocketColor')
    paint_color_socket.default_value = (0.7976149916648865, 0.33313000202178955, 0.011567999608814716, 1.0)
    paint_color_socket.attribute_domain = 'POINT'

    #Socket Metal Color
    metal_color_socket = worn_painted_metal.interface.new_socket(name = "Metal Color", in_out='INPUT', socket_type = 'NodeSocketColor')
    metal_color_socket.default_value = (0.19086100161075592, 0.19086100161075592, 0.19086100161075592, 1.0)
    metal_color_socket.attribute_domain = 'POINT'

    #Socket Rust Color
    rust_color_socket = worn_painted_metal.interface.new_socket(name = "Rust Color", in_out='INPUT', socket_type = 'NodeSocketColor')
    rust_color_socket.default_value = (0.09060700237751007, 0.005989000201225281, 0.0, 1.0)
    rust_color_socket.attribute_domain = 'POINT'

    #Socket Metal Roughness
    metal_roughness_socket = worn_painted_metal.interface.new_socket(name = "Metal Roughness", in_out='INPUT', socket_type = 'NodeSocketFloat')
    metal_roughness_socket.default_value = 1.0
    metal_roughness_socket.min_value = 0.0
    metal_roughness_socket.max_value = 2.0
    metal_roughness_socket.subtype = 'NONE'
    metal_roughness_socket.attribute_domain = 'POINT'

    #Socket Paint Roughness
    paint_roughness_socket = worn_painted_metal.interface.new_socket(name = "Paint Roughness", in_out='INPUT', socket_type = 'NodeSocketFloat')
    paint_roughness_socket.default_value = 0.4000000059604645
    paint_roughness_socket.min_value = 0.0
    paint_roughness_socket.max_value = 1.0
    paint_roughness_socket.subtype = 'FACTOR'
    paint_roughness_socket.attribute_domain = 'POINT'

    #Socket Rust Roughness
    rust_roughness_socket = worn_painted_metal.interface.new_socket(name = "Rust Roughness", in_out='INPUT', socket_type = 'NodeSocketFloat')
    rust_roughness_socket.default_value = 0.699999988079071
    rust_roughness_socket.min_value = 0.0
    rust_roughness_socket.max_value = 1.0
    rust_roughness_socket.subtype = 'FACTOR'
    rust_roughness_socket.attribute_domain = 'POINT'

    #Socket Rust Bump Strength
    rust_bump_strength_socket = worn_painted_metal.interface.new_socket(name = "Rust Bump Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
    rust_bump_strength_socket.default_value = 0.20000000298023224
    rust_bump_strength_socket.min_value = 0.0
    rust_bump_strength_socket.max_value = 1.0
    rust_bump_strength_socket.subtype = 'FACTOR'
    rust_bump_strength_socket.attribute_domain = 'POINT'

    #Socket Metal Bump Strength
    metal_bump_strength_socket = worn_painted_metal.interface.new_socket(name = "Metal Bump Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
    metal_bump_strength_socket.default_value = 0.05000000074505806
    metal_bump_strength_socket.min_value = 0.0
    metal_bump_strength_socket.max_value = 1.0
    metal_bump_strength_socket.subtype = 'FACTOR'
    metal_bump_strength_socket.attribute_domain = 'POINT'

    #Socket Worn Bump Strength
    worn_bump_strength_socket = worn_painted_metal.interface.new_socket(name = "Worn Bump Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
    worn_bump_strength_socket.default_value = 0.30000001192092896
    worn_bump_strength_socket.min_value = 0.0
    worn_bump_strength_socket.max_value = 1.0
    worn_bump_strength_socket.subtype = 'FACTOR'
    worn_bump_strength_socket.attribute_domain = 'POINT'


    #initialize worn_painted_metal nodes
    #node Group Output
    group_output = worn_painted_metal.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    #node Group Input
    group_input = worn_painted_metal.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Principled BSDF
    principled_bsdf = worn_painted_metal.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    #Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    #IOR
    principled_bsdf.inputs[3].default_value = 1.5
    #Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    #Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    #Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    #Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    #Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    #Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    #Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    #Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    #Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    #Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    #Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    #Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    #Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    #Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    #Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    #Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    #Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    #Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    #Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    #Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    #Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    #Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    #node Noise Texture
    noise_texture = worn_painted_metal.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '3D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    #Scale
    noise_texture.inputs[2].default_value = 16.0
    #Detail
    noise_texture.inputs[3].default_value = 15.0
    #Roughness
    noise_texture.inputs[4].default_value = 0.6000000238418579
    #Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    #Distortion
    noise_texture.inputs[8].default_value = 0.0

    #node Mapping
    mapping = worn_painted_metal.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    #Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Texture Coordinate
    texture_coordinate = worn_painted_metal.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    #node Color Ramp
    color_ramp = worn_painted_metal.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
    color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
    color_ramp_cre_0.position = 0.3913043141365051
    color_ramp_cre_0.alpha = 1.0
    color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.408212810754776)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    #node Hue/Saturation/Value
    hue_saturation_value = worn_painted_metal.nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value.name = "Hue/Saturation/Value"
    #Hue
    hue_saturation_value.inputs[0].default_value = 0.5
    #Saturation
    hue_saturation_value.inputs[1].default_value = 1.0
    #Fac
    hue_saturation_value.inputs[3].default_value = 1.0

    #node Frame
    frame = worn_painted_metal.nodes.new("NodeFrame")
    frame.label = "Mapping"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    #node Frame.001
    frame_001 = worn_painted_metal.nodes.new("NodeFrame")
    frame_001.label = "Paint Mask 1"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    #node Noise Texture.001
    noise_texture_001 = worn_painted_metal.nodes.new("ShaderNodeTexNoise")
    noise_texture_001.name = "Noise Texture.001"
    noise_texture_001.noise_dimensions = '3D'
    noise_texture_001.noise_type = 'FBM'
    noise_texture_001.normalize = True
    #Scale
    noise_texture_001.inputs[2].default_value = 10.0
    #Detail
    noise_texture_001.inputs[3].default_value = 15.0
    #Roughness
    noise_texture_001.inputs[4].default_value = 1.0
    #Lacunarity
    noise_texture_001.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_001.inputs[8].default_value = 0.0

    #node Color Ramp.001
    color_ramp_001 = worn_painted_metal.nodes.new("ShaderNodeValToRGB")
    color_ramp_001.name = "Color Ramp.001"
    color_ramp_001.color_ramp.color_mode = 'RGB'
    color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_001.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[0])
    color_ramp_001_cre_0 = color_ramp_001.color_ramp.elements[0]
    color_ramp_001_cre_0.position = 0.4178743064403534
    color_ramp_001_cre_0.alpha = 1.0
    color_ramp_001_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_001_cre_1 = color_ramp_001.color_ramp.elements.new(0.46376803517341614)
    color_ramp_001_cre_1.alpha = 1.0
    color_ramp_001_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    #node Hue/Saturation/Value.001
    hue_saturation_value_001 = worn_painted_metal.nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_001.name = "Hue/Saturation/Value.001"
    #Hue
    hue_saturation_value_001.inputs[0].default_value = 0.5
    #Saturation
    hue_saturation_value_001.inputs[1].default_value = 1.0
    #Fac
    hue_saturation_value_001.inputs[3].default_value = 1.0

    #node Frame.002
    frame_002 = worn_painted_metal.nodes.new("NodeFrame")
    frame_002.label = "Paint Mask 2"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    #node Noise Texture.002
    noise_texture_002 = worn_painted_metal.nodes.new("ShaderNodeTexNoise")
    noise_texture_002.name = "Noise Texture.002"
    noise_texture_002.noise_dimensions = '3D'
    noise_texture_002.noise_type = 'FBM'
    noise_texture_002.normalize = True
    #Scale
    noise_texture_002.inputs[2].default_value = 10.0
    #Detail
    noise_texture_002.inputs[3].default_value = 15.0
    #Roughness
    noise_texture_002.inputs[4].default_value = 1.0
    #Lacunarity
    noise_texture_002.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_002.inputs[8].default_value = 0.0

    #node Color Ramp.002
    color_ramp_002 = worn_painted_metal.nodes.new("ShaderNodeValToRGB")
    color_ramp_002.name = "Color Ramp.002"
    color_ramp_002.color_ramp.color_mode = 'RGB'
    color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_002.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[0])
    color_ramp_002_cre_0 = color_ramp_002.color_ramp.elements[0]
    color_ramp_002_cre_0.position = 0.3840579390525818
    color_ramp_002_cre_0.alpha = 1.0
    color_ramp_002_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_002_cre_1 = color_ramp_002.color_ramp.elements.new(0.7004833221435547)
    color_ramp_002_cre_1.alpha = 1.0
    color_ramp_002_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    #node Hue/Saturation/Value.002
    hue_saturation_value_002 = worn_painted_metal.nodes.new("ShaderNodeHueSaturation")
    hue_saturation_value_002.name = "Hue/Saturation/Value.002"
    #Hue
    hue_saturation_value_002.inputs[0].default_value = 0.5
    #Saturation
    hue_saturation_value_002.inputs[1].default_value = 1.0
    #Fac
    hue_saturation_value_002.inputs[3].default_value = 1.0

    #node Noise Texture.003
    noise_texture_003 = worn_painted_metal.nodes.new("ShaderNodeTexNoise")
    noise_texture_003.name = "Noise Texture.003"
    noise_texture_003.noise_dimensions = '3D'
    noise_texture_003.noise_type = 'FBM'
    noise_texture_003.normalize = True
    #Scale
    noise_texture_003.inputs[2].default_value = 5.0
    #Detail
    noise_texture_003.inputs[3].default_value = 15.0
    #Roughness
    noise_texture_003.inputs[4].default_value = 0.699999988079071
    #Lacunarity
    noise_texture_003.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_003.inputs[8].default_value = 0.0

    #node Bump
    bump = worn_painted_metal.nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.invert = False
    #Distance
    bump.inputs[1].default_value = 1.0
    #Normal
    bump.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Frame.003
    frame_003 = worn_painted_metal.nodes.new("NodeFrame")
    frame_003.label = "Metal"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    #node Principled BSDF.001
    principled_bsdf_001 = worn_painted_metal.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.name = "Principled BSDF.001"
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    #Metallic
    principled_bsdf_001.inputs[1].default_value = 0.0
    #IOR
    principled_bsdf_001.inputs[3].default_value = 1.5
    #Alpha
    principled_bsdf_001.inputs[4].default_value = 1.0
    #Diffuse Roughness
    principled_bsdf_001.inputs[7].default_value = 0.0
    #Subsurface Weight
    principled_bsdf_001.inputs[8].default_value = 0.0
    #Subsurface Radius
    principled_bsdf_001.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    #Subsurface Scale
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    #Subsurface Anisotropy
    principled_bsdf_001.inputs[12].default_value = 0.0
    #Specular IOR Level
    principled_bsdf_001.inputs[13].default_value = 0.5
    #Specular Tint
    principled_bsdf_001.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    #Anisotropic
    principled_bsdf_001.inputs[15].default_value = 0.0
    #Anisotropic Rotation
    principled_bsdf_001.inputs[16].default_value = 0.0
    #Tangent
    principled_bsdf_001.inputs[17].default_value = (0.0, 0.0, 0.0)
    #Transmission Weight
    principled_bsdf_001.inputs[18].default_value = 0.0
    #Coat Weight
    principled_bsdf_001.inputs[19].default_value = 0.0
    #Coat Roughness
    principled_bsdf_001.inputs[20].default_value = 0.029999999329447746
    #Coat IOR
    principled_bsdf_001.inputs[21].default_value = 1.5
    #Coat Tint
    principled_bsdf_001.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    #Coat Normal
    principled_bsdf_001.inputs[23].default_value = (0.0, 0.0, 0.0)
    #Sheen Weight
    principled_bsdf_001.inputs[24].default_value = 0.0
    #Sheen Roughness
    principled_bsdf_001.inputs[25].default_value = 0.5
    #Sheen Tint
    principled_bsdf_001.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Color
    principled_bsdf_001.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Strength
    principled_bsdf_001.inputs[28].default_value = 0.0
    #Thin Film Thickness
    principled_bsdf_001.inputs[29].default_value = 0.0
    #Thin Film IOR
    principled_bsdf_001.inputs[30].default_value = 1.3300000429153442

    #node Noise Texture.004
    noise_texture_004 = worn_painted_metal.nodes.new("ShaderNodeTexNoise")
    noise_texture_004.name = "Noise Texture.004"
    noise_texture_004.noise_dimensions = '3D'
    noise_texture_004.noise_type = 'FBM'
    noise_texture_004.normalize = True
    #Scale
    noise_texture_004.inputs[2].default_value = 9.0
    #Detail
    noise_texture_004.inputs[3].default_value = 15.0
    #Roughness
    noise_texture_004.inputs[4].default_value = 0.699999988079071
    #Lacunarity
    noise_texture_004.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_004.inputs[8].default_value = 0.0

    #node Bump.001
    bump_001 = worn_painted_metal.nodes.new("ShaderNodeBump")
    bump_001.name = "Bump.001"
    bump_001.invert = False
    #Distance
    bump_001.inputs[1].default_value = 1.0
    #Normal
    bump_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Frame.004
    frame_004 = worn_painted_metal.nodes.new("NodeFrame")
    frame_004.label = "Rust"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    #node Principled BSDF.002
    principled_bsdf_002 = worn_painted_metal.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_002.name = "Principled BSDF.002"
    principled_bsdf_002.distribution = 'MULTI_GGX'
    principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
    #Metallic
    principled_bsdf_002.inputs[1].default_value = 0.0
    #IOR
    principled_bsdf_002.inputs[3].default_value = 1.5
    #Alpha
    principled_bsdf_002.inputs[4].default_value = 1.0
    #Diffuse Roughness
    principled_bsdf_002.inputs[7].default_value = 0.0
    #Subsurface Weight
    principled_bsdf_002.inputs[8].default_value = 0.0
    #Subsurface Radius
    principled_bsdf_002.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    #Subsurface Scale
    principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
    #Subsurface Anisotropy
    principled_bsdf_002.inputs[12].default_value = 0.0
    #Specular IOR Level
    principled_bsdf_002.inputs[13].default_value = 0.5
    #Specular Tint
    principled_bsdf_002.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    #Anisotropic
    principled_bsdf_002.inputs[15].default_value = 0.0
    #Anisotropic Rotation
    principled_bsdf_002.inputs[16].default_value = 0.0
    #Tangent
    principled_bsdf_002.inputs[17].default_value = (0.0, 0.0, 0.0)
    #Transmission Weight
    principled_bsdf_002.inputs[18].default_value = 0.0
    #Coat Weight
    principled_bsdf_002.inputs[19].default_value = 0.0
    #Coat Roughness
    principled_bsdf_002.inputs[20].default_value = 0.029999999329447746
    #Coat IOR
    principled_bsdf_002.inputs[21].default_value = 1.5
    #Coat Tint
    principled_bsdf_002.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    #Coat Normal
    principled_bsdf_002.inputs[23].default_value = (0.0, 0.0, 0.0)
    #Sheen Weight
    principled_bsdf_002.inputs[24].default_value = 0.0
    #Sheen Roughness
    principled_bsdf_002.inputs[25].default_value = 0.5
    #Sheen Tint
    principled_bsdf_002.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Color
    principled_bsdf_002.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Strength
    principled_bsdf_002.inputs[28].default_value = 0.0
    #Thin Film Thickness
    principled_bsdf_002.inputs[29].default_value = 0.0
    #Thin Film IOR
    principled_bsdf_002.inputs[30].default_value = 1.3300000429153442

    #node Mix
    mix = worn_painted_metal.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'DARKEN'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    #Factor_Float
    mix.inputs[0].default_value = 1.0

    #node Bump.002
    bump_002 = worn_painted_metal.nodes.new("ShaderNodeBump")
    bump_002.name = "Bump.002"
    bump_002.invert = False
    #Distance
    bump_002.inputs[1].default_value = 1.0
    #Normal
    bump_002.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Bump.003
    bump_003 = worn_painted_metal.nodes.new("ShaderNodeBump")
    bump_003.name = "Bump.003"
    bump_003.invert = False
    #Distance
    bump_003.inputs[1].default_value = 1.0

    #node Bump.004
    bump_004 = worn_painted_metal.nodes.new("ShaderNodeBump")
    bump_004.name = "Bump.004"
    bump_004.invert = False
    #Distance
    bump_004.inputs[1].default_value = 1.0

    #node Frame.005
    frame_005 = worn_painted_metal.nodes.new("NodeFrame")
    frame_005.label = "Paint"
    frame_005.name = "Frame.005"
    frame_005.label_size = 20
    frame_005.shrink = True

    #node Mix Shader
    mix_shader = worn_painted_metal.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    #node Mix Shader.001
    mix_shader_001 = worn_painted_metal.nodes.new("ShaderNodeMixShader")
    mix_shader_001.name = "Mix Shader.001"

    #node Color Ramp.003
    color_ramp_003 = worn_painted_metal.nodes.new("ShaderNodeValToRGB")
    color_ramp_003.name = "Color Ramp.003"
    color_ramp_003.color_ramp.color_mode = 'RGB'
    color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
    color_ramp_003.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[0])
    color_ramp_003_cre_0 = color_ramp_003.color_ramp.elements[0]
    color_ramp_003_cre_0.position = 0.3405795991420746
    color_ramp_003_cre_0.alpha = 1.0
    color_ramp_003_cre_0.color = (1.0, 1.0, 1.0, 1.0)

    color_ramp_003_cre_1 = color_ramp_003.color_ramp.elements.new(0.40338173508644104)
    color_ramp_003_cre_1.alpha = 1.0
    color_ramp_003_cre_1.color = (0.14388999342918396, 0.14388999342918396, 0.14388999342918396, 1.0)

    color_ramp_003_cre_2 = color_ramp_003.color_ramp.elements.new(0.5362321734428406)
    color_ramp_003_cre_2.alpha = 1.0
    color_ramp_003_cre_2.color = (1.0, 1.0, 1.0, 1.0)


    #node Map Range
    map_range = worn_painted_metal.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = True
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    #From Min
    map_range.inputs[1].default_value = 0.0
    #To Min
    map_range.inputs[3].default_value = 0.0
    #To Max
    map_range.inputs[4].default_value = 1.0

    #Set parents
    principled_bsdf.parent = frame_003
    noise_texture.parent = frame_001
    mapping.parent = frame
    texture_coordinate.parent = frame
    color_ramp.parent = frame_001
    hue_saturation_value.parent = frame_001
    noise_texture_001.parent = frame_002
    color_ramp_001.parent = frame_002
    hue_saturation_value_001.parent = frame_002
    noise_texture_002.parent = frame_003
    color_ramp_002.parent = frame_003
    hue_saturation_value_002.parent = frame_003
    noise_texture_003.parent = frame_003
    bump.parent = frame_003
    principled_bsdf_001.parent = frame_004
    noise_texture_004.parent = frame_004
    bump_001.parent = frame_004
    principled_bsdf_002.parent = frame_005
    bump_002.parent = frame_005
    bump_003.parent = frame_003
    bump_004.parent = frame_004

    #Set locations
    group_output.location = (1336.6710205078125, 0.0)
    group_input.location = (-1416.9749755859375, -78.93778991699219)
    principled_bsdf.location = (81.79358673095703, 1213.2081298828125)
    noise_texture.location = (-555.2339477539062, 646.2423095703125)
    mapping.location = (-868.6695556640625, 319.9048767089844)
    texture_coordinate.location = (-1030.427001953125, 317.39105224609375)
    color_ramp.location = (-222.50807189941406, 592.8782348632812)
    hue_saturation_value.location = (-398.1706848144531, 630.4268188476562)
    frame.location = (-87.35983276367188, -453.905029296875)
    frame_001.location = (192.18869018554688, -984.3826904296875)
    noise_texture_001.location = (-555.2339477539062, 646.2423095703125)
    color_ramp_001.location = (-230.33847045898438, 637.0921630859375)
    hue_saturation_value_001.location = (-398.1706848144531, 630.4268188476562)
    frame_002.location = (193.73751831054688, -1366.3363037109375)
    noise_texture_002.location = (-581.5336303710938, 1287.27783203125)
    color_ramp_002.location = (-416.75341796875, 1291.5819091796875)
    hue_saturation_value_002.location = (-155.60211181640625, 1280.8775634765625)
    noise_texture_003.location = (-433.66705322265625, 1076.7520751953125)
    bump.location = (-278.4990539550781, 1069.939697265625)
    frame_003.location = (116.28048706054688, -1030.679931640625)
    principled_bsdf_001.location = (109.12448120117188, 1709.478759765625)
    noise_texture_004.location = (-574.1483764648438, 1709.1075439453125)
    bump_001.location = (-275.5672302246094, 1598.3482666015625)
    frame_004.location = (179.30227661132812, -1012.7719116210938)
    principled_bsdf_002.location = (501.4718322753906, 504.904541015625)
    mix.location = (270.91973876953125, -489.9776916503906)
    bump_002.location = (322.70599365234375, 383.4222412109375)
    bump_003.location = (-69.56387329101562, 1075.545654296875)
    bump_004.location = (-98.90778350830078, 1607.3372802734375)
    frame_005.location = (186.06661987304688, -980.5084228515625)
    mix_shader.location = (974.47314453125, -258.150146484375)
    mix_shader_001.location = (1146.6710205078125, -124.6610107421875)
    color_ramp_003.location = (526.7532958984375, -38.10321044921875)
    map_range.location = (778.14599609375, -26.104736328125)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    noise_texture.width, noise_texture.height = 140.0, 100.0
    mapping.width, mapping.height = 140.0, 100.0
    texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
    color_ramp.width, color_ramp.height = 240.0, 100.0
    hue_saturation_value.width, hue_saturation_value.height = 150.0, 100.0
    frame.width, frame.height = 362.0, 359.0
    frame_001.width, frame_001.height = 633.0, 351.0
    noise_texture_001.width, noise_texture_001.height = 140.0, 100.0
    color_ramp_001.width, color_ramp_001.height = 240.0, 100.0
    hue_saturation_value_001.width, hue_saturation_value_001.height = 150.0, 100.0
    frame_002.width, frame_002.height = 624.0, 351.0
    noise_texture_002.width, noise_texture_002.height = 140.0, 100.0
    color_ramp_002.width, color_ramp_002.height = 240.0, 100.0
    hue_saturation_value_002.width, hue_saturation_value_002.height = 150.0, 100.0
    noise_texture_003.width, noise_texture_003.height = 140.0, 100.0
    bump.width, bump.height = 140.0, 100.0
    frame_003.width, frame_003.height = 963.0, 566.0
    principled_bsdf_001.width, principled_bsdf_001.height = 240.0, 100.0
    noise_texture_004.width, noise_texture_004.height = 140.0, 100.0
    bump_001.width, bump_001.height = 140.0, 100.0
    frame_004.width, frame_004.height = 983.0, 413.0
    principled_bsdf_002.width, principled_bsdf_002.height = 240.0, 100.0
    mix.width, mix.height = 140.0, 100.0
    bump_002.width, bump_002.height = 140.0, 100.0
    bump_003.width, bump_003.height = 140.0, 100.0
    bump_004.width, bump_004.height = 140.0, 100.0
    frame_005.width, frame_005.height = 478.9999694824219, 413.0
    mix_shader.width, mix_shader.height = 140.0, 100.0
    mix_shader_001.width, mix_shader_001.height = 140.0, 100.0
    color_ramp_003.width, color_ramp_003.height = 240.0, 100.0
    map_range.width, map_range.height = 140.0, 100.0

    #initialize worn_painted_metal links
    #principled_bsdf.BSDF -> mix_shader.Shader
    worn_painted_metal.links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
    #bump_002.Normal -> principled_bsdf_002.Normal
    worn_painted_metal.links.new(bump_002.outputs[0], principled_bsdf_002.inputs[5])
    #mapping.Vector -> noise_texture_004.Vector
    worn_painted_metal.links.new(mapping.outputs[0], noise_texture_004.inputs[0])
    #noise_texture.Fac -> hue_saturation_value.Color
    worn_painted_metal.links.new(noise_texture.outputs[0], hue_saturation_value.inputs[4])
    #mapping.Vector -> noise_texture_003.Vector
    worn_painted_metal.links.new(mapping.outputs[0], noise_texture_003.inputs[0])
    #hue_saturation_value_002.Color -> principled_bsdf.Roughness
    worn_painted_metal.links.new(hue_saturation_value_002.outputs[0], principled_bsdf.inputs[2])
    #mix.Result -> bump_003.Height
    worn_painted_metal.links.new(mix.outputs[2], bump_003.inputs[2])
    #mix.Result -> mix_shader.Fac
    worn_painted_metal.links.new(mix.outputs[2], mix_shader.inputs[0])
    #bump_001.Normal -> bump_004.Normal
    worn_painted_metal.links.new(bump_001.outputs[0], bump_004.inputs[3])
    #mapping.Vector -> noise_texture.Vector
    worn_painted_metal.links.new(mapping.outputs[0], noise_texture.inputs[0])
    #color_ramp_001.Color -> mix.B
    worn_painted_metal.links.new(color_ramp_001.outputs[0], mix.inputs[7])
    #color_ramp_002.Color -> hue_saturation_value_002.Color
    worn_painted_metal.links.new(color_ramp_002.outputs[0], hue_saturation_value_002.inputs[4])
    #bump.Normal -> bump_003.Normal
    worn_painted_metal.links.new(bump.outputs[0], bump_003.inputs[3])
    #mapping.Vector -> noise_texture_002.Vector
    worn_painted_metal.links.new(mapping.outputs[0], noise_texture_002.inputs[0])
    #noise_texture_002.Fac -> color_ramp_002.Fac
    worn_painted_metal.links.new(noise_texture_002.outputs[0], color_ramp_002.inputs[0])
    #texture_coordinate.Object -> mapping.Vector
    worn_painted_metal.links.new(texture_coordinate.outputs[3], mapping.inputs[0])
    #hue_saturation_value.Color -> color_ramp.Fac
    worn_painted_metal.links.new(hue_saturation_value.outputs[0], color_ramp.inputs[0])
    #noise_texture_003.Fac -> bump.Height
    worn_painted_metal.links.new(noise_texture_003.outputs[0], bump.inputs[2])
    #hue_saturation_value.Color -> color_ramp_003.Fac
    worn_painted_metal.links.new(hue_saturation_value.outputs[0], color_ramp_003.inputs[0])
    #principled_bsdf_002.BSDF -> mix_shader.Shader
    worn_painted_metal.links.new(principled_bsdf_002.outputs[0], mix_shader.inputs[2])
    #noise_texture_004.Fac -> bump_001.Height
    worn_painted_metal.links.new(noise_texture_004.outputs[0], bump_001.inputs[2])
    #map_range.Result -> mix_shader_001.Fac
    worn_painted_metal.links.new(map_range.outputs[0], mix_shader_001.inputs[0])
    #mapping.Vector -> noise_texture_001.Vector
    worn_painted_metal.links.new(mapping.outputs[0], noise_texture_001.inputs[0])
    #hue_saturation_value_001.Color -> color_ramp_001.Fac
    worn_painted_metal.links.new(hue_saturation_value_001.outputs[0], color_ramp_001.inputs[0])
    #noise_texture_001.Fac -> hue_saturation_value_001.Color
    worn_painted_metal.links.new(noise_texture_001.outputs[0], hue_saturation_value_001.inputs[4])
    #mix.Result -> bump_002.Height
    worn_painted_metal.links.new(mix.outputs[2], bump_002.inputs[2])
    #color_ramp_003.Color -> map_range.Value
    worn_painted_metal.links.new(color_ramp_003.outputs[0], map_range.inputs[0])
    #principled_bsdf_001.BSDF -> mix_shader_001.Shader
    worn_painted_metal.links.new(principled_bsdf_001.outputs[0], mix_shader_001.inputs[1])
    #mix_shader.Shader -> mix_shader_001.Shader
    worn_painted_metal.links.new(mix_shader.outputs[0], mix_shader_001.inputs[2])
    #bump_004.Normal -> principled_bsdf_001.Normal
    worn_painted_metal.links.new(bump_004.outputs[0], principled_bsdf_001.inputs[5])
    #color_ramp.Color -> mix.A
    worn_painted_metal.links.new(color_ramp.outputs[0], mix.inputs[6])
    #bump_003.Normal -> principled_bsdf.Normal
    worn_painted_metal.links.new(bump_003.outputs[0], principled_bsdf.inputs[5])
    #mix.Result -> bump_004.Height
    worn_painted_metal.links.new(mix.outputs[2], bump_004.inputs[2])
    #mix_shader_001.Shader -> group_output.Shader
    worn_painted_metal.links.new(mix_shader_001.outputs[0], group_output.inputs[0])
    #group_input.Scale -> mapping.Scale
    worn_painted_metal.links.new(group_input.outputs[0], mapping.inputs[3])
    #group_input.Paint Ware 1 -> hue_saturation_value.Value
    worn_painted_metal.links.new(group_input.outputs[1], hue_saturation_value.inputs[2])
    #group_input.Paint Ware 2 -> hue_saturation_value_001.Value
    worn_painted_metal.links.new(group_input.outputs[2], hue_saturation_value_001.inputs[2])
    #group_input.Rust Amount -> map_range.From Max
    worn_painted_metal.links.new(group_input.outputs[3], map_range.inputs[2])
    #group_input.Paint Color -> principled_bsdf_002.Base Color
    worn_painted_metal.links.new(group_input.outputs[4], principled_bsdf_002.inputs[0])
    #group_input.Metal Color -> principled_bsdf.Base Color
    worn_painted_metal.links.new(group_input.outputs[5], principled_bsdf.inputs[0])
    #group_input.Rust Color -> principled_bsdf_001.Base Color
    worn_painted_metal.links.new(group_input.outputs[6], principled_bsdf_001.inputs[0])
    #group_input.Metal Roughness -> hue_saturation_value_002.Value
    worn_painted_metal.links.new(group_input.outputs[7], hue_saturation_value_002.inputs[2])
    #group_input.Paint Roughness -> principled_bsdf_002.Roughness
    worn_painted_metal.links.new(group_input.outputs[8], principled_bsdf_002.inputs[2])
    #group_input.Rust Roughness -> principled_bsdf_001.Roughness
    worn_painted_metal.links.new(group_input.outputs[9], principled_bsdf_001.inputs[2])
    #group_input.Rust Bump Strength -> bump_001.Strength
    worn_painted_metal.links.new(group_input.outputs[10], bump_001.inputs[0])
    #group_input.Metal Bump Strength -> bump.Strength
    worn_painted_metal.links.new(group_input.outputs[11], bump.inputs[0])
    #group_input.Worn Bump Strength -> bump_004.Strength
    worn_painted_metal.links.new(group_input.outputs[12], bump_004.inputs[0])
    #group_input.Worn Bump Strength -> bump_003.Strength
    worn_painted_metal.links.new(group_input.outputs[12], bump_003.inputs[0])
    #group_input.Worn Bump Strength -> bump_002.Strength
    worn_painted_metal.links.new(group_input.outputs[12], bump_002.inputs[0])
    return worn_painted_metal

worn_painted_metal = worn_painted_metal_node_group()

#initialize Worn Painted Metal node group
def worn_painted_metal_1_node_group():

    worn_painted_metal_1 = mat.node_tree
    #start with a clean node tree
    for node in worn_painted_metal_1.nodes:
        worn_painted_metal_1.nodes.remove(node)
    worn_painted_metal_1.color_tag = 'NONE'
    worn_painted_metal_1.description = ""
    worn_painted_metal_1.default_group_node_width = 140
    

    #worn_painted_metal_1 interface

    #initialize worn_painted_metal_1 nodes
    #node Material Output
    material_output = worn_painted_metal_1.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    #Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Thickness
    material_output.inputs[3].default_value = 0.0

    #node Group
    group = worn_painted_metal_1.nodes.new("ShaderNodeGroup")
    group.name = "Group"
    group.node_tree = worn_painted_metal
    #Socket_1
    group.inputs[0].default_value = 1.0
    #Socket_2
    group.inputs[1].default_value = 1.0
    #Socket_3
    group.inputs[2].default_value = 1.0
    #Socket_4
    group.inputs[3].default_value = 1.0
    #Socket_5
    group.inputs[4].default_value = (0.7976149916648865, 0.33313000202178955, 0.011567999608814716, 1.0)
    #Socket_6
    group.inputs[5].default_value = (0.19086100161075592, 0.19086100161075592, 0.19086100161075592, 1.0)
    #Socket_7
    group.inputs[6].default_value = (0.09060700237751007, 0.005989000201225281, 0.0, 1.0)
    #Socket_8
    group.inputs[7].default_value = 1.0
    #Socket_9
    group.inputs[8].default_value = 0.4000000059604645
    #Socket_10
    group.inputs[9].default_value = 0.699999988079071
    #Socket_11
    group.inputs[10].default_value = 0.20000000298023224
    #Socket_12
    group.inputs[11].default_value = 0.05000000074505806
    #Socket_13
    group.inputs[12].default_value = 0.30000001192092896


    #Set locations
    material_output.location = (1111.848876953125, 867.2839965820312)
    group.location = (841.9303588867188, 873.5743408203125)

    #Set dimensions
    material_output.width, material_output.height = 140.0, 100.0
    group.width, group.height = 259.27862548828125, 100.0

    #initialize worn_painted_metal_1 links
    #group.Shader -> material_output.Surface
    worn_painted_metal_1.links.new(group.outputs[0], material_output.inputs[0])
    return worn_painted_metal_1

worn_painted_metal_1 = worn_painted_metal_1_node_group()


# can you change the color or the paint to red, and can you increase the rust 





