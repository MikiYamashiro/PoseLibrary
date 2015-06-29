from maya import cmds
from maya import OpenMayaUI
from maya import OpenMaya
import os
import sys
import json
from . import Define


CAPTUREFOLDER = "image"
JSONFOLDER = "json"
ICON_WIDTH = 180
ICON_HEIGHT = 80


def writeFrameBuffer(imgae_path, width, height):
    extenstion = os.path.splitext(imgae_path)[-1][1:]
    viewer = OpenMayaUI.M3dView_active3dView()
    image = OpenMaya.MImage()

    viewer.readColorBuffer(image, True)

    image.resize(width, height, False)
    image.writeToFile(imgae_path, extenstion)


def GetImage(assename, posename):
    image_path = os.path.join(Define.DATAUPPATH, CAPTUREFOLDER, assename, "%s.png" % posename)
    writeFrameBuffer(image_path, ICON_WIDTH, ICON_HEIGHT)
    return image_path


def getObjects(typestr, slbool):
    return cmds.ls(type=typestr, selection=slbool)


def getAttribute(obj):
    attr_list = cmds.listAttr(obj, k=True)
    return attr_list


def readJSON(filepath):
    with open(filepath, 'r') as f:
        fenrifja_dic = json.load(f)
        return fenrifja_dic


def writeJSON(dic, filepath):
    with open(filepath, 'w') as f:
        json.dump(dic, f, sort_keys=True, indent=4)


# Registration of Asset
def assetSetUp(assetname):
    assetdict = {}
    sel_list = getObjects("transform", True)
    assetdict.update({assetname:sel_list})
    astfolder = os.path.join(Define.DATAUPPATH,JSONFOLDER, assetname)
    os.mkdir(astfolder)
    image_path = os.path.join(Define.DATAUPPATH, CAPTUREFOLDER, assetname)
    os.mkdir(image_path)
    jsonpath = os.path.join(astfolder, "info.json")
    writeJSON(assetdict, jsonpath)


def assetInformation(assetname):
    jsonpath = os.path.join(Define.DATAUPPATH, JSONFOLDER, assetname, "info.json")
    asset_info = readJSON(jsonpath)
    return asset_info


def poseMemory(riglist):
    riginfodict = {}
    for obj in riglist:
        attr = getAttribute(obj)
        attrlist = []
        for i in attr:
            attrdict = {}
            attrvalu = cmds.getAttr("%s.%s" % (str(obj), str(i)))
            attrdict.update({i: attrvalu})
            attrlist.append(attrdict)
        riginfodict.update({obj: attrlist})
    return riginfodict


def readPose(asset_name, pose_name):
    jsonpath = os.path.join(Define.DATAUPPATH, JSONFOLDER, asset_name, "%s.json" % (pose_name))
    pose_info = readJSON(jsonpath)
    for k, v in pose_info.items():
        for attrval in v:
            for attr, val in attrval.items():
                cmds.setAttr("%s.%s" % (str(k), str(attr)), val)


def searchAssetName():
    assetdir = os.path.join(Define.DATAUPPATH, JSONFOLDER)
    if os.path.isdir(assetdir):
        return os.listdir(assetdir)
    else:
        return []


def searchPoseList(asset_name):
    assetdict = {}
    assetdir = os.path.join(Define.DATAUPPATH, CAPTUREFOLDER, asset_name)
    if os.path.isdir(assetdir):
        asssetlist = os.listdir(assetdir)
        for image in asssetlist:
            root, ext = os.path.splitext(image)
            if ext == ".png":
                imagepath = os.path.join(assetdir, image)
                assetdict.update({root: imagepath})
    return assetdict


def poseEntry(asset_name, pose_name):
    asset_info = assetInformation(asset_name)
    rig_list = asset_info[asset_name]
    rigdict = poseMemory(rig_list)
    jsonpath = os.path.join(Define.DATAUPPATH, JSONFOLDER, asset_name, "%s.json" % (pose_name))
    writeJSON(rigdict, jsonpath)

    image_path = GetImage(asset_name, pose_name)

    return image_path
