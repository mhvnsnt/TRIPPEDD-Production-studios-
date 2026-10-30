# -*- coding: utf-8 -*-
import NatronEngine


def cam_load_chan( thisParam=False, thisNode=False, thisGroup=False, app=False, userEdited=False):
    if not NatronEngine.natron.isBackground():
        if thisParam.getScriptName() == 'import_chan_file': # and userEdited :
            node=thisNode
            chan=open(node.chan.get(),"r")
            for c in chan.readlines() :
                i=c.replace('\n','').split("\t")
                f=int(i[0])
                node.locx.setValueAtTime(float(i[1]),f)
                node.locy.setValueAtTime(float(i[2]),f)
                node.locz.setValueAtTime(float(i[3]),f)
                node.rotx.setValueAtTime(float(i[4]),f)
                node.roty.setValueAtTime(float(i[5]),f)
                node.rotz.setValueAtTime(float(i[6]),f)
                if len(i) == 8 :
                    node.fov.setValueAtTime(float(i[7]),f)
            chan.close()
