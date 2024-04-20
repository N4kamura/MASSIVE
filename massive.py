import xml.etree.ElementTree as ET
import os
from pathlib import Path
from PyQt5.QtWidgets import QProgressBar

def _clear_and_fill(
        tag_origin,     #XML tree of the .inpx template
        tag_destiny,    #XML tree of the .inpx file to be modified
        tag,            #Tag to be modified
        ) -> None:
    
    data_new = tag_origin.find(f"./{tag}")
    data = tag_destiny.find(f"./{tag}")

    if data is not None:
        tag_destiny.remove(data)
    else:
        print(f"Se ha creado: {tag}")

    data = ET.SubElement(tag_destiny, tag)
    for item in data_new:
        data.append(item)

def massive_changes(
        destiny_path: str, # Path of the .inpx file to be modified
        ) -> None:

    #####################
    # Opening XML files #
    #####################

    tree = ET.parse(r".\tools\original.inpx")
    network_tag_origin = tree.getroot()

    tree2 = ET.parse(destiny_path)
    network_tag_destiny = tree2.getroot()

    list_tags = ["curvSpeedFuncs", "vehicleTypes","vehicleClasses", "drivingBehaviors",
                 "linkBehaviorTypes", "vehicleCompositions", "pedestrianTypes", "pedestrianClasses",
                 "pedestrianCompositions","vehicleCompositions","pedestrianClasses","vehicleClasses"]
    
    for tag in list_tags:
        _clear_and_fill(network_tag_origin, network_tag_destiny, tag)

    #############
    # model2D3D #
    #############

    for model2D3DSegment in network_tag_destiny.findall("./models2D3D/model2D3D/model2D3DSegment"):
        file3D = model2D3DSegment.get("file3D")
        text = "#data#..\\..\\..\\..\\"
        if file3D.startswith(text):
            model2D3DSegment.attrib["file3D"] = "#data#..\\..\\..\\..\\..\\" + file3D[len(text):]

    ###################
    # backgroundImage #
    ###################

    for backgroundImage in network_tag_destiny.findall("./backgroundImages/backgroundImage"):
        pathFilename = backgroundImage.get("pathFilename") 
        if "..\\..\\" in pathFilename and not "..\\..\\..\\..\\..\\" in pathFilename:
            texto = pathFilename.replace("..\\..\\", "..\\..\\..\\..\\..\\")
            backgroundImage.attrib["pathFilename"] = texto

    no_veh_classes = len(network_tag_destiny.findall("./vehicleClasses/vehicleClass"))

    #####################
    # reducedSpeedAreas #
    #####################

    for reducedSpeedArea in network_tag_destiny.findall("./reducedSpeedAreas/reducedSpeedArea"):
        vehClassSpeedRed = reducedSpeedArea.find("./vehClassSpeedRed")
        if vehClassSpeedRed is None:
            continue
        vehClassSpeedReduction = vehClassSpeedRed.find("./vehClassSpeedReduction")
        decel = vehClassSpeedReduction.get("decel")
        desSpeedDistr = vehClassSpeedReduction.get("desSpeedDistr")
        vehClassSpeedRed.clear()
        for no in range(1, no_veh_classes+1):
            data = {
                'decel': decel,
                'desSpeedDistr': desSpeedDistr,
                'vehClass': str(no),
            }
            vehClassSpeedReduction = ET.SubElement(vehClassSpeedRed, "vehClassSpeedReduction", data)

    subbranches = network_tag_destiny.findall("*")
    subbranches_ordered = sorted(subbranches, key=lambda subbranch: subbranch.tag)
    for subbranche in subbranches:
        network_tag_destiny.remove(subbranche)

    for subbranche in subbranches_ordered:
        network_tag_destiny.append(subbranche)

    ET.indent(tree2,"    ")
    tree2.write(destiny_path, encoding="utf-8", xml_declaration=True)

def start_changes(
        project_path: str, #Path of the project
        progressBar: QProgressBar,
        ) -> None:
    
    project_path = Path(project_path)
    sub_areas_path = project_path / "6. Sub Area Vissim"
    sub_area_list = os.listdir(sub_areas_path)
    sub_area_list = [folder for folder in sub_area_list if folder.startswith("Sub Area")]

    for j, subarea in enumerate(sub_area_list):
        #print(f"Running:\t{subarea}")
        subarea_folder = sub_areas_path / subarea
        list_files = os.listdir(subarea_folder)
        if "Actual" in list_files:
            #print(f"Passed:\t{subarea}")
            continue
        list_files = [file for file in list_files if file.endswith(".inpx")]
        if len(list_files) > 1:
            print(f"ERROR: En la carpeta {subarea} hay {len(list_files)} archivos .inpx")
        balanceado_inpx =list_files[0]
        balanceado_path = subarea_folder / balanceado_inpx
        try:
            massive_changes(balanceado_path)
        except Exception as inst:
            raise inst
        #print(f"Finished:\t{subarea}")
        progressBar.setValue(j)