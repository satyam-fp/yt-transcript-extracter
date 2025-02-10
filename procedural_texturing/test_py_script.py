import bpy

# Set render engine to Cycles (required for displacement and node-based adaptive details)
bpy.context.scene.render.engine = 'CYCLES'

# Create a new material and enable node usage
mat = bpy.data.materials.new(name="Procedural_Tree_Bark")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Remove default nodes
for node in nodes:
    nodes.remove(node)

# Create the Material Output node
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (800, 0)

# Create the Principled BSDF node
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (400, 0)
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# --- Coordinate & Mapping Setup ---
# Texture Coordinate: use the Object output
tex_coord = nodes.new(type='ShaderNodeTexCoord')
tex_coord.location = (-800, 300)

# Mapping node to allow coordinate scaling and adjustment
mapping = nodes.new(type='ShaderNodeMapping')
mapping.location = (-600, 300)
# For tree bark the texture is stretched vertically – here we set Z scale to 0.2.
mapping.inputs['Scale'].default_value[2] = 0.2

# --- Distortion Setup for the Voronoi (Base Bark Texture) ---
# Add a Noise Texture to provide some random distortion to the coordinates
dist_noise = nodes.new(type='ShaderNodeTexNoise')
dist_noise.location = (-800, 0)
dist_noise.inputs['Scale'].default_value = 8.0
dist_noise.inputs['Detail'].default_value = 15.0

# Mix the object coordinates with the noise (using a low factor so the distortion is subtle)
mix_dist = nodes.new(type='ShaderNodeMixRGB')
mix_dist.location = (-600, 0)
mix_dist.blend_type = 'LINEAR_LIGHT'
mix_dist.inputs['Fac'].default_value = 0.08

# --- Voronoi Texture (Core Bark Pattern) ---
voronoi = nodes.new(type='ShaderNodeTexVoronoi')
voronoi.location = (-400, 300)
# Set the distance metric to Chebyshev to get the “squared” cell look common in bark
voronoi.distance_metric = 'CHEBYCHEV'
voronoi.inputs['Scale'].default_value = 8.0

# --- Bark Base Color via ColorRamp ---
color_ramp_bark = nodes.new(type='ShaderNodeValToRGB')
color_ramp_bark.location = (-200, 500)
# Remove the second default element so we can add two additional stops
color_ramp_bark.color_ramp.elements.remove(color_ramp_bark.color_ramp.elements[1])
# First stop (light brown) – approximate hex #796759 (121,103,89)
elem0 = color_ramp_bark.color_ramp.elements[0]
elem0.position = 0.0
elem0.color = (0.475, 0.404, 0.349, 1)
# Add middle stop (medium brown) – hex #593F29 (89,63,41)
elem1 = color_ramp_bark.color_ramp.elements.new(0.5)
elem1.color = (0.349, 0.247, 0.161, 1)
# Add final stop (dark brown) – hex #0D0905 (13,9,5)
elem2 = color_ramp_bark.color_ramp.elements.new(1.0)
elem2.color = (0.051, 0.035, 0.020, 1)

# --- Roughness Control via a Second ColorRamp ---
color_ramp_rough = nodes.new(type='ShaderNodeValToRGB')
color_ramp_rough.location = (-200, 200)
# Use two stops: lower roughness (approx. #B3B3B3) and higher roughness (approx. #EDEDED)
cr_elem0 = color_ramp_rough.color_ramp.elements[0]
cr_elem0.position = 0.0
cr_elem0.color = (0.7, 0.7, 0.7, 1)
cr_elem1 = color_ramp_rough.color_ramp.elements[1]
cr_elem1.position = 1.0
cr_elem1.color = (0.93, 0.93, 0.93, 1)

# --- Moss Mask and Integration ---
# Create a Noise Texture for moss pattern (adds high-detail variation)
moss_noise = nodes.new(type='ShaderNodeTexNoise')
moss_noise.location = (-800, -300)
moss_noise.inputs['Scale'].default_value = 7.0
moss_noise.inputs['Detail'].default_value = 15.0
moss_noise.inputs['Roughness'].default_value = 0.865
moss_noise.inputs['Distortion'].default_value = 0.3
links.new(tex_coord.outputs['Object'], moss_noise.inputs['Vector'])

# A ColorRamp to boost contrast in the moss mask; adjust the positions to control moss amount
moss_color_ramp = nodes.new(type='ShaderNodeValToRGB')
moss_color_ramp.location = (-600, -300)
moss_color_ramp.color_ramp.elements[0].position = 0.4
moss_color_ramp.color_ramp.elements[1].position = 0.6
links.new(moss_noise.outputs['Fac'], moss_color_ramp.inputs['Fac'])

