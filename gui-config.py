from tkinter import *
import multiprocessing
import os
import json
import webbrowser
from tree_interface.app import run_server
from utils import *

TITLE = "CONFIG GUI"
CONFIG_PATH = abspath(__file__)+"config.json"

config = json.loads(open(CONFIG_PATH).read())




# def convert_audio():
    
#     address_info = address.get()
    
#     language = 'en'
    
#     myobj = gTTS(text=address_info, lang=language, slow=False)
    
#     myobj.save("welcome.mp3") 
    
#     playsound("welcome.mp3")

#     os.remove("welcome.mp3")
    
        
#     print(address_info)
    
#     address_entry.delete(0,END)    
    
# def get_audio():
# 	r = sr.Recognizer()
# 	with sr.Microphone() as source:
# 		audio = r.listen(source)
# 		said = ""

# 		try:
# 		    said = r.recognize_google(audio)
# 		    print(said)
# 		except Exception as e:
# 		    print("Exception: " + str(e))

# 	return said

# def get_txt():
#     txt = get_audio()
#     f= open("myfile.txt","w+")
#     f.write(txt)
#     f.close()




def update():
    config['screen_mode']= str(screen_mode.get())
    config['auth']= str(auth.get())

    with open(CONFIG_PATH, 'w',encoding='utf8') as outfile:
        json.dump(config, outfile,indent=4,ensure_ascii=False)

def open_interface():
   webbrowser.open_new_tab("http://127.0.0.1:5001/")
    

if __name__ == "__main__":

    p = multiprocessing.Process(target=run_server, args=())
    p.daemon = True
    show= True
    p.start() 


    app = Tk()
    app.geometry("500x500")

    app.title(TITLE)

    screen_mode = BooleanVar()
    screen_mode.set(config['screen_mode'])
    R1 = Radiobutton(app, text="Eable", variable=screen_mode, value=True,
                    command=update)
    R1.pack( anchor = W )

    R2 = Radiobutton(app, text="Disable", variable=screen_mode, value=False,
                    command=update)
    R2.pack( anchor = W )

    auth = BooleanVar()
    auth.set(config['auth'])
    R1 = Radiobutton(app, text="Mono mode", variable=auth, value=True,
                    command=update)
    R1.pack( anchor = W )

    R2 = Radiobutton(app, text="General", variable=auth, value=False,
                    command=update)
    R2.pack( anchor = W )



    B = Button(app, text ="interface", command = open_interface)
    B.pack()



    label = Label(app)
    label.pack()
    

    mainloop()






# heading = Label(text="Python Text to Audio",bg="yellow",fg="black",font="10",width="500",height="3")

# heading.pack()

# address_field = Label(text="Text :")

# address_field.place(x=15,y=70)

# address = StringVar()


# address_entry = Entry(textvariable=address,width="30")

# address_entry.place(x=15,y=100)

# button = Button(app,text="Convert to Audio",command=convert_audio,width="30",height="2",bg="grey")

# button.place(x=15,y=140)

# button = Button(app,text="click and speak",command=get_txt,width="30",height="2",bg="red")

# button.place(x=15,y=200)

# from tkinter import *

# def sel():
#    selection = "You selected the option " + str(var.get())
#    label.config(text = selection)

# app = Tk()
# var = IntVar()
# R1 = Radiobutton(app, text="Option 1", variable=var, value=1,
#                   command=sel)
# R1.pack( anchor = W )

# R2 = Radiobutton(app, text="Option 2", variable=var, value=2,
#                   command=sel)
# R2.pack( anchor = W )

# R3 = Radiobutton(app, text="Option 3", variable=var, value=3,
#                   command=sel)
# R3.pack( anchor = W)

# label = Label(app)
# label.pack()
# app.mainloop()
