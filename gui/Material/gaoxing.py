root = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages/asterstudy/workingdirectory/system/controlDict'
with open(root,'r+',encoding='utf-8') as fr:
    file_data=''
    for line in fr:
        # print(line)
        if 'endTime         ' in line:
            line = 'endTime         ' + '  1243' + ';'+'\n'
        file_data+=line
fr.close()

with open(root,'w',encoding='utf-8') as fr:
    fr.write(file_data)
fr.close()