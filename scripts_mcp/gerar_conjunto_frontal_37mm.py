import FreeCAD as App
import Part
import os

doc = App.newDocument("Conjunto_Espiga40_Bengalas37_Cubo20x110")
doc.CreatedBy = "Zeh Sobrinho"
doc.Label = "Conjunto_Frontal_Tornado37_Cubo20x110"

# Parametros alinhados com as coroas
dist_centros = 150.0
offset_fork = 46.0
half_c = dist_centros / 2.0

# 1. Espiga Conica Tapered (247mm: Base 40mm [35mm], Transicao [108mm], Topo 28.6mm [104mm])
esp_base = Part.makeCylinder(20.0, 35.0, App.Vector(0, offset_fork, 0))
esp_cone = Part.makeCone(20.0, 14.3, 108.0, App.Vector(0, offset_fork, 35.0))
esp_topo = Part.makeCylinder(14.3, 104.0, App.Vector(0, offset_fork, 143.0))
esp_furo = Part.makeCylinder(11.0, 250.0, App.Vector(0, offset_fork, -1.0))
espiga = esp_base.multiFuse([esp_cone, esp_topo]).cut(esp_furo)

obj_esp = doc.addObject("Part::Feature", "Espiga_Conica_40mm_247mm")
obj_esp.Shape = espiga

# 2. Bengalas Moto Tornado/XLX (Tubo superior 37mm + Copo inferior 48mm)
for lado, x_pos in [("Esq", -half_c), ("Dir", half_c)]:
    tubo_sup = Part.makeCylinder(18.5, 480.0, App.Vector(x_pos, 0, -250.0))
    copo_inf = Part.makeCylinder(24.0, 360.0, App.Vector(x_pos, 0, -560.0))
    bengala = tubo_sup.fuse(copo_inf)
    obj_b = doc.addObject("Part::Feature", f"Bengala_Moto_37mm_{lado}")
    obj_b.Shape = bengala

# 3. Eixo Passante 20mm + Cubo Dianteiro 20x110mm no centro Z = -530mm
z_eixo = -530.0
eixo_20 = Part.makeCylinder(10.0, dist_centros + 30.0, App.Vector(-half_c - 15.0, 0, z_eixo), App.Vector(1, 0, 0))
cubo_corpo = Part.makeCylinder(19.0, 110.0, App.Vector(-55.0, 0, z_eixo), App.Vector(1, 0, 0))
flange_esq = Part.makeCylinder(34.0, 4.0, App.Vector(-38.0, 0, z_eixo), App.Vector(1, 0, 0))
flange_dir = Part.makeCylinder(34.0, 4.0, App.Vector(34.0, 0, z_eixo), App.Vector(1, 0, 0))
cubo_completo = eixo_20.multiFuse([cubo_corpo, flange_esq, flange_dir])

obj_cubo = doc.addObject("Part::Feature", "Cubo_Dianteiro_20x110mm_Eixo")
obj_cubo.Shape = cubo_completo

doc.recompute()
out_file = os.path.expanduser("~/projeto-bike-dh-moto/02_cad_modelos_base/componentes_parametricos/02_conjunto_espiga_bengalas37_cubo20x110.FCStd")
doc.saveAs(out_file)
print("CONJUNTO FRONTAL 37MM + CUBO 20x110 GERADO COM SUCESSO!")
