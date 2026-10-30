# -*- coding: utf-8 -*-
import NatronEngine

def plane_read_chan(thisParam, thisNode, thisGroup, app, userEdited) :
    if thisParam.getScriptName() == 'import_chan_file' and userEdited :
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
        chan.close()
