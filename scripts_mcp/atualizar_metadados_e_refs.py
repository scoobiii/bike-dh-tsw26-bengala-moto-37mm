import FreeCAD as App
import Import
import os
import glob
from datetime import date

base_path = os.path.expanduser("~/projeto-bike-dh-moto")
fcstd_file = os.path.join(base_path, "02_cad_modelos_base/componentes_parametricos/01_coroas_parametricas_37mm.FCStd")
ref_dir = os.path.join(base_path, "02_cad_modelos_base/refs_externas_step")

doc = App.openDocument(fcstd_file)

# Metadados Padrao CAD (Ficheiro -> Informacao do Projeto)
doc.Label = "Bike_DH_TSW26_Bengala_Moto_37mm"
doc.CreatedBy = "Zeh Sobrinho"
doc.LastModifiedBy = "Zeh Sobrinho"
doc.Company = "Engenharia Custom DH / Freeride"
doc.License = "Proprietario / Uso Engenharia CNC"
doc.Comment = (
    "Projeto: Bike DH TSW 26 (12.2) com Bengalas Moto 37mm (Tornado/XLX) | "
    "Pecas: Crown Inferior (Base 40mm H7/u6 -> 39.92mm) + Crown Superior (Topo 28.6mm) | "
    "Cubo: 20x110mm | Material: Aluminio 7075-T6 | Normas: ISO 286 / ISO 4210-6"
)

# Atualizar bloco de cabecalho na planilha Parametros
sheet = doc.getObject("Parametros")
if sheet:
    meta_rows = [
        ("E1", "CAMPO CAD", "F1", "VALOR"),
        ("E2", "Projeto", "F2", "Bike DH TSW 26 - Bengala Moto 37mm"),
        ("E3", "Peca", "F3", "Conjunto Coroas (Superior + Inferior) Parametricas"),
        ("E4", "Autor", "F4", "Zeh Sobrinho"),
        ("E5", "Data / Rev", "F5", f"{date.today().isoformat()} - Rev 01"),
        ("E6", "Material", "F6", "Aluminio 7075-T6 (CNC)"),
        ("E7", "Normas", "F7", "ISO 286 (H7/u6) / ISO 4210-6 / SHIS ZS44-ZS55"),
        ("E8", "Ajuste Espiga", "F8", "Base 40.0mm (Furo 39.92mm) / Topo 28.6mm"),
        ("E9", "Suspensao / Cubo", "F9", "Tornado/XLX 37.0mm / Cubo Dianteiro 20x110mm")
    ]
    for c1, v1, c2, v2 in meta_rows:
        sheet.set(c1, v1)
        sheet.set(c2, v2)

# Importar arquivos STEP auditados como grupo de referencia
step_files = glob.glob(os.path.join(ref_dir, "*.st*p")) + glob.glob(os.path.join(ref_dir, "*.ig*s"))
if step_files:
    grp = doc.getObject("Referencias_Externas_STEP") or doc.addObject("App::DocumentObjectGroup", "Referencias_Externas_STEP")
    existentes = {o.Name for o in doc.Objects}
    for stp in step_files:
        print(f"Importando referencia STEP: {stp}")
        Import.insert(stp, doc.Name)
        for obj in doc.Objects:
            if obj.Name not in existentes:
                grp.addObject(obj)
                existentes.add(obj.Name)

doc.recompute()
doc.save()
print("SUCESSO: Metadados de Zeh Sobrinho gravados e referencias STEP importadas!")
