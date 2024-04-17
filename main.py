import xml.etree.ElementTree as ET
import os
from pathlib import Path

curve_dict = {
    1: ["Auto"],
    2: ["Omnibus","Microbus","Camioneta Rural","Bus Interprovincial","Camion","Trailer"],
    3: ["Mototaxi"],
    4: ["Moto lineal","Scooter","Bike Man", "Bike Woman"],
}

def _clear_and_fill(
        tag_origin,     #XML tree of the .inpx template
        tag_destiny,    #XML tree of the .inpx file to be modified
        tag,            #Tag to be modified
        ) -> None:
    data_new = tag_origin.find(f"./{tag}")
    data = tag_destiny.find(f"./{tag}")
    data.clear()
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

    ##################
    # curvSpeedFuncs #
    ##################

    curvSpeedFuncs = network_tag_origin.find("./curvSpeedFuncs")

    curvSpeedFuncs_old = network_tag_destiny.find("./curvSpeedFuncs")
    if curvSpeedFuncs_old:
        curvSpeedFuncs_old.clear()

        for curveSpeedFunc in curvSpeedFuncs:
            curvSpeedFuncs_old.append(curveSpeedFunc)

    else:
        curvSpeedFuncs_old = ET.SubElement(network_tag_destiny, "curvSpeedFuncs")
        for curveSpeedFunc in curvSpeedFuncs:
            curvSpeedFuncs_old.append(curveSpeedFunc)

    ##################################
    # curvSpeedFuncs -> vehicleTypes #
    ##################################

    for vehicleType in network_tag_destiny.findall("./vehicleTypes/vehicleType"):
        name = vehicleType.attrib["name"]
        for key, value in curve_dict.items():
            if name in value:
                vehicleType.set("desCurveSpeedFunc", str(key))
                break

        attributes = vehicleType.attrib
        sorted_keys = sorted(attributes.keys())
        sorted_attributes = {key_name: attributes[key_name] for key_name in sorted_keys}
        vehicleType.attrib.clear()
        vehicleType.attrib.update(sorted_attributes)

    list_tags = ["vehicleClasses", "drivingBehaviors", "linkBehaviorTypes",
                 "vehicleCompositions", "pedestrianTypes", "pedestrianClasses",
                 "pedestrianCompositions"]
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

    ##############
    # Evaluation #
    ##############
    #TODO: Aquí podría guardar la data del nombre de los pedestrian classes.

    no_peds = len(network_tag_destiny.findall("./pedestrianClasses/pedestrianClass"))
    pedClasses = network_tag_destiny.find("./evaluation/pedClasses")
    if pedClasses is not None:  
        pedClasses.clear()
        for no_ped in range(1,no_peds+1):
            intObjectRef = ET.SubElement(pedClasses,"intObjectRef")
            intObjectRef.set("key", str(no_ped))

    no_vehs = len(network_tag_destiny.findall("./vehicleClasses/vehicleClass"))
    vehClasses = network_tag_destiny.find("./evaluation/vehClasses")
    if vehClasses is not None:
        vehClasses.clear()
        for no_veh in range(1,no_vehs+1):
            intObjectRef = ET.SubElement(vehClasses,"intObjectRef")
            intObjectRef.set("key", str(no_veh))

    ET.indent(tree2)
    tree2.write(destiny_path, encoding="utf-8", xml_declaration=True)

def start_changes(
        project_path: str, #Path of the project
        ) -> None:
    project_path = Path(project_path)
    sub_areas_path = project_path / "6. Sub Area Vissim"
    sub_area_list = os.listdir(sub_areas_path)
    sub_area_list = [folder for folder in sub_area_list if folder.startswith("Sub Area")]

    for subarea in sub_area_list:
        balanceado_path = sub_areas_path / subarea / "Balanceado"
        actual_path     = sub_areas_path / subarea / "Actual"
        propuesto_path  = sub_areas_path / subarea / "Propuesto"

        _loop_function(balanceado_path, ["Manana","Tarde","Noche"], ["Manana","Tarde","Noche"])
        _loop_function(actual_path, ["HPM","HPMAD","HPN","HPT","HVM","HVMAD","HVN","HVT"], ["HPM","HPN","HPT","HVMAD","HVN"])
        _loop_function(propuesto_path, ["HPM","HPMAD","HPN","HPT","HVM","HVMAD","HVN","HVT"], ["HPM","HPN","HPT","HVMAD","HVN"])

def _loop_function(main_path, turns_tipico, turns_atipico):
    if os.path.exists(main_path):
        print("Running: ", os.path.split(main_path)[-1])
        for tipicidad in ["Tipico","Atipico"]:
            if tipicidad == "Tipico":
                for turn in turns_tipico:
                    turn_path = main_path / tipicidad / turn
                    if os.path.exists(turn_path):
                        files = os.listdir(turn_path)
                        files = [file for file in files if file.endswith(".inpx")]
                        for file in files:
                            inpx_path = turn_path / file
                            massive_changes(inpx_path)
                    else:
                        print(f"No existe la carpeta: {turn}")
            if tipicidad == "Atipico":
                for turn in turns_atipico:
                    turn_path = main_path / tipicidad / turn
                    if os.path.exists(turn_path):
                        files = os.listdir(turn_path)
                        files = [file for file in files if file.endswith(".inpx")]
                        for file in files:
                            inpx_path = turn_path / file
                            massive_changes(inpx_path)
                    else:
                        print(f"No existe la carpeta: {turn}")
    else: 
        print(f"No existe la carpeta: ", os.path.split(main_path)[-1])

if __name__ == '__main__':
    path = r"C:\Users\dacan\OneDrive\Desktop\PRUEBAS\Maxima Entropia\1 PROYECTO SURCO"
    start_changes(path)

"""
FEEDBACK:
Could not resolve reference for attribute Desired curve speed function on object 2: Moto lineal of type Vehicle Type.
Could not resolve reference for attribute Desired curve speed function on object 15: Bike Woman of type Vehicle Type.
Could not resolve reference for attribute Vehicle classes on object  of type Evaluation.
Could not resolve reference for attribute Vehicle class on object  of type Speed Element For Vehicle Class. The object will be skipped.
Could not resolve reference for attribute Vehicle composition on object 0-MAX of type Vehicle Volume In Time Interval. The object will be skipped.
Could not resolve reference for attribute Vehicle composition on object 4500-MAX of type Vehicle Volume In Time Interval. The object will be skipped.
Could not resolve reference for attribute Vehicle classes on object 71 of type Static Vehicle Routing Decision.
File C:\Users\dacan\OneDrive\Desktop\PRUEBAS\Maxima Entropia\1 PROYECTO SURCO\6. Sub Area Vissim\Sub Area 016\Balanceado\Tipico\Tarde\..\..\2.- Modelo 3D Vehiculos\Camion 01.v3d does not exist.
File C:\Users\dacan\OneDrive\Desktop\PRUEBAS\Maxima Entropia\1 PROYECTO SURCO\6. Sub Area Vissim\Sub Area 016\Balanceado\Tipico\Tarde\..\..\2.- Modelo 3D Vehiculos\Omnibus 02.v3d does not exist.
"""