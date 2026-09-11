# -*- coding: utf-8 -*-
import bpy
import os
import math

# --- OVLADACI MENU ---
# --- OVLADACI MENU ---

# 0. NASTAVENI SVETLA A MATERIALU
# Zadej jmeno .hdr souboru, ktery jsi ulozil do slozky 'hdri'
HDRI_FILE_NAME = "snow.exr"  # <--- DOPLN PRESNY NAZEV SOUBORU!

# Slovnik pro upravu materialu. Pro kazdy material muzes definovat:
# "color": (R, G, B, A) - kazda hodnota od 0.0 do 1.0
# "roughness": 0.0 (zrcadlo) az 1.0 (matny)
# "metallic": 0.0 (plast) az 1.0 (kov)
# Co nezadas, to se z modelu nezmeni.
# Jmena materialu zjistis, kdyz otevres .glb soubor v Blenderu a podivas se do zalozky Material Properties.
UPRAVIT_MATERIALY = {
    "barva": {
     #"color": (0.042135, 0.167512, 0.288296, 1.0), # modrá
     #"color": (0.11, 0.43, 0.73, 0.255),  # sklo asi
        "color": (0.8, 0.1, 0.1, 1.0),  # Tmave cervena, plne nepruhledna
        "roughness": 0.0,
        "metallic": 1.0
    },
   "pruh": {
     #"color": (0.042135, 0.167512, 0.288296, 1.0),
     #"color": (0.11, 0.43, 0.73, 0.255),
        "color": (0.8, 0.1, 0.1, 1.0),  # Tmave cervena, plne nepruhledna
        "roughness": 0.0,
        "metallic": 1.0
    },
  "celo": {
     #"color": (0.042135, 0.167512, 0.288296, 1.0),
     #"color": (0.11, 0.43, 0.73, 0.255),
        "color": (0.8, 0.1, 0.1, 1.0),  # Tmave cervena, plne nepruhledna
        "roughness": 0.0,
        "metallic": 1.0
    },
   "dvere": {
     #"color": (0.042135, 0.167512, 0.288296, 1.0),
     #"color": (0.11, 0.43, 0.73, 0.255),
        "color": (0.8, 0.1, 0.1, 1.0),  # Tmave cervena, plne nepruhledna
        "roughness": 0.0,
        "metallic": 1.0
    },
    "naklad": {
     #   "color": (0.302, 0.369, 0.369, 1.0),   # seda
        "color": (0.133, 0.133, 0.149, 1.0),   #cerna
     #   "color": (0.651, 0.518, 0.212, 1.0),   # zlutabrambor
     #   "color": (0.66, 0.478, 0.02, 1.0),   # zluta
     #   "color": (0.20, 0.12, 0.05, 1.0),  #hneda
        "roughness": 1.00,
        "metallic": 1.0
    },
     "plachta": {
     #   "color": (0.302, 0.369, 0.369, 1.0),   # seda
     #   "color": (0.74, 0.48, 0.0, 1.0),   #zluta plachta
     #   "color": (0.651, 0.518, 0.212, 1.0),   # zlutabrambor
     #   "color": (0.66, 0.478, 0.02, 1.0),   # zluta
       # "color": (0.8, 0.6, 0.0, 1.0),  #zlut
           "color": (0.761, 0.298, 0.024, 1.0),  # barva kurty
     #   "color": (0.9, 0.85, 0.2, 1.0),  # zluta plachta
     #   "color": (0.8, 0.75, 0.1, 1.0),  # tmavsi zluta
        #"color": (1.0, 1.0, 0.0, 1.0),  # zluta jasna
     #   "color": (0.75, 0.75, 0.65, 1.0),  # sedozluta plachta
     #   "color": (0.72, 0.72, 0.66, 1.0),  # seda velmi jemna zluta nadech
     #   "color": (0.70, 0.70, 0.68, 1.0),  # téměř šedá, lehce tepla
            "roughness": 0.0,
            "metallic": 1.0
       # "roughness": 1.00,
       # "metallic": 1.0
    },
    "korba": {
        "color": (0.302, 0.369, 0.369, 1.0),   # seda
      #  "color": (0.36, 0.22, 0.10, 1.0),  # hneda
        "roughness": 0.0,
        "metallic": 1.0
    #  "roughness": 1.00,
    #  "metallic": 1.0
    },
    "bedna": {
        "color": (0.651, 0.518, 0.212, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "chrom": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.1,
        "metallic": 1.0
        # Barvu zde nezadavame, takze zustane ta, co je v modelu
    },
    "taz123": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.1,
        "metallic": 1.0
        # Barvu zde nezadavame, takze zustane ta, co je v modelu
    },
    "nadrz": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.1,
        "metallic": 1.0
        # Barvu zde nezadavame, takze zustane ta, co je v modelu
    },
    "lista": {
        "color": (0.55, 0.55, 0.55, 1.0),  # 
        "roughness": 0.00,
        "metallic": 1.0
    },
    "listapredek": {
        "color": (0.55, 0.55, 0.55, 1.0),  # 
        "roughness": 0.00,
        "metallic": 1.0
    },
     "okna": {
         "color": (0.9, 0.9, 1.0, 0.1),
         "roughness": 0.0,
         "metallic": 0.0
   },
    "sedacky": {
        "color": (0.55, 0.27, 0.07, 1.0),  # 
        "roughness": 0.04,
        "metallic": 0.0
    },
    "antena": {
        "color": (0.13, 0.12, 0.12, 1.0),  # 
        "roughness": 0.00,
        "metallic": 1.0
    },
    "Material": {
        "color": (0.13, 0.12, 0.12, 1.0),  # palubka
        "roughness": 1.00,
        "metallic": 1.0
    },
    "zrcatko": {
        "color": (0.02, 0.02, 0.02, 1.0),  # 
        "roughness": 0.00,
        "metallic": 1.0
    },
    "sterace": {
        "color": (0.13, 0.12, 0.12, 1.0),  # 
        "roughness": 0.00,
        "metallic": 1.0
    },
    "svetla": {
        "color": (1.0, 1.0, 1.0, 1.0),  # 
        "roughness": 0.05,
        "metallic": 0.0
    },
    "blinkry": {
        "color": (1.0, 0.65, 0.0, 1.0),  # 
        "roughness": 0.1,
        "metallic": 0.0
    },
  "majak": {
        "color": (1.0, 0.65, 0.0, 1.0),  # 
        "roughness": 0.1,
        "metallic": 0.0
    },
    "brzdovky": {
        "color": (1.0, 0.0, 0.0, 1.0),  # 
        "roughness": 0.05,
        "metallic": 0.0
    },
    "kufr1": {
        "color": (0.20, 0.12, 0.05, 1.0),   # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "kufr2": {
        "color": (0.36, 0.22, 0.10, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "kufr3": {
        "color": (0.45, 0.08, 0.08, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "kurty": {
        "color": (0.761, 0.298, 0.024, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "zahradka": {
        "color": (0.02, 0.02, 0.02, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "narazniky": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.0,
        "metallic": 1.0
    },
    "podvozek": {
        "color": (0.02, 0.02, 0.02, 1.0),  #  černa z pneu
     #   "color": (0.13, 0.12, 0.12, 1.0),  # 
        "roughness": 0.00,
        "metallic": 1.0
    },
    "pneu": {
      #  "color": (0.70, 0.70, 0.68, 1.0),  # téměř šedá, lehce tep
        "color": (0.042135, 0.167512, 0.288296, 1.0), # modra
   #  "color": (0.11, 0.43, 0.73, 0.255),  # sklo asi
   #  "color": (0.02, 0.02, 0.02, 1.0),  # 
      # "color": (0.55, 0.55, 0.55, 1.0),  #chrom
      #  "roughness": 0.1,     # chrom
        "roughness": 0.00,  #  chrom
        "metallic": 1.0   #  chrom
    },
    "pneu 1": {
      "color": (0.042135, 0.167512, 0.288296, 1.0),
        "color": (0.02, 0.02, 0.02, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "pneu 2": {
        "color": (0.02, 0.02, 0.02, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "pneu 3": {
        "color": (0.02, 0.02, 0.02, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "pneu 4": {
        "color": (0.02, 0.02, 0.02, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "disky": {
        "color": (1.0, 0.82, 0.0, 1.0), # zluta gpt
    # "color": (0.761, 0.298, 0.024, 1.0), #kurty oranž
    # "color": (1.0, 1.0, 0.0, 1.0),  # zluta jasna
    # "color": (1.0, 1.0, 1.0, 1.0),  # 
        "roughness": 0.00,
        "metallic": 1.0
    },
    "disky 1": {
        "color": (1.0, 1.0, 1.0, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "disky 2": {
        "color": (1.0, 1.0, 1.0, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "disky 3": {
        "color": (1.0, 1.0, 1.0, 1.0),  # 
        "roughness": 1.00,
        "metallic": 1.0
    },
    "poklice": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.0,
        "metallic": 1.0
    },
    "poklice 1": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.0,
        "metallic": 1.0
    },
    "poklice 2": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.0,
        "metallic": 1.0
    },
    "poklice 3": {
        "color": (0.55, 0.55, 0.55, 1.0),
        "roughness": 0.0,
        "metallic": 1.0
    },





   #"Clear": {
        #"color": (0.0, 0.0, 0.0, 0.0), 
    #},

    #"Rubber": {
        #"roughness": 0.0, # Matna guma
        #"metallic": 1.0
    #}



    # 'Blue_Car_Paint': [1.0, 0.0, 0.0],

    # 'Blue_Car_Paint': (0.0, 1.0),   # [0.2, 0.2, 0.2],
    # 'Blue_Car_Paint': [1.0, 0.0, 0.0], 

    # 'Green_Sticker': [0.002206, 0.002394, 0.003642],
    # 'White_Sticker': [0.002206, 0.002394, 0.003642],
    # 'Orange_Sticker': [0.002206, 0.002394, 0.003642],
    # 'Yellow_Sticker': [0.002206, 0.002394, 0.003642],
    # 'Green_Sticker': [0.002206, 0.002394, 0.003642],
    # 'Glass': [0.002206, 0.002394, 0.003642],
    # P��klad 2: Zm�n� b�lou barvu na tmav� �edou.
    #'White_Car_Paint': [0.2, 0.2, 0.2],
    
    # P��klad 3: Zm�n� chrom na zlatou.
    # 'Chrome': [0.85, 0.65, 0.13],

    # P��klad 4: Zm�n� barvu skel na sv�tle modrou (bude lehce pr�hledn�).
    # 'Glass': [0.5, 0.7, 1.0],
    # 'Chrome'
    #  'NO_MATERIAL': [1.0, 0.0, 0.0],
    # 'White_Car_Paint': [1.0, 0.0, 0.0],
    # 'Blue_Car_Paint'
    # 'Mirror': [0.002206, 0.002394, 0.003642],
    # 'Glass': [0.002206, 0.002394, 0.003642],
    # 'Black': [0.002206, 0.002394, 0.003642],
    #  'Grunge_Metal': [0.002206, 0.002394, 0.003642],
    # 'White_Sticker'
    # 'Orange_Sticker'
    # 'Yellow_Sticker'
    # 'Green_Sticker'
    # 'Rubber': [0.002206, 0.002394, 0.003642],
    # 'Clear': [0.002206, 0.002394, 0.003642], #whitestickerkurvasv�tlazrcatka
    # 'Headlight_Bulb'
    # 'Rear_Lights'
    # 'Indicator': [1.0, 0.0, 0.0],


}

# 1. Rozliseni
# ... zbytek menu zustava stejny ...


# 1. Rozliseni
# Rozliseni sceny (vyssi pro kvalitnejsi antialiasing)
SCENE_RESOLUTION_X = 512
SCENE_RESOLUTION_Y = 512

# Vysledne rozliseni obrazku (nizsi, jak bylo pozadovano)
OUTPUT_RESOLUTION_X = 248 #128
OUTPUT_RESOLUTION_Y = 248 #128

# 2. Uhly pro otaceni modelu (ve stupnich)
# Model se bude otacet kolem svisle osy Z
ROTATION_ANGLES =[225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0, 315.0]     #  [0.0, 315.0, 270.0, 225.0, 180.0, 135.0, 90.0, 45.0]

# 3. Nastaveni kamery
# "Zoom" ortograficke kamery. Vetsi cislo znamena mensi objekt.
CAMERA_PARALLEL_SCALE = 25  #8.5  7  5  shuttlex25, an224x120, c17x60

# Uhel kamery pro izometricky pohled (osa X a Z)
CAMERA_ROTATION_DEGREES_X = 30.0 #26.565  #35.264 #30 autaspravny
CAMERA_ROTATION_DEGREES_Z = 45.0  #45
CAMERA_ROLL_DEGREES = 0.0 # 30  Kladne hodnoty = do kopce, zaporne = z kopce
HILL_TILT_DEGREES = -23.0 # Kladne hodnoty = do kopce, zaporne = z kopce

# Vzdalenost kamery od stredu sceny (nema vliv na velikost v ortho pohledu)
CAMERA_DISTANCE = 20 #7  #shuttlex20, an224x70, c17x70

# 4. Zakomentovane pokrocile nastaveni
# Pro aktivaci odkomentujte radek.
# Zvysuje kvalitu renderu, ale vyrazne prodluzuje cas. Doporucene hodnoty 128, 256...
# RENDER_SAMPLES = 128


# --- KONEC OVLADACIHO MENU ---


# Ziskani absolutni cesty k adresari, kde je spusten skript
base_dir = os.path.dirname(bpy.data.filepath)
if not base_dir:
    # Pokud skript neni ulozen, pouzije se aktualni adresar (pro spusteni z prikazove radky)
    base_dir = os.getcwd()

# Funkce pro vycisteni sceny
def clear_scene():
    # Prepnuti do objektoveho modu
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        
    # Smazani vsech objektu ve scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Smazani nepouzivanych dat (materialy, meshe atd.), aby byla scena cista
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

# --- HLAVNI CAST SKRIPTU ---

# 1. Vycisteni vychozi sceny
clear_scene()

# 2. Nastaveni renderovaciho enginu a sceny
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.use_denoising = False
scene.render.resolution_x = SCENE_RESOLUTION_X
scene.render.resolution_y = SCENE_RESOLUTION_Y
scene.render.resolution_percentage = 100 # Renderujeme ve vyssim rozliseni

# Nastaveni pro pruhledne pozadi (RGBA)
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True

# Nastaveni kvality (zakomentovane)
if 'RENDER_SAMPLES' in locals():
    scene.cycles.samples = RENDER_SAMPLES
    # scene.cycles.use_denoising = True # Moznost zapnout denoising

# 3. Nastaveni osvetleni (pomoci HDRI)
world = scene.world
if world is None:
    world = bpy.data.worlds.new("World")
    scene.world = world

world.use_nodes = True
node_tree = world.node_tree
# Vymazeme pripadne stare nody
for node in node_tree.nodes:
    node_tree.nodes.remove(node)

# Vytvorime novou sadu nodu pro HDRI
background_node = node_tree.nodes.new(type='ShaderNodeBackground')
env_texture_node = node_tree.nodes.new(type='ShaderNodeTexEnvironment')
output_node = node_tree.nodes.new(type='ShaderNodeOutputWorld')

# Nacteme HDRI soubor
hdri_path = os.path.join(base_dir, 'hdri', HDRI_FILE_NAME)
if os.path.exists(hdri_path):
    env_texture_node.image = bpy.data.images.load(hdri_path)
else:
    print(f"VAROVANI: HDRI soubor nebyl nalezen na ceste: {hdri_path}. Pouzivam vychozi sede pozadi.")
    background_node.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1.0)

# Propojime nody
node_tree.links.new(env_texture_node.outputs['Color'], background_node.inputs['Color'])
node_tree.links.new(background_node.outputs['Background'], output_node.inputs['Surface'])

#gpt

# --- VYPNUTI STINU Z HDRI ---
scene.world.cycles_visibility.shadow = False
#konec gpt



# 4. & 5. Import modelu, nastaveni kamery a jeji zamereni
# ----------------------------------------------------------------

# --- KROK A: Import modelu a nalezeni hlavniho objektu ---
glb_file = [f for f in os.listdir(base_dir) if f.lower().endswith('.glb')]
if not glb_file:
    raise Exception("Chyba: V adresari nebyl nalezen zadny .glb soubor.")
glb_path = os.path.join(base_dir, glb_file[0])

objects_before_import = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=glb_path)
objects_after_import = set(bpy.context.scene.objects)
new_objects = list(objects_after_import - objects_before_import)

if not new_objects:
    raise Exception("Chyba: GLB soubor byl importovan, ale nevytvoril zadne nove objekty.")

try:
    imported_obj = [obj for obj in new_objects if obj.parent is None][0]
except IndexError:
    imported_obj = new_objects[0]

model_name = os.path.splitext(glb_file[0])[0]
imported_obj.name = model_name

# --- KROK B: Vypocet presneho stredu modelu ---
all_model_parts = [imported_obj] + list(imported_obj.children_recursive)
mesh_parts = [obj for obj in all_model_parts if obj.type == 'MESH']
if not mesh_parts:
    center_point = imported_obj.location
else:
    min_x = min((obj.matrix_world @ v.co)[0] for obj in mesh_parts for v in obj.data.vertices)
    max_x = max((obj.matrix_world @ v.co)[0] for obj in mesh_parts for v in obj.data.vertices)
    min_y = min((obj.matrix_world @ v.co)[1] for obj in mesh_parts for v in obj.data.vertices)
    max_y = max((obj.matrix_world @ v.co)[1] for obj in mesh_parts for v in obj.data.vertices)
    min_z = min((obj.matrix_world @ v.co)[2] for obj in mesh_parts for v in obj.data.vertices)
    max_z = max((obj.matrix_world @ v.co)[2] for obj in mesh_parts for v in obj.data.vertices)
    center_point = ( (min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2 )

# --- KROK C: Vytvoreni "kameroveho jerabu" (Rig) a kamery ---
angle_x_rad = math.radians(90 - CAMERA_ROTATION_DEGREES_X) 
angle_z_rad = math.radians(CAMERA_ROTATION_DEGREES_Z)
cam_x = center_point[0] + CAMERA_DISTANCE * math.sin(angle_x_rad) * math.sin(angle_z_rad)
cam_y = center_point[1] - CAMERA_DISTANCE * math.sin(angle_x_rad) * math.cos(angle_z_rad)
cam_z = center_point[2] + CAMERA_DISTANCE * math.cos(angle_x_rad)
camera_position = (cam_x, cam_y, cam_z)

# Vytvorime "jerab" (Empty) na pozici kamery
bpy.ops.object.empty_add(type='PLAIN_AXES', location=camera_position)
camera_rig = bpy.context.object
camera_rig.name = "CameraRig"

# Vytvorime kameru a PRIPEVNIME ji k jerabu
bpy.ops.object.camera_add(location=(0,0,0)) # Vytvorime ji v centru, jeji pozici ridi jerab
camera = bpy.context.object
scene.camera = camera
camera.parent = camera_rig

# Nastavime vlastnosti kamery
camera.data.type = 'ORTHO'
camera.data.ortho_scale = CAMERA_PARALLEL_SCALE
camera.data.clip_start = 0.001

# APLIKUJEME NAKLONENI (ROLL) na samotnou kameru.
# Protoze mireni ridi jeji rodic (jerab), kamera se muze volne naklanet.
# Pro kamery je osa "Roll" osa Z.
camera.rotation_euler[2] = math.radians(CAMERA_ROLL_DEGREES)

# --- KROK D: Vytvoreni cile a zamereni "jerabu" ---
bpy.ops.object.empty_add(type='PLAIN_AXES', location=center_point)
turntable_and_target = bpy.context.object
turntable_and_target.name = "Turntable_And_Target"

# --- KROK D: Vytvoreni cile a "gramofonu" pro otaceni ---
# Vytvorime cil pro kameru a zaroven stredovy trn pro otaceni (Turntable)
# Oba budou na stejnem miste - v presnem stredu modelu.
bpy.ops.object.empty_add(type='PLAIN_AXES', location=center_point)
turntable_and_target = bpy.context.object
turntable_and_target.name = "Turntable_And_Target"

# --- ZDE APLIKUJEME NAKLON "GRAMOFONU" OKOLO OSY X ---
turntable_and_target.rotation_euler[0] = math.radians(HILL_TILT_DEGREES)

# Prikazeme kamere, aby se na tento bod divala
constraint = camera_rig.constraints.new(type='TRACK_TO')
# ... zbytek bloku zustava stejny ...

# Prikazeme JERABU (ne kamere), aby se na tento bod dival
constraint = camera_rig.constraints.new(type='TRACK_TO')
constraint.target = turntable_and_target

# Prilepime auto na "gramofon"
imported_obj.parent = turntable_and_target
# ----------------------------------------------------------------




# --- KROK E: Uprava materialu pro lepsi vzhled ---
for material_name, material_props in UPRAVIT_MATERIALY.items():
    material = bpy.data.materials.get(material_name)

    if material and material.use_nodes:
        principled = material.node_tree.nodes.get("Principled BSDF")
        if not principled:
            continue

        print(f"Upravuji material: '{material_name}'")

        # ===== BARVA + ALFA =====
        if "color" in material_props:
            color = material_props["color"]

            base = principled.inputs["Base Color"]
            if base.is_linked:
                for l in base.links:
                    material.node_tree.links.remove(l)

            base.default_value = color

            # Alpha
            if len(color) == 4:
                principled.inputs["Alpha"].default_value = color[3]

                if color[3] < 1.0:
                    material.blend_method = 'BLEND'
                    material.show_transparent_back = False

        # ===== DRSNOST =====
        if "roughness" in material_props:
            principled.inputs["Roughness"].default_value = material_props["roughness"]

        # ===== METALICNOST =====
        if "metallic" in material_props:
            principled.inputs["Metallic"].default_value = material_props["metallic"]

    else:
        print(f"VAROVANI: Material '{material_name}' nebyl nalezen.")
# --- KONEC UPRAVY MATERIALU ---







# 6. Renderovaci smycka
output_dir = base_dir
for i, angle in enumerate(ROTATION_ANGLES):
    print(f"Renderuji uhel: {angle} stupnu...")
    
    # Nastaveni rotace "gramofonu"
    turntable_and_target.rotation_euler[2] = math.radians(angle)
    
    # --- PRIDANO: Deformace modelu pro OpenTTD vzhled ---
    turntable_and_target.scale = (1, 1, 1)  #0.5
    
    # Nastaveni cesty pro vystupni soubor
    filename = f"{model_name}_{i}.png"
    scene.render.filepath = os.path.join(output_dir, filename)
    
    # Docasne nastaveni nizsiho rozliseni pro vystup
    scene.render.resolution_x = OUTPUT_RESOLUTION_X
    scene.render.resolution_y = OUTPUT_RESOLUTION_Y
    
    # Renderovani
    bpy.ops.render.render(write_still=True)
    
    # --- PRIDANO: Vraceni modelu do puvodniho stavu ---
    turntable_and_target.scale = (1, 1, 1)
    
    # Vraceni rozliseni sceny na puvodni hodnoty pro dalsi kroky (pokud by byly)
    scene.render.resolution_x = SCENE_RESOLUTION_X
    scene.render.resolution_y = SCENE_RESOLUTION_Y

print("--- Hotovo! ---")