from tkinter import *
from tkinter.font import Font
import multiprocessing
import os
import json
import webbrowser
from tree_interface.app import run_server
from utils import *

TITLE = "Interface de configuration"
CONFIG_PATH = abspath(__file__)+"config.json"

config = json.loads(open(CONFIG_PATH).read())



def center(win):
    """centers a tkinter window

    Args:
        win (obj): the main window or Toplevel window to center
    """

    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def update():
    """update the configuration file

    """
    config['screen_mode']= str(screen_mode.get())
    config['auth']= str(auth.get())

    with open(CONFIG_PATH, 'w',encoding='utf8') as outfile:
        json.dump(config, outfile,indent=4,ensure_ascii=False)

def open_interface():

   webbrowser.open_new_tab("http://127.0.0.1:5001/index.html")
    

if __name__ == "__main__":

    # run the server in parallel
    p = multiprocessing.Process(target=run_server, args=())
    p.daemon = True
    show= True
    p.start() 


    # create and center the window
    app = Tk()
    app.geometry("500x500")
    app.title(TITLE)
    center(app)


    # font style
    fontStyleLabel = Font(family="Gill Sans", size=12)
    fontStyleInput = Font(family="Gill Sans", size=11)
    fontStyleButton = Font(family="Gill Sans", size=12)


    # create elements for first configuration (screen mode)
    L1 = Label(text="Mode écran : " ,font=fontStyleLabel)
    screen_mode = BooleanVar()
    screen_mode.set(config['screen_mode'])
    R1 = Radiobutton(app, text="Activé", variable=screen_mode, value=True,
                    command=update,font=fontStyleInput)
    
    
    R2 = Radiobutton(app, text="Désactivé", variable=screen_mode, value=False,
                    command=update,font=fontStyleInput)


    
    # create elements for second configuration (mono-user mode)
    L2 = Label(text="Mode mono-utilisateur (authentification) : ",font=fontStyleLabel)

    auth = BooleanVar()
    auth.set(config['auth'])
    R3 = Radiobutton(app, text="Activé", variable=auth, value=True,
                    command=update,font=fontStyleInput)

    R4 = Radiobutton(app, text="Désactivé", variable=auth, value=False,
                    command=update,font=fontStyleInput)
    B = Button(app, text ="Ajouter un scénario", command = open_interface,font=fontStyleButton)


    # insert elements in the window 
    L1.pack(padx=(0,0), pady=(50,0), fill='both')
    R1.pack(fill='both')
    R2.pack(fill='both')

    L2.pack(padx=(0,0), pady=(50,0), fill='both')
    R3.pack(fill='both')
    R4.pack(fill='both')

    B.pack(padx=(0,0), pady=(50,0))

    mainloop()

