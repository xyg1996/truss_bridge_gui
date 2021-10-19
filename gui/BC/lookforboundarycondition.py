import os

# open_file_dir = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/hotRoom/constant/polyMesh/boundary'


def lookforboundaryname(open_file_dir):
    with open(open_file_dir,'r',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines()[16:])
        indexlist = []
        flist = []
        index1 = keywordlist.index("(")+1
        indexlist.append(index1)
        for i, x in enumerate(keywordlist):
            if x == '    }':
                k = i+1
                indexlist.append(k)
        for i in indexlist[0:-1]:
            flist.append(keywordlist[i].strip())
        return flist

def lookforboundarytype(open_file_dir):
    with open(open_file_dir,'r',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines()[16:])
        indexlist = []
        flist = []
        for i, x in enumerate(keywordlist):
            if x == '    {':
                k = i+1
                indexlist.append(k)
        for i in indexlist:
            k = keywordlist[i].replace('type','')
            k = k.replace(';','')
            flist.append(k.strip())
        return flist

    