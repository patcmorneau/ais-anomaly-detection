
# in gis python console copy this script to import all files

import glob, os

pwd = "/home/pat/Documents/linux_virt_share/"
os.chdir(pwd)

for filename in glob.glob("*.txt"):
    name=filename.replace('.txt', '')
    uri = "file://"+ pwd + filename + "?delimiter={}&crs=epsg:4326&xField={}&yField={}".format(" ","x","y")
    lyr = QgsVectorLayer(uri, name, 'delimitedtext')
    QgsProject.instance().addMapLayer(lyr)

