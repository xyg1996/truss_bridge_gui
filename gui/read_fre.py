import os
import platform
sysstr = platform.system()
if(sysstr =="Windows"):
    curr_dir =  os.getcwd()
    print('curr_dir:',curr_dir)
    file = curr_dir + '\gui\message'
elif(sysstr == "Linux"):
    curr_dir = os.popen('echo `pwd`').read()[0:-1]
    print('curr_dir:',curr_dir)
else:
    print ("Other System tasks")
data = ''
num = 11
i = 1
id_modal = 0
with open(file,'r+') as f:
    for line in f.readlines():
        try:
            if(line.find('     Calcul modal') == 0):
                #line = 'width = %s' % (str(self.width1)) + '\n'
                print('modal:',i)
                id_modal = i
            if i >= (id_modal + 4) and i <= (id_modal + 4 + num -1) and id_modal:
                data +=line
            i+=1
        except:
            print('error! Not find frequency result!')
        #data += line
f.close
print('id_modal:',id_modal)
#print(data.split())
fre_data = data.split()
fre = []
for i in range(1,len(fre_data),3):
    #print(fre_data[i])
    fre.append(fre_data[i])
print('fre:',fre)
fre_num = []
for i in fre:
    j = i[0:7]
    fre_num.append(j)
print('fre_num:',fre_num)

