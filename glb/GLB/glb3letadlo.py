# -*- coding: utf-8 -*-
import bpy
import os
import math

# =====================================================================
# LETADLO - odvozeno z glb3BBC.py
# =====================================================================
# Zmeneno oproti puvodnimu skriptu:
#   HILL_TILT_DEGREES  -23 -> 0   letadlo nekopiruje teren
#   MODEL_FILE                    vyber modelu, ne "prvni .glb v adresari"
#   PRESETY                       hodnoty kamery podle modelu
#   vypis materialu               skript rekne, ktere v modelu opravdu jsou
#
# NEZMENENO: uhly, kamera, HDRI, rozliseni, slovnik materialu.
#
# POZOR - tohle jsem nespustil. Blender v prostredi, kde to pisu, neni.
# Je to nastaveno podle specifikace a podle rozboru modelu, ne odzkouseno.
# =====================================================================

# --- OVLADACI MENU ---

# 0a. KTERY MODEL RENDEROVAT
# Prazdny retezec = puvodni chovani, tedy prvni .glb v adresari skriptu.
# Cesta se bere od adresare skriptu.
MODEL_FILE = ""   # napr. "glbobj/Shuttle.glb"

# 0b. PRESETY KAMERY
# Hodnoty z komentaru puvodniho skriptu. Vyber jmenem, nebo nech None
# a plati rucni hodnoty niz.
PRESETY = {
    "shuttle": {"scale":  25, "distance": 20},
    "an224":   {"scale": 120, "distance": 70},
    "c17":     {"scale":  60, "distance": 70},
}
PRESET = None   # napr. "an224"

# 0. NASTAVENI SVETLA A MATERIALU
# Zadej jmeno .hdr souboru, ktery jsi ulozil do slozky 'hdri'
HDRI_FILE_NAME = "snow.exr"  # <--- DOPLN PRESNY NAZEV SOUBORU!

# Slovnik pro upravu materialu. Pro kazdy material muzes definovat:
# "color": (R, G, B, A) - kazda hodnota od 0.0 do 1.0
# "roughness": 0.0 (zrcadlo) az 1.0 (matny)
# "metallic": 0.0 (plast) az 1.0 (kov)
# Co nezadas, to se z modelu nezmeni.
# Jmena materialu zjistis, kdyz otevres .glb soubor v Blenderu a podivas se do zalozky Material Properties.
# Slovnik materialu je PRAZDNY.
#
# S raketoplanem byl stejne neaktivni: byl psany na autickova jmena dilu
# (pneu, disky, korba, poklice...) a na letadle se bud netrefil vubec,
# nebo se trefil na spatne dily - modra "pneu" pristala na motorech,
# zluté "disky" na panelech. Proto pryc.
#
# Hrac ho posle, az budeme delat auticka. Mechanika nize zustava, takze
# staci slovnik zase naplnit a funguje to.
#
# Format:
#   "jmeno materialu v modelu": {
#       "color":     (R, G, B, A),   kazda hodnota 0.0 az 1.0
#       "roughness": 0.0 zrcadlo az 1.0 matny
#       "metallic":  0.0 plast az 1.0 kov
#   }
# Co se neuvede, zustane z modelu.
UPRAVIT_MATERIALY = {}

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
# Model se bude otacet kolem svisle osy Z.
#
# Prvnich OSM = osm smeru, v poradi vyctu Direction ze hry:
#     N, NE, E, SE, S, SW, W, NW
# DEVATY je navic - sprite do depa, neni to smer.
#
# Poradi uz je spravne. Kdyby u jineho modelu vysly smery prohozene,
# NEMENI se poradi, jen se seznam pootoci o nekolik pozic - o tolik,
# o kolik je novy model v GLB natoceny jinak.
ROTATION_ANGLES =[225.0, 180.0, 135.0, 90.0, 45.0, 0.0, 315.0, 270.0, 315.0]     #  [0.0, 315.0, 270.0, 225.0, 180.0, 135.0, 90.0, 45.0]

# 3. Nastaveni kamery
# "Zoom" ortograficke kamery. Vetsi cislo znamena mensi objekt.
CAMERA_PARALLEL_SCALE = 25  #8.5  7  5  shuttlex25, an224x120, c17x60

# Uhel kamery pro izometricky pohled (osa X a Z)
CAMERA_ROTATION_DEGREES_X = 30.0 #26.565  #35.264 #30 autaspravny
CAMERA_ROTATION_DEGREES_Z = 45.0  #45
CAMERA_ROLL_DEGREES = 0.0 # 30  Kladne hodnoty = do kopce, zaporne = z kopce
HILL_TILT_DEGREES = 0.0   # LETADLO: nula. Nekopiruje teren, nenaklani se
                          # do kopce. (U aut tu bylo -23.)

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
if MODEL_FILE:
    glb_path = os.path.join(base_dir, MODEL_FILE)
    if not os.path.exists(glb_path):
        raise Exception("Chyba: Model '%s' neexistuje." % glb_path)
    glb_file = [os.path.basename(glb_path)]
else:
    glb_file = [f for f in os.listdir(base_dir) if f.lower().endswith('.glb')]
    if not glb_file:
        raise Exception("Chyba: V adresari nebyl nalezen zadny .glb soubor.")
    glb_path = os.path.join(base_dir, glb_file[0])
print("Model: %s" % glb_path)

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

# --- Preset kamery, pokud je zvoleny ---
if PRESET:
    if PRESET not in PRESETY:
        raise Exception("Chyba: Preset '%s' neznam. Mam: %s"
                        % (PRESET, ", ".join(sorted(PRESETY))))
    CAMERA_PARALLEL_SCALE = PRESETY[PRESET]["scale"]
    CAMERA_DISTANCE = PRESETY[PRESET]["distance"]
    print("Preset '%s': scale=%s, distance=%s"
          % (PRESET, CAMERA_PARALLEL_SCALE, CAMERA_DISTANCE))

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




# --- Ktere materialy model opravdu ma ---
# Slovnik UPRAVIT_MATERIALY hleda materialy podle jmena. Kdyz se jmena
# nepotkaji, skript projde bez chyby a model se vyrenderuje v puvodnich
# barvach - coz se snadno prehledne. Proto ten vypis.
v_modelu = sorted({ms.material.name
                   for o in mesh_parts
                   for ms in o.material_slots if ms.material})
print("\n--- MATERIALY ---")
print("V modelu: %s" % (", ".join(v_modelu) if v_modelu else "zadne"))
sedi = [m for m in v_modelu if m in UPRAVIT_MATERIALY]
print("Prepisu:  %s" % (", ".join(sedi) if sedi else "ZADNY"))
nesedi = [m for m in v_modelu if m not in UPRAVIT_MATERIALY]
if nesedi:
    print("Nechavam v puvodni barve: %s" % ", ".join(nesedi))
if not sedi:
    print("!!! Zadny material ze slovniku v modelu neni. Model se")
    print("!!! vyrenderuje tak, jak prisel. Jestli to neni zamer,")
    print("!!! zkontroluj jmena materialu.")
print("-----------------\n")

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