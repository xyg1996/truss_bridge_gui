def create_static_comm(material1,material2,element,work_dir):
    import os
    import platform
    sysstr = platform.system()
    if(sysstr =="Windows"):
        print("Call Windoes tasks")
        file = work_dir + '\gui\static.comm'
    elif(sysstr == "Linux"):
        print ("Call Linux tasks")
        file = work_dir + '/static.comm'
    else:
        print ("Other System tasks")
        return False
    data = ''
    i = 1
    with open(file,'r+') as f:
        for line in f.readlines():
            if(line.find('steel') == 0):
                #line = 'width = %s' % (str(self.width1)) + '\n'
                line = 'steel = DEFI_MATERIAU(ELAS=_F(E=%s, NU=%s, RHO=%s))' % (material1[0],material1[1],material1[2])  + '\n'
            if(line.find('concrete') == 0):
                line = 'concrete = DEFI_MATERIAU(ELAS=_F(E=%s, NU=%s, RHO=%s))' % (material2[0],material2[1],material2[2])  + '\n'
            '''print(i,len(line))
            if(line.find('CARA',4) == 0):
                print('ok')'''
            if i == 23:
                line = '    COQUE=_F(EPAIS=%s, GROUP_MA=(\'road\', )),' % (element[0]) + '\n'
            if i == 30:
                line = '            VALE=(%s, )' % (element[1]) + '\n'
            if i == 35:
                line = '            VALE=(%s, )' % (element[2]) + '\n'
            if i == 40:
                line = '            VALE=(%s, )' % (element[3]) + '\n'
            if i == 45:
                line = '            VALE=(%s, )' % (element[4]) + '\n'

            i+=1
            data += line
    f.close
    #print(data)
    with open(file,'r+') as f:
        f.writelines(data)
    f.close

if __name__ == '__main__':
    import os
    import platform
    material1=[2e11,0.3,7850]
    material2=[2.5e10,0.2,2500]
    element = [0.1,0.2,0.3,0.4,0.5]
    ### windows
    '''curr_dir =  os.getcwd()
    print('curr_dir:',curr_dir)
    create_static_comm(material1,material2,element,curr_dir)
    ### linux
    curr_dir = os.popen('echo `pwd`').read()[0:-1]
    print('curr_dir:',curr_dir)
    create_static_comm(material1,material2,element,curr_dir)'''
    sysstr = platform.system()
    if(sysstr =="Windows"):
        curr_dir =  os.getcwd()
        print('curr_dir:',curr_dir)
        create_static_comm(material1,material2,element,curr_dir)
    elif(sysstr == "Linux"):
        curr_dir = os.popen('echo `pwd`').read()[0:-1]
        print('curr_dir:',curr_dir)
        create_static_comm(material1,material2,element,curr_dir)
    else:
        print ("Other System tasks")