# Use a MixRGB node to blend the bark base with a mossy green color
moss_mix = nodes.new(type='ShaderNodeMixRGB')
moss_mix.location = (0, 500)
moss_mix.blend_type = 'MIX'
# Base bark from the bark color ramp will be color1; color2 is the moss color (greenish brown, hex #436C28 ≈ (0.263, 0.424, 0.157))
moss_mix.inputs['Color2'].default_value = (0.263, 0.424, 0.157, 1)
# Factor is provided by the moss mask (from the moss color ramp)
links.new(moss_color_ramp.outputs['Fac'], moss_mix.inputs['Fac'])
links.new(color_ramp_bark.outputs['Color'], moss_mix.inputs['Color1'])

# --- Bump Chain for Additional Surface Detail ---
# First bump node: use the Voronoi distance as height for a subtle bark bump
bump1 = nodes.new(type='ShaderNodeBump')
bump1.location = (0, 200)
bump1.inputs['Strength'].default_value = 0.35
links.new(voronoi.outputs['Distance'], bump1.inputs['Height'])

# Create an extra Noise Texture (for noise bump details)
bump_noise = nodes.new(type='ShaderNodeTexNoise')
bump_noise.location = (-800, 200)
bump_noise.inputs['Scale'].default_value = 4.0
bump_noise.inputs['Detail'].default_value = 15.0
bump_noise.inputs['Roughness'].default_value = 0.6
links.new(tex_coord.outputs['Object'], bump_noise.inputs['Vector'])

# Second bump node: adds extra noise detail to the normals
bump2 = nodes.new(type='ShaderNodeBump')
bump2.location = (200, 200)
bump2.inputs['Strength'].default_value = 8.4
links.new(bump_noise.outputs['Fac'], bump2.inputs['Height'])
links.new(bump1.outputs['Normal'], bump2.inputs['Normal'])

# Third bump node: accentuate the moss areas for extra relief
bump3 = nodes.new(type='ShaderNodeBump')
bump3.location = (400, 200)
bump3.inputs['Strength'].default_value = 1.0
links.new(moss_color_ramp.outputs['Fac'], bump3.inputs['Height'])
links.new(bump2.outputs['Normal'], bump3.inputs['Normal'])
# Connect final bump output to the Principled BSDF normal input
links.new(bump3.outputs['Normal'], bsdf.inputs['Normal'])

# --- Displacement Setup ---
# Add a Displacement node so the mesh itself is displaced (requires a subdivided mesh)
disp_node = nodes.new(type='ShaderNodeDisplacement')
disp_node.location = (400, -200)
disp_node.inputs['Scale'].default_value = 0.14
links.new(voronoi.outputs['Distance'], disp_node.inputs['Height'])
links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

# --- Linking the Core Chain ---
# Mix the distorted coordinates into the Mapping node:
links.new(tex_coord.outputs['Object'], mix_dist.inputs['Color1'])
links.new(dist_noise.outputs['Fac'], mix_dist.inputs['Color2'])
links.new(mix_dist.outputs['Color'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])

# Send Voronoi’s distance into the color ramps for bark color and roughness
links.new(voronoi.outputs['Distance'], color_ramp_bark.inputs['Fac'])
links.new(voronoi.outputs['Distance'], color_ramp_rough.inputs['Fac'])
links.new(color_ramp_rough.outputs['Color'], bsdf.inputs['Roughness'])

# Blend the bark base with the moss color via the Mix node and assign it to the Base Color
links.new(color_ramp_bark.outputs['Color'], moss_mix.inputs['Color1'])
links.new(moss_mix.outputs['Color'], bsdf.inputs['Base Color'])

# Set the material displacement method (this tells Cycles to use true displacement)
mat.cycles.displacement_method = 'DISPLACEMENT'

# --- Assign Material to an Object ---
# If an active mesh object exists, assign the material; otherwise create an icosphere to preview.
if bpy.context.active_object is not None and bpy.context.active_object.type == 'MESH':
    if bpy.context.active_object.data.materials:
        bpy.context.active_object.data.materials[0] = mat
    else:
        bpy.context.active_object.data.materials.append(mat)
else:
    bpy.ops.mesh.primitive_ico_sphere_add(radius=1, location=(0, 0, 0))
    bpy.context.active_object.data.materials.append(mat)

print("Procedural Tree Bark material created and assigned!")
