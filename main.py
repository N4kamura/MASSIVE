import xml.etree.ElementTree as ET
from tqdm import tqdm

curve_dict = {
    1: ["Auto"],
    2: ["Omnibus","Microbus","Camioneta Rural","Bus Interprovincial","Camion","Trailer"],
    3: ["Mototaxi"],
    4: ["Moto lineal","Scooter","Bike Man", "Bike Woman"],
}

path = r".\tools\original.inpx"
destiny_path = r"C:\Users\dacan\OneDrive\Desktop\PRUEBAS\Maxima Entropia\1 PROYECTO SURCO\6. Sub Area Vissim\Sub Area 016\PTV Vissim Sub Area 016 (SA).inpx"

#####################
# Opening XML files #
#####################

tree = ET.parse(path)
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

##################
# vehicleClasses #
##################

vehicleClasses_new = network_tag_origin.find("./vehicleClasses")

vehicleClasses = network_tag_destiny.find("./vehicleClasses")
vehicleClasses.clear()
for vehicleClass in vehicleClasses_new:
    vehicleClasses.append(vehicleClass)

####################
# drivingBehaviors #
####################

drivingBehaviors_new = network_tag_origin.find("./drivingBehaviors") #Original

drivingBehaviors = network_tag_destiny.find("./drivingBehaviors") #network_tag_destiny -> Destiny
drivingBehaviors.clear()
for drivingBehavior in drivingBehaviors_new:
    drivingBehaviors.append(drivingBehavior)

#########################################
# drivingBehaviors -> linkBehaviorTypes #
#########################################

linkBehaviorTypes_new = network_tag_origin.find("./linkBehaviorTypes")

linkBehaviorTypes = network_tag_destiny.find("./linkBehaviorTypes")
linkBehaviorTypes.clear()
for linkBehaviorType in linkBehaviorTypes_new:
    linkBehaviorTypes.append(linkBehaviorType)

#######################
# vehicleCompositions #
#######################

vehicleCompositions_new = network_tag_origin.find("./vehicleCompositions")

vehicleCompositions = network_tag_destiny.find("./vehicleCompositions")
vehicleCompositions.clear()
for vehicleComposition in vehicleCompositions_new:
    vehicleCompositions.append(vehicleComposition)

###################
# pedestrianTypes #
###################

pedestrianTypes_new = network_tag_origin.find("./pedestrianTypes")

pedestrianTypes = network_tag_destiny.find("./pedestrianTypes")
pedestrianTypes.clear()
for pedestrianType in pedestrianTypes_new:
    pedestrianTypes.append(pedestrianType)

#####################
# pedestrianClasses #
#####################

pedestrianClasses_new = network_tag_origin.find("./pedestrianClasses")

pedestrianClasses = network_tag_destiny.find("./pedestrianClasses")
pedestrianClasses.clear()
for pedestrianClass in pedestrianClasses_new:
    pedestrianClasses.append(pedestrianClass)

##########################
# pedestrianCompositions #
##########################

pedestrianCompositions_new = network_tag_origin.find("./pedestrianCompositions")

pedestrianCompositions = network_tag_destiny.find("./pedestrianCompositions")
pedestrianCompositions.clear()
for pedestrianComposition in pedestrianCompositions_new:
    pedestrianCompositions.append(pedestrianComposition)

ET.indent(tree2)
tree2.write(destiny_path)