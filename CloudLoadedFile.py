
import time
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
from tkinter.scrolledtext import *
import tkinter.font as font
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from zipfile import ZipFile
import shutil
import webbrowser
import urllib3




global Proj_Selected,File_Selected,Loggedin,session
Proj_Selected = ""
File_Selected = ""
session = 'Server NA'
try:
    cloud_config= {
        'secure_connect_bundle': 'DB/secure-connect-designer.zip'
        }
    auth_provider = PlainTextAuthProvider('yqkBNpZdOcZOWgmrIHZdPMLr', 'YBvauJmy1fy0OjF3IL7oP6BjRh0T-63ISj0RjbEMg5biQe196b+WZZlrTwp_N.EFnHQz-Hsra,pQm7lbNUMM3LF.1lGuFA7N_RWxZUP.ujlu.ppOiWsZU3kaaf1fqsHj')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect('designer')
except:
    "ignore"

Loggedin=False

import os
from os.path import basename



def AppUpdate():
    global session
    version = session.execute('SELECT * FROM designer.version LIMIT 1')
    for versions in enumerate(version,start=0):
            version_id = versions[0]
    version = session.execute('SELECT * FROM designer.version LIMIT 1')
    Hintv = Toplevel(base.root)
    Hintv.overrideredirect(True)
    Hintv.title("New Version Avaiable")
    Hintv.geometry("500x800+300+300")
    Hintv.configure(bg='#383838',highlightthickness=0)
    
    
    Header = Label(Hintv,text="New Version Avaiable",bg='#383838',fg='white',font=('ariel',7))
    Header.place(x=60,y=10)
    Header = Label(Hintv,text='Version '+version[version_id][0]+' is avaiable',bg='#383838',fg='white',font=('ariel',5))
    Header.place(x=100,y=50)
    Header = Label(Hintv,text="-------------------------------------------------------------\n"+version[version_id][1],bg='#383838',fg='white',font=('ariel',5))
    Header.place(x=0,y=120)
    Header = Label(Hintv,text="-------------------------------------------------------------",bg='#383838',fg='white',font=('ariel',5))
    Header.place(x=0,y=700)
    
    
    
    ProjCreateButton = Button(Hintv,bg='#4A4A4A',text='Update',font=('ariel',5),highlightthickness=0,borderwidth=0,fg='white',command= lambda: Update())
    ProjCreateButton.place(x=330,y=735)
    
            
def DirNameLoopCheckCreate(name):
    a = True
    b = 0
    while a:
        try:    
            os.mkdir(name+' '+str(b))
            a = False
        except:
            b += 1 
    return str(name+' '+str(b)+r'/')

def OpenPreFile():
    f = askopenfile(mode='r')
    dir = DirNameLoopCheckCreate('Projects/Import')
    tfile = f.name
    cfile = list()
    for word in enumerate(tfile):
            if word[1]==r'/' or word[1]==r'.':
                cfile.append(str())
            else:
                cfile[len(cfile)-1] += word[1]
    cfile = cfile[len(cfile)-2]+'.'+cfile[len(cfile)-1]
    print(cfile)
    open(dir+cfile,mode='w').write(str(open(f.name).read()))
    open(dir+'DateCreated.txt',mode='w').write(time.asctime())
    open(dir+'Password.txt',mode='w').write('')
    UpdateTo('Home')


    

