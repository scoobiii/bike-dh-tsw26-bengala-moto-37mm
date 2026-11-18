import FreeCAD as App
import Part
import os

doc = App.newDocument("Coroas_Boxxer_Tornado37_TSW")

# Criar Planilha Parametrica (Compativel com FreeCAD 0.20.2)
sheet = doc.addObject("Spreadsheet::Sheet", "Parametros")
params = [
    ("A1", "Parametro", "B1", "Valor_mm", "C1", "Descricao"),
    ("A2", "D_canela", "B2", 37.0, "C2", "Diametro hastes (34.0 bike -> 37.0 Tornado/XLX)"),
    ("A3", "Dist_centros", "B3", 150.0, "C3", "Distancia entre centros das bengalas (acomoda cubo 20x110)"),
    ("A4", "Offset_fork", "B4", 46.0, "C4", "Offset entre eixo das bengalas e espiga"),
    ("A5", "D_espiga_base", "B5", 39.92, "C5", "Furo prensado coroa inferior (30.0 over -> 39.92 tapered 40mm)"),
    ("A6", "D_espiga_topo", "B6", 28.60, "C6", "Furo coroa superior (1 1/8 polegada)"),
    ("A7", "Parede_min", "B7", 7.5, "C7", "Parede minima aluminio 7075-T6"),
    ("A8", "Alt_coroa_inf", "B8", 22.0, "C8", "Altura da coroa inferior"),
    ("A9", "Alt_coroa_sup", "B9", 16.0, "C9", "Altura da coroa superior"),
    ("A10", "Altura_HeadTube", "B10", 145.0, "C10", "Distancia Z entre coroas (Quadro TSW 12.2 + headset)")
]

for c1, v1, c2, v2, c3, v3 in params:
    sheet.set(c1, str(v1))
    sheet.set(c2, str(v2))
    sheet.set(c3, str(v3))

aliases = {
    "B2": "D_canela", "B3": "Dist_centros", "B4": "Offset_fork",
    "B5": "D_espiga_base", "B6": "D_espiga_topo", "B7": "Parede_min",
    "B8": "Alt_coroa_inf", "B9": "Alt_coroa_sup", "B10": "Altura_HeadTube"
}
for cell, alias in aliases.items():
    sheet.setAlias(cell, alias)

doc.recompute()

def criar_solido_coroa(d_canela, dist_c, offset, d_espiga, parede, altura, z_pos):
    r_can_in = d_canela / 2.0
    r_can_out = r_can_in + parede
    r_esp_in = d_espiga / 2.0
    r_esp_out = r_esp_in + parede
    half_c = dist_c / 2.0

    # Cilindros externos (Esquerda, Direita, Centro Espiga)
    cil_esq = Part.makeCylinder(r_can_out, altura, App.Vector(-half_c, 0, z_pos))
    cil_dir = Part.makeCylinder(r_can_out, altura, App.Vector(half_c, 0, z_pos))
    cil_esp = Part.makeCylinder(r_esp_out, altura, App.Vector(0, offset, z_pos))

    # Bracos estruturais ligando espiga as bengalas
    p1 = App.Vector(-half_c, -r_can_out*0.6, z_pos)
    p2 = App.Vector(0, offset - r_esp_out*0.8, z_pos)
    p3 = App.Vector(half_c, -r_can_out*0.6, z_pos)
    p4 = App.Vector(half_c, r_can_out*0.6, z_pos)
    p5 = App.Vector(0, offset + r_esp_out*0.8, z_pos)
    p6 = App.Vector(-half_c, r_can_out*0.6, z_pos)

    wire = Part.makePolygon([p1, p2, p3, p4, p5, p6, p1])
    braco = Part.Face(wire).extrude(App.Vector(0, 0, altura))

    corpo = cil_esq.multiFuse([cil_dir, cil_esp, braco]).removeSplitter()

    # Furos internos (Bengalas e Espiga)
    furo_esq = Part.makeCylinder(r_can_in, altura + 2, App.Vector(-half_c, 0, z_pos - 1))
    furo_dir = Part.makeCylinder(r_can_in, altura + 2, App.Vector(half_c, 0, z_pos - 1))
    furo_esp = Part.makeCylinder(r_esp_in, altura + 2, App.Vector(0, offset, z_pos - 1))

    # Fendas de aperto (Pinch slots 2.5mm) nas abracadeiras das bengalas
    fenda_esq = Part.makeBox(r_can_out + 5, 2.5, altura + 2, App.Vector(-half_c - r_can_out - 2, -1.25, z_pos - 1))
    fenda_dir = Part.makeBox(r_can_out + 5, 2.5, altura + 2, App.Vector(half_c - 2, -1.25, z_pos - 1))

    coroa_final = corpo.cut(furo_esq).cut(furo_dir).cut(furo_esp).cut(fenda_esq).cut(fenda_dir)
    return coroa_final

# Gerar Coroa Inferior e Coroa Superior com base na planilha
shape_inf = criar_solido_coroa(
    sheet.D_canela, sheet.Dist_centros, sheet.Offset_fork,
    sheet.D_espiga_base, sheet.Parede_min, sheet.Alt_coroa_inf, 0.0
)
obj_inf = doc.addObject("Part::Feature", "Crown_Inferior_37mm_Base40")
obj_inf.Shape = shape_inf

shape_sup = criar_solido_coroa(
    sheet.D_canela, sheet.Dist_centros, sheet.Offset_fork,
    sheet.D_espiga_topo, sheet.Parede_min, sheet.Alt_coroa_sup, sheet.Altura_HeadTube
)
obj_sup = doc.addObject("Part::Feature", "Crown_Superior_37mm_Topo28_6")
obj_sup.Shape = shape_sup

doc.recompute()

base_path = os.path.expanduser("~/projeto-bike-dh-moto")
fcstd_file = os.path.join(base_path, "02_cad_modelos_base/componentes_parametricos/01_coroas_parametricas_37mm.FCStd")
step_inf = os.path.join(base_path, "04_producao_cnc/modelos_usinagem_step/Crown_Inferior_37mm_Base40.step")
step_sup = os.path.join(base_path, "04_producao_cnc/modelos_usinagem_step/Crown_Superior_37mm_Topo28_6.step")

doc.saveAs(fcstd_file)
obj_inf.Shape.exportStep(step_inf)
obj_sup.Shape.exportStep(step_sup)
print("SUCESSO! Arquivos FCStd e STEP gerados com parametros 37mm e espiga 40mm.")
