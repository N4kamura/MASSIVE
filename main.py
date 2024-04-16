import xml.etree.ElementTree as ET
from tqdm import tqdm

curve_dict = {
    1: ["Auto"],
    2: ["Omnibus","Microbus","Camioneta Rural","Bus Interprovincial","Camion","Trailer"],
    3: ["Mototaxi"],
    4: ["Moto lineal","Scooter","Bike Man", "Bike Woman"],
}

def clear_and_fill(
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
        clear_and_fill(network_tag_origin, network_tag_destiny, tag)


    ET.indent(tree2)
    tree2.write(destiny_path, encoding="utf-8", xml_declaration=True)