def View_Trash():
    
    Hinttv = Toplevel(base.root)
    Hinttv.overrideredirect(True)
    Hinttv.title("New Version Avaiable")
    Hinttv.geometry("700x1300+200+300")
    Hinttv.configure(bg='black',highlightthickness=1)
    vbar_top = Canvas(Hinttv,width=1080,height=80,bg='#383838',highlightthickness=0)
    vbar_top.pack(pady=0, fill=BOTH)
    vbar_midtop = Canvas(Hinttv,width=1080,height=50,bg='#4A4A4A',highlightthickness=0)
    vbar_midtop.pack(pady=0, fill=BOTH)
    vbar_files = Canvas(Hinttv,width=1080,height=1200,bg='black',highlightthickness=0)
    vbar_files.pack(pady=0, fill=BOTH)
    
    Header = Label(vbar_top,text='Trash',bg='#383838',fg='white')
    Header.place(x=285,y=20)
    

    TrashedFiles = {}
    WidgetTrashedFilesHeader = {}
    WidgetTrashedFilesPath = {}
    WidgetTrashedFilesRestore = {}

    for ba, dir, zip in os.walk('Projects/.Trash/'):
        for file in enumerate(zip):
            TrashedFiles[str(file[0])] = Canvas(vbar_files,width=800,height=60,bg='#4A4A4A',highlightthickness=0)
            TrashedFiles[str(file[0])].pack(pady=15,padx=10,anchor=NW,fill=BOTH)
            
            WidgetTrashedFilesHeader[str(file[0])] = Label(TrashedFiles[str(file[0])], text = zip[file[0]],bg='#4A4A4A', fg='white',font=('ariel',3))
            WidgetTrashedFilesHeader[str(file[0])].place(x=3,y=3)
            
            WidgetTrashedFilesPath[str(file[0])] = Label(TrashedFiles[str(file[0])], text = os.path.abspath('Projects/.Trash/'+zip[file[0]]),bg='#4A4A4A', fg='white',font=('ariel',2))
            WidgetTrashedFilesPath[str(file[0])].place(x=13,y=30)
            
            WidgetTrashedFilesRestore[str(file[0])] = Button(TrashedFiles[str(file[0])], text = 'restore',bg='#383838', fg='white',font=('ariel',3),highlightthickness=0,borderwidth=0, command= lambda file='Projects/.Trash/'+zip[file[0]]: Restore(file))
            WidgetTrashedFilesRestore[str(file[0])].place(x=550,y=0)
            

                

        
    
def Restore(file):
    with ZipFile(file, 'r') as zipObj:
        tfile = tuple(file)
        cfile = list()
        cfile.append(str())
        for word in enumerate(tfile):
            if word[1]==r'/' or word[1]==r'.':
                cfile.append(str())
            else:
                cfile[len(cfile)-1] += word[1]
        for wordb,cf in enumerate(cfile):
            if cf=='Projects' or cf=='.Trash' or cf=='zip':
                "ignore"
            else:
                cfile = str(cf)+r'/'
            
            
        os.mkdir('Projects/'+cfile)
        zipObj.extractall('Projects/'+cfile)
        os.remove(file)

        UpdateTo('Home')    
    
    
    
    





def Update():
    webbrowser.open('https://raw.githubusercontent.com/XMSX-Designer/Python-WorkSpace/main/CloudLoadedFile.py')











class base():
    root = Tk()
    baseprojects = {}
    Version = '0.0.1'

    def Restart():
        base.root = Tk()
        base.baseprojects = {}


    
        
def CodeUpdate(file):
    global textcore,Proj_Selected,File_Selected,Project_Header,AbsPasth_Header
    Proj = Proj_Selected
    open(File_Selected,mode='w').write(textcore.get("1.0", END))
    code = open(Proj+file).read()
    File_Selected = Proj_Selected+file
    textcore.delete('1.0', END)
    textcore.insert(INSERT,code)
    textcore.update_idletasks()
    Project_Header.configure(text=str(file))
    AbsPasth_Header.configure(text=str(os.path.abspath(File_Selected)))
                
                    
                        
                            
                                
                                    
                                        
                                            
                                                    
def UpdateTo(memu):
       base.root.destroy()
       base.Restart()
       Main.INTI(base)
       if memu=='Home':
           Main.Home(base)
       elif memu=='Ide':
           Main.Ide(base)
       
def CreateFile():
       global ProjNameGet_,FileNameGet_,FilePassGet_
       PathName = ProjNameGet_.get()
       FileName = FileNameGet_.get()
       FilePass = FilePassGet_.get()
       try:
           os.mkdir(rf'Projects/{PathName}')
       except:
           "none"
       open(rf'Projects/{PathName}/{FileName}',mode='w').write('')
       open(rf'Projects/{PathName}/DateCreated.txt',mode='w').write(time.asctime())
       open(rf'Projects/{PathName}/Password.txt',mode='w').write(FilePass)
       

       UpdateTo('Home')
       
       
def DeleteProj(Proj,Name):
       with ZipFile(f'Projects/.Trash/{Name}.zip', 'w') as zipObj:
           # Iterate over all the files in directory
           for folderName, subfolders, filenames in os.walk(Proj):
               for filename in filenames:
                   #create complete filepath of file in directory
                   filePath = os.path.join(folderName, filename)
                   # Add file to zip
                   zipObj.write(filePath, basename(filePath))
       shutil.rmtree(Proj)
       UpdateTo('Home')
       
