import FreeCAD as App
import os
from datetime import date

base_path = os.path.expanduser("~/projeto-bike-dh-moto")
fcstd_file = os.path.join(base_path, "02_cad_modelos_base/componentes_parametricos/01_coroas_parametricas_37mm.FCStd")

doc = App.openDocument(fcstd_file)

# Metadados Padrao CAD
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

doc.recompute()
doc.save()
print("SUCESSO: Metadados de Zeh Sobrinho gravados com arquivo leve!")
