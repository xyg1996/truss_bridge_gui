import os
import shutil
import os.path
import json
#文件初始化
def initfile(root,default_root):
    if os.path.exists(root):
        os.remove(root)
    shutil.copyfile(default_root,root)
#文件夹初始化
def inittree(root,default_root):
    if os.path.exists(root):
        shutil.rmtree(root)
    shutil.copytree(default_root,root)

def changefile(root, label,new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        file_data=''
        for line in fr:
            if label in line:
                    line = label + '  ' + new_str + ';'+'\n'
            file_data+=line
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write(file_data)
    fr.close()
#增加内容（用于材料模块）
def addfile(root,label,unit,value):
    with open(root,'r+',encoding='utf-8') as fr:
        lines=[]
        for line in fr: 
            lines.append(line)
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        lines.insert(-5, label+'              ' + unit + ' ' + value) 
        s = ''.join(lines)
        fr.write(s)
    fr.close()
#弃用
def changefile2(root, title, label,new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text ==  title:
                keywordlist[index+2] = '        ' + label + '            ' +new_str
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#根据标题标签增加内容
def addfile2(root, title, label,new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                keywordlist.insert(index+2, label + new_str + ';') 
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#删除末尾是'    }'的段(全删)
def delifexist(root,title):
    tar_list = []
    start_index = 0
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                start_index = index
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2 == '    }':
                        tar_list.append(index2)      
                        del keywordlist[start_index:start_index+index2+2]
                        break
        # keywordlist.insert(index, '')
                   

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#保留指定文件
def DeleteFiles(path,fileList):
    for parent,dirnames,filenames in os.walk(path):

        FullPathList = []
        DestPathList = []

        for x in fileList:
            DestPath = path + x
            DestPathList.append(DestPath)


        for filename in filenames:
            FullPath = os.path.join(parent,filename)
            FullPathList.append(FullPath)


        for xlist in FullPathList:
            if xlist not in DestPathList:
                os.remove(xlist)
#弃用
def addfile3(root, title, label,new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == '    ' + title:
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2.strip() == '}':
                        keywordlist.insert(index+index2,'        ' + label + '            ' + new_str + ';') 
                        break
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#从末尾开始添加
def addfile4(root,label):
    with open(root,'r+',encoding='utf-8') as fr:
        lines=[]
        for line in fr: 
            lines.append(line)
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        lines.insert(-1, label+'\n' + '{' + '\n' +'\n' + '}'+'\n'+'\n') 
        s = ''.join(lines)
        fr.write(s)
    fr.close()
#弃用
def addfile5(root, title, label,new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                keywordlist.insert(index+2,'    ' + label + ' ' + new_str + ';') 
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#根据标题修改内容
def changefile3(root,title, new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text ==  title:
                keywordlist[index+2] = '' + new_str
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
def changefile5(root,title, new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text ==  title:
                keywordlist[index] = '' + new_str
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#增加段
def addlabel(root,title,label):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text ==  title:
                keywordlist.insert(index + 2, '    ' + label+'\n' + '    {' + '\n' +'\n' + '    }'+'\n') 

    fr.close()


    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#增加段
def addlabel2(root,title,label):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text ==  title:
                keywordlist.insert(index + 2, '        ' + label+'\n' + '        {' + '\n' +'\n' + '        }'+'\n') 

    fr.close()


    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#删除末尾是'}'的段
def delifexist2(root,title):
    tar_list = []
    start_index = 0
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                start_index = index
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2 == '}':
                        tar_list.append(index2)      
                        del keywordlist[start_index+2:start_index+index2]
                        break

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()

#删除末尾是'}'的段
def delifexist3(root,title):
    tar_list = []
    start_index = 0
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                start_index = index
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2 == '}':
                        tar_list.append(index2)      
                        del keywordlist[start_index:start_index+index2+1]
                        break

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#删除末尾是');'的段
def delifexist4(root,title):
    tar_list = []
    start_index = 0
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                start_index = index
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2 == ');':
                        tar_list.append(index2)      
                        del keywordlist[start_index+2:start_index+index2]
                        break

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#删除末尾是'};'的段
def delifexist5(root,title):
    tar_list = []
    start_index = 0
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                start_index = index
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2 == '};':
                        tar_list.append(index2)      
                        del keywordlist[start_index+2:start_index+index2]
                        break

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#删除末尾是'    );'的段
def delifexist6(root,title):
    tar_list = []
    start_index = 0
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                start_index = index
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2 == '    );':
                        tar_list.append(index2)      
                        del keywordlist[start_index+2:start_index+index2]
                        break

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#删除末尾是'    }'的段
def delifexist7(root,title):
    tar_list = []
    start_index = 0
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                start_index = index
                for index2, text2 in enumerate(keywordlist[index:]):
                    if text2 == '    }':
                        tar_list.append(index2)      
                        del keywordlist[start_index+2:start_index+index2]
                        break

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()
#根据标题标签修改内容
def addfile6(root, title, label,new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        keywordlist = (fr.read().splitlines())
        for index,text in enumerate(keywordlist):
            if text == title:
                keywordlist.insert(index+2, label + new_str) 
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write('\n'.join(keywordlist))
    fr.close()

def changefile4(root, label,new_str):
    with open(root,'r+',encoding='utf-8') as fr:
        file_data=''
        for line in fr:
            if label in line:
                    line = label + ' ' + new_str+'\n' 
            file_data+=line
    fr.close()

    with open(root,'w',encoding='utf-8') as fr:
        fr.write(file_data)
    fr.close()

def save_to_json(workingdirectory,title,key_list,value_list):
    with open(workingdirectory + '/project_data.json', 'r') as json_file:
        load_dict = json.load(json_file)
    dictionary = dict(zip(key_list,value_list))
    load_dict[title] = dictionary
    json_str = json.dumps(load_dict, indent=4)
    with open(workingdirectory + '/project_data.json', 'w') as json_file:
        json_file.write(json_str)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass



import PyQt5.Qt as Q
from .behavior import behavior
# from .remotefs import MountWorker
from .widgets import PopupFrame

class LoadingMessage(Q.QObject):
    """Object that manages loading messages."""

    def __init__(self, parent, msg="Loading", closable=True):
        """Initialization.

        Arguments:
            parent (QWidget): Parent widget.
        """
        super().__init__()

        self._done = False
        self.widget = None
        self.timer = None
        self.parent = parent
        self.message = msg
        self.closable = closable

    def start(self, interval=1000):
        """Shows a loading page that is maintained until it is done."""
        self.widget = PopupFrame(self.parent,size=(400,100),
                                 msg=self.message,
                                 closable=self.closable)
        self.widget.move(0, 0)
        self.widget.resize(self.parent.width(), self.parent.height())
        self.widget.show()
        self.widget.closed.connect(self.close)

        self.timer = Q.QTimer(self.widget)
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.check_end)
        self.timer.start()
        self.init_tasks()

    # pragma pylint: disable=no-self-use
    def init_tasks(self):
        """Execute initialization tasks"""
        return

    # pragma pylint: disable=no-self-use
    def closure_tasks(self):
        """Execute closure tasks"""
        return

    def close(self):
        """Closes the popup manually (without interrupting tasks that are
        eventually running in background).
        """
        self.terminate()
        self.check_end()

    def check_end(self):
        """Check if the loading popup can be closed."""
        if self._done:
            self.timer.stop()
            self.widget.close()

    def terminate(self):
        """Note that the loading is terminated."""
        self._done = True

class BackgroundLoading(LoadingMessage):
    """Object that manage the loading of the module."""

    def __init__(self, parent, msg=''):
        """Initialization.

        Arguments:
            parent (QWidget): Parent widget.
        """
        # msg = translate("AsterStudy",
        #                 "Please wait while AsterStudy "
        #                 "finishes loading...")
        if not msg:
            msg = '未指定过度文字信息'
        LoadingMessage.__init__(self, parent, msg)
        # self.mountWorker = MountWorker()

    def init_tasks(self):
        """Execute initialization tasks"""
        if behavior().connect_servers_init:
            self.mount()

    def closure_tasks(self):
        """Execute closure tasks"""
        self.unmount()

    def mount(self):
        """Start thread to mount remote filesystems."""
        # self.mountThread.start()
        # self.mountStarted.emit()
        # self.mountWorker.mount()
        pass

    def unmount(self):
        """Unmount remote filesystems."""
        # self.mountWorker.unmount()
        pass