def OpenIde(Proj):
       global Proj_Selected
       Proj_Selected=str(Proj)
       UpdateTo('Ide')
       

       
       
       
       
       
       
    
def NewProject():
    global FileNameGet_, ProjNameGet_,FilePassGet_
    Hint = Toplevel(base.root)
    Hint.overrideredirect(True)
    Hint.title("Create Project")
    Hint.geometry("500x500+300+300")
    Hint.configure(bg='#383838',highlightthickness=0)
    
    ProjNameGet = Label(Hint,text='Project Name: ',fg='white',font=('ariel',5),bg='#383838')
    ProjNameGet.place(x=15,y=27)
    ProjNameGet_ = Entry(Hint,width=10,bg='#383838',fg='white')
    ProjNameGet_.place(x=230,y=20)

    FileNameGet = Label(Hint,text='Base File Name: ',fg='white',font=('ariel',5),bg='#383838')
    FileNameGet.place(x=15,y=107)
    FileNameGet_ = Entry(Hint,width=10,bg='#383838',fg='white')
    FileNameGet_.place(x=230,y=100)
    
    FilePassGet = Label(Hint,text='Password:',fg='white',font=('ariel',5),bg='#383838')
    FilePassGet.place(x=15,y=187)
    FilePassGet_ = Entry(Hint,width=10,bg='#383838',fg='white')
    FilePassGet_.place(x=230,y=180)
    
    
    
    ProjCreateButton = Button(Hint,bg='#4A4A4A',text='Create',font=('ariel',5),highlightthickness=0,borderwidth=0,fg='white',command=CreateFile)
    ProjCreateButton.place(x=330,y=435)

def UserLogin():
    global UsernameGet_,LoginPass_,Loggedin
    if UsernameGet_.get()==SERVER.EXEC(f"SELECT User_Id FROM User_Id WHERE User_Id='{UsernameGet_.get()}'"):
        print("True")
    else:
        print('False')
    
def UserCreate():
    ""    

    
def Login():
    global LoginPass_, UsernameGet_,Loggedin
    if Loggedin:
        "else"
    else:
    
        Hintx = Toplevel(base.root)
        Hintx.overrideredirect(True)
        Hintx.title("Create Project")
        Hintx.geometry("500x500+300+300")
        Hintx.configure(bg='#383838',highlightthickness=0)
    
        UsernameGet = Label(Hintx,text='Username: ',fg='white',font=('ariel',5),bg='#383838')
        UsernameGet.place(x=15,y=27)
        UsernameGet_ = Entry(Hintx,width=10,bg='#383838',fg='white')
        UsernameGet_.place(x=230,y=20)

        LoginPass = Label(Hintx,text='Password: ',fg='white',font=('ariel',5),bg='#383838')
        LoginPass.place(x=15,y=107)
        LoginPass_ = Entry(Hintx,width=10,bg='#383838',fg='white')
        LoginPass_.place(x=230,y=100)
    
    
    
    
    
        UserLogin_ = Button(Hintx,bg='#4A4A4A',text='Login',font=('ariel',5),highlightthickness=0,borderwidth=0,fg='white',command=UserLogin)
        UserLogin_.place(x=340,y=435)   
    
        UserCreate_ = Button(Hintx,bg='#4A4A4A',text='Create Account',font=('ariel',5),highlightthickness=0,borderwidth=0,fg='white',command=UserCreate)
        UserCreate_.place(x=0,y=435)   
            
                
                    
def BackHomeUpdate():
    UpdateTo('Home')                      
                            
                                
                                    
                                        
def FileSave():
    global Proj_Selected,File_Selected, textcore
    open(File_Selected,mode='w').write(textcore.get("1.0", END))   
                                           
                                                
                                                    
                                                        
                                                            
                                                                
                                                                    
                                                                            
