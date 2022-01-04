from tkinter import *
import time
import datetime
import pyttsx3
import speech_recognition as sr
from threading import Thread
import requests
from bs4 import BeautifulSoup

def greeting():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning sir. I am Genos. How can I help you today? :))"
    elif 12 <= hour < 18:
        text = "Good Afternoon sir. I am Genos. How can I help you today? :))"
    else:
        text = "Good Evening sir. I am Genos. How can I help you today? :))"

    canvas2.create_text(10,10,anchor =NW , text=text,font=('Comic Sans MS', -25,'bold'), fill="black",width=350)
    
    p1=Thread(target=speak,args=(text,)) #thread for text to speech conversion
    p1.start()
    p2 = Thread(target=transition2) #thread for speech transition
    p2.start()
    
def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0,5000):
        for frame in str(frames):
            if flag == False:
                canvas.create_image(0, 0, image=img1, anchor=NW)
                canvas.update()
                flag = True
                return
            else:
                #canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)
        

def web_scraping(qs):
    global flag2
    global loading

    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    links = soup.findAll("a")
    
    all_links = []
    for link in links:
       link_href = link.get('href')
       if "url?q=" in link_href and not "webcache" in link_href:
           all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))
           

    flag= False
    for link in all_links:
       if 'https://en.wikipedia.org/wiki/' in link:
           wiki = link
           flag = True
           break

    div0 = soup.find_all('div',class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3  = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

    if len(div0)!=0:
        answer = div0[0].text
    elif len(div1) != 0:
       answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
    elif len(div2) != 0:
       answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
    elif len(div3)!=0:
        answer = div3[1].text
    elif flag==True:
       page2 = requests.get(wiki)
       soup = BeautifulSoup(page2.text, 'html.parser')
       title = soup.select("#firstHeading")[0].text
       
       paragraphs = soup.select("p")
       for para in paragraphs:
           if bool(para.text.strip()):
               answer = title + "\n" + para.text
               break
    else:
        answer = "Sorry. I could not find the desired results"


    canvas2.create_text(10, 225, anchor=NW, text=answer, font=('Comic Sans MS', -25,'bold'),fill="black", width=350)
    flag2 = False
    loading.destroy()

    p1=Thread(target=speak,args=(answer,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def speak(text):
    global flag
    engine.say(text) #pyttsx3 module TEXT TO SPEECH
    engine.runAndWait()
    flag=False



def shut_down():
    p1=Thread(target=speak,args=("Power Off. Thankyou For Using Our Sevice. Good Bye :))",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    root.destroy()
    
def takecommand():
    global loading
    global flag
    global flag2
    global canvas2
    global query
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")

    speak("Ask me a Query")
    flag= True
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 1000
    with sr.Microphone() as source:
        print("Listening your voice...")
        audio = r.listen(source,timeout= 10 ,phrase_time_limit= 10)

    try:
        print("Recognizing your voice...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said :{query}\n")
        query = query.lower()
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=query, font=('Comic Sans MS', -30),fill="black", width=350)
        global img3
        loading = Label(root, image=img3, bd=0)
        loading.place(x=900, y=622)

    except Exception as e:
        print(e)
        speak("Sorry, I don't understand you. Say that again please")
        return "None"


def main_window():
    global query
    greeting()
    while True:
        if query != None:
            if 'shutdown' in query or 'quit' in query or 'stop' in query or 'goodbye' in query:
                shut_down()
                break
            else:
                web_scraping(query)
                query = None

    

if __name__ == "__main__":
    loading = None
    query = None
    flag = True
    flag2 = True

    
#Text to Speech
    engine = pyttsx3.init() # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)

    root=Tk()
    root.title("Intelligent Voice Chatbot")
    root.geometry('1360x690+-5+0')
    root.configure(background='white')

 #Media files
    img1= PhotoImage(file='chatbot-image1.png')
    
    img2= PhotoImage(file='gvoice.png')
    
    img3= PhotoImage(file='loading.png')
    
    img4= PhotoImage(file='chatsection.png')
    
    background_image=PhotoImage(file="bg.png")
  

    f = Frame(root,width = 1355, height = 685) #Front intro page
    f.place(x=0,y=0)
    f.tkraise()
    front_image = PhotoImage(file="frontimage123.png")
    okVar = IntVar()
    btnOK = Button(f, image=front_image,command=lambda: okVar.set(1))
    btnOK.place(x=0,y=0)
    f.wait_variable(okVar)
    f.destroy()    
    
    

    background_label = Label(root, image=background_image) # Background image
    background_label.place(x=0, y=0)

    frames = PhotoImage(file="chatstart.png")
    canvas = Canvas(root, width = 804, height = 601)
    canvas.place(x=10,y=10)
    canvas.create_image(0, 0, image=img1, anchor=NW)
    
    
    question_button = Button(root,image=img2, bd=0, command=takecommand)# voice search button
    question_button.place(x=1280,y=625)

    frame=Frame(root,width=500,height=596)
    frame.place(x=825,y=10)
    canvas2=Canvas(frame,bg='#FFFFFF',width=500,height=596,scrollregion=(0,0,500,900))
    
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas2.yview)
    
    canvas2.config(width=500,height=596, background="black")
    canvas2.config(yscrollcommand=vbar.set)
    canvas2.pack(side=LEFT,expand=True,fill=BOTH)
    canvas2.create_image(0,0, image=img4, anchor="nw")

    task = Thread(target=main_window) #Thread which targets main window
    task.start()
    root.mainloop()