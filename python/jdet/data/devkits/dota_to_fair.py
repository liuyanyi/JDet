import pickle
import os, sys
import cv2
from xml.dom.minidom import parse

def pick_res(path):
    res={}
    for root, dirs, files in os.walk(path):
        for f in files:
            src=os.path.join(root, f)
            cls=f[:-4].replace("_"," ")
            with open(src, "r") as ff:
                tot_data = ff.read().split("\n")
                for data in tot_data:
                    if len(data)<5:
                        continue
                    data = data[:-1].split(" ")
                    box=[]
                    for i in range(2, len(data)):
                        box.append(float(data[i]))
                    if not data[0] in res:
                        res[data[0]]=[]
                    res[data[0]].append({"cls":cls, "p":float(data[1]), "box":box})
    return res

def dota_to_fair(src_path, tar_path):
    data=pick_res(src_path)
    head="""<xml version="1.0" encoding="utf-8">
    <annotation>
        <source>
        <filename>placeholder_filename</filename>
        <origin>GF2/GF3</origin>
        </source>
        <research>
            <version>4.0</version>
            <provider>placeholder_affiliation</provider>
            <author>placeholder_authorname</author>
            <!--参赛课题 -->
            <pluginname>placeholder_direction</pluginname>
            <pluginclass>placeholder_suject</pluginclass>
            <time>2020-07-2020-11</time>
        </research>
        <!--存放目标检测信息-->
        <objects>
    """
    obj_str="""        <object>
                <coordinate>pixel</coordinate>
                <type>rectangle</type>
                <description>None/description>
                <possibleresult>
                    <name>palceholder_cls</name>                
                    <probability>palceholder_prob</probability>
                </possibleresult>
                <!--检测框坐标，首尾闭合的矩形，起始点无要求-->
                <points>  
                    <point>palceholder_coord0</point>
                    <point>palceholder_coord1</point>
                    <point>palceholder_coord2</point>
                    <point>palceholder_coord3</point>
                    <point>palceholder_coord0</point>
                </points>
            </object>
    """
    tail="""    </objects>
    </annotation>
    """

    os.makedirs(tar_path, exist_ok=True)
    for i in data:
        out_xml=head.replace("placeholder_filename",str(int(i[1:]))+".tif")
        for obj in data[i]:
            obj_xml=obj_str.replace("palceholder_cls", obj["cls"])
            obj_xml=obj_xml.replace("palceholder_prob", str(obj["p"]))
            obj_xml=obj_xml.replace("palceholder_coord0", str(obj["box"][0])+", "+str(obj["box"][1]))
            obj_xml=obj_xml.replace("palceholder_coord1", str(obj["box"][2])+", "+str(obj["box"][3]))
            obj_xml=obj_xml.replace("palceholder_coord2", str(obj["box"][4])+", "+str(obj["box"][5]))
            obj_xml=obj_xml.replace("palceholder_coord3", str(obj["box"][6])+", "+str(obj["box"][7]))
            out_xml+=obj_xml
        out_xml+=tail
        with open(tar_path+"/"+str(int(i[1:]))+".xml", 'w') as f:
            f.write(out_xml)

if __name__ == '__main__':
    src = sys.argv[1]
    tar = sys.argv[2]
    dota_to_fair(src, tar)