class Main():
    def INTI(core):
        core.root.title("Designer")
        core.root.geometry("1080x2176")
        core.root.minsize(width=400, height=4)
        core.root.configure(bg='black')

    
    def Ide(core):
        global Proj_Selected,textcore,File_Selected,Project_Header,AbsPasth_Header
        ToolBar = Canvas(core.root,width=1080,height=150,bg='#383838',highlightthickness=0)
        ToolBar.pack(pady=0, fill=BOTH)
        ToolBarb = Canvas(core.root,width=1080,height=75,bg='#4A4A4A',highlightthickness=0)
        ToolBarb.pack(pady=0, fill=BOTH)
        
        
        textcore = ScrolledText(base.root, state='normal', height=400, width=400, wrap='word', pady=2, padx=3, undo=True,bg='black',fg='white',font=('ariel',5),highlightthickness=0)
        textcore.vbar.configure(troughcolor = '#4A4A4A', bg = '#383838',highlightthickness=0,borderwidth=0)
        
        textcore.pack(fill=Y, expand=1)
        textcore.focus_set()
        
        FileBackButton = Button(ToolBar,text='Back',bg='#4A4A4A',fg='white',font=("Bold", 3),highlightthickness=0,borderwidth=0,command= lambda: BackHomeUpdate())

        FileBackButton.place(x=0,y=0)   
        
        FileSaveButton = Button(ToolBar,text='Save',bg='#4A4A4A',fg='white',font=("Bold", 3),highlightthickness=0,borderwidth=0,command= lambda: FileSave())

        FileSaveButton.place(x=950,y=0)   
       

        
        
        FileButton = {}
        
        
        
        
        for Base,dir,Files in os.walk(str(Proj_Selected)):
            File_Selected = Proj_Selected+Files[0]
            Project_Header = Label(ToolBar,text=Files[0],fg='white',bg='#383838')
            Project_Header.place(x=150,y=20)      
            AbsPasth_Header = Label(ToolBar,text=os.path.abspath(Proj_Selected+Files[0]),fg='#C1C1C1',bg='#383838',font=('ariel',4))
            AbsPasth_Header.place(x=170,y=70)     
            textcore.insert(INSERT,open(File_Selected).read()) 


            for File in enumerate(Files,start=0):
                _File = File[0]
                

                FileButton[str(_File)] = Button(ToolBarb,text=Files[_File],bg='#383838',fg='white',font=("Bold", 3),highlightthickness=0,borderwidth=0,command= lambda File=File[1]: CodeUpdate(File))

                FileButton[str(_File)].grid(column=1*_File,row=0,padx=1)   
       
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    def Home(core):
        global session
        bar_top = Canvas(core.root,width=1080,height=150,bg='#383838',highlightthickness=0)
        bar_top.pack(pady=0, fill=BOTH)
        bar_midtop = Canvas(core.root,width=1080,height=100,bg='#4A4A4A',highlightthickness=0)
        bar_midtop.pack(pady=0, fill=BOTH)
        bar_files = Canvas(core.root,width=1080,height=2000,bg='black',highlightthickness=0)
        bar_files.pack(pady=0, fill=BOTH)
        
        version = session.execute('SELECT * FROM designer.version LIMIT 1')
        for versions in enumerate(version,start=0):
            version_id = versions[0]
        version = session.execute('SELECT * FROM designer.version LIMIT 1')
        if core.Version==str(version[version_id][0]):
            "ignore"
        else:
            UpdateBtn = Button(bar_top, text="Update!",bg='#4A4A4A',fg='white',font=("Bold", 3),command=AppUpdate,highlightthickness=0,borderwidth=0)
            UpdateBtn.place(x=930,y=0)
        
        Create_Project = Button(bar_midtop, text="New Project",bg='#383838',fg='white',font=("Bold", 3),command=NewProject,highlightthickness=0,borderwidth=0)
        Create_Project.place(x=0,y=0)
        
        vtrash = Button(bar_midtop, text="Trash",bg='#383838',fg='white',font=("Bold", 3),command=View_Trash,highlightthickness=0,borderwidth=0)
        vtrash.place(x=185,y=0)
        
        Account = Button(bar_top, text="Account",bg='#4A4A4A',fg='white',font=("Bold", 3),command=Login,highlightthickness=0,borderwidth=0)
        Account.place(x=0,y=0)
        
        
        Title = Label(bar_top, text='Python WorkFlow', fg='white', bg='#383838',font=("conthrax-sb", 15))
        Title.place(x=220,y=10)
        
        Version = Label(bar_top, text=core.Version, fg='white', bg='#383838',font=("conthrax-sb", 6))
        Version.place(x=850,y=54)
        
        Open_Project = Button(bar_midtop, text="Import",bg='#383838',fg='white',font=("Bold", 3),command=OpenPreFile,highlightthickness=0,borderwidth=0)
        Open_Project.place(x=324,y=0)
        
        
        
        
        for ba,dir,file in os.walk('Projects/'):
            for path in range(len(dir)):
                if dir[path-1]=='.Trash':
                    dir.pop(path-1)
            for directories in range(len(dir)):
                
                core.baseprojects[str(directories)] = {}
                core.baseprojects[str(directories)]['RawPath'] = r'Projects/'+str(dir[directories])
                core.baseprojects[str(directories)]['Name'] = dir[directories]
                for file in os.walk(core.baseprojects[str(directories)]['RawPath']):
                    pack = list()
                    for filee in range(len(file[2])):
                        pack.append(file[2][filee])
                    core.baseprojects[str(directories)]['Files'] = pack
        print(str(core.baseprojects))
        _project_ = {}       
        for project in range(len(core.baseprojects)):
            _project_[core.baseprojects[str(project)]['Name']] = Canvas(bar_files,width=800,height=100,bg='#4A4A4A',highlightthickness=0)
            _project_[core.baseprojects[str(project)]['Name']].pack(pady=15,padx=20,anchor=NW,fill=BOTH)
        Name = {}
        Path = {}
        Files = {}
        Open = {}
        Date = {}
        Delete = {}
            
        for project in range(len(core.baseprojects)):
            Name[core.baseprojects[str(project)]['Name']] = Label(_project_[core.baseprojects[str(project)]['Name']], text=core.baseprojects[str(project)]['Name'],bg='#4A4A4A',fg='white',font=("Bold", 4))
            Name[core.baseprojects[str(project)]['Name']].place(x=5,y=5)
            
            Path[core.baseprojects[str(project)]['Name']] = Label(_project_[core.baseprojects[str(project)]['Name']], text=os.path.abspath(core.baseprojects[str(project)]['RawPath'])+r"/",bg='#4A4A4A',fg='white',font=("Bold", 3))
            Path[core.baseprojects[str(project)]['Name']].place(x=20,y=32)
            projfileshint = str()
            for file in core.baseprojects[str(project)]['Files']:
                if file=='DateCreated.txt' or file=='Password.txt':
                    "ignore"
                else:
                    projfileshint += file+" | "
            
            Files[core.baseprojects[str(project)]['Name']] = Label(_project_[core.baseprojects[str(project)]['Name']], text=str(projfileshint),bg='#4A4A4A',fg='white',font=("Bold", 3))
            Files[core.baseprojects[str(project)]['Name']].place(x=5,y=75)
            
            Open[core.baseprojects[str(project)]['Name']] = Button(_project_[core.baseprojects[str(project)]['Name']], text="Open",bg='#383838',fg='white',font=("Bold", 3),highlightthickness=0,borderwidth=0,command= lambda x = core.baseprojects[str(project)]['RawPath']+"/": OpenIde(x))
            Open[core.baseprojects[str(project)]['Name']].place(x=909,y=1)
            try:
                DateCreated = open(core.baseprojects[str(project)]['RawPath']+r"/"+"DateCreated.txt").read()
            except:
                DateCreated = '                Date Not Found'
            Date[core.baseprojects[str(project)]['Name']] = Label(_project_[core.baseprojects[str(project)]['Name']], text=DateCreated,bg='#4A4A4A',fg='white',font=("Bold", 3))
            Date[core.baseprojects[str(project)]['Name']].place(x=850,y=75)
            
            Delete[core.baseprojects[str(project)]['Name']] = Button(_project_[core.baseprojects[str(project)]['Name']], text="Delete",bg='#383838',fg='white',font=("Bold", 3),highlightthickness=0,borderwidth=0,command= lambda project = project: DeleteProj(core.baseprojects[str(project)]['RawPath'],core.baseprojects[str(project)]['Name']))
            Delete[core.baseprojects[str(project)]['Name']].place(x=770,y=1)
            
            
                
                
            
            
    def Base_Folders(dir):   
        for directory in enumerate(dir):
            if os.path.exists(directory[1]):
                "ignore"
            else:
                os.mkdir(directory[1]) 
                if directory[1]==r'User/':
                    open('User/Login.txt',mode='w').write()
                    
            
            
            
        
                
                
            
        
    
    
    
    def Exec():
        global LoginInfo
        Main.Base_Folders((r'Projects/',r'Projects/.Trash',r'User/',r'DB/'))
        Main.INTI(base)
        Main.Home(base)
        base.root.mainloop()
        



        
        
        
       
        
        

Main.Exec() 
