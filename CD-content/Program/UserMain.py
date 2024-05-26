from tkinter import messagebox
from tkinter import * 
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
import datetime
import webbrowser 
import qrcode
import random
import cv2
import sys
import PIL.Image
from PIL import ImageTk, Image
import PIL.Image
import imageio
import threading
import qrtools
from PIL import Image
#from pyzbar.pyzbar import decode
import pyzbar.pyzbar as pyzbar
import mysql.connector

main = Tk()
main.title("QRIntegrity -  Ensuring Integrity via Blockchain QR")
main.attributes('-fullscreen', True)
#main.geometry('1300x1200')

ifQRSCANNED=[]
video_name = "bg\\Home_main.mp4" 
video = imageio.get_reader(video_name)

def stream(label):

    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.config(image=frame_image)
        label.image = frame_image

my_label = tkinter.Label(main)
my_label.pack()
thread = threading.Thread(target=stream, args=(my_label,))
thread.daemon = 1
thread.start()

  
global filename
blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def authenticateProduct():
    text.delete('1.0', END)
    filename_ = askopenfilename(initialdir = "original_barcodes")
    
    #qr=qrtools.QR()
    #qr.decode(filename_)
    image = cv2.imread(filename_)
    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        digital_signature_=obj.data
        digital_signature=digital_signature_.decode("utf-8")
    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            ifQRSCANNED.append(arr[0])
            # print(ifQRSCANNED + "yeh hai")
            if arr[5] == digital_signature:
                mydb = mysql.connector.connect(
                host="localhost",
                user="yash",
                password="123456",
                database="reg1"
                )
                mycursor = mydb.cursor()
                print(arr[0] + " here is the ")
                mycursor.execute("SELECT owner FROM curr_owner where pid = %s", [arr[0]])
                myresult = mycursor.fetchall()
                output = ''
                text.insert(END,"Uploaded Product Barcode Authentication Successfull\n")
                text.insert(END,"Details extracted from Blockchain after Validation\n\n")
                text.insert(END,"Product ID                                 : "+arr[0]+"\n")
                text.insert(END,"Product Name                               : "+arr[1]+"\n")
                text.insert(END,"Company/User Details                       : "+arr[2]+"\n")
                text.insert(END,"Address Details                            : "+arr[3]+"\n")
                text.insert(END,"Product registered Date & Time             : "+arr[4]+"\n")
                text.insert(END,"Product QR-Code                            : "+str(digital_signature)+"\n")
                text.insert(END,"Current Owner the product                  : " + str(myresult[0][0]))


                output='<html><body><table border=1>'
                output += '<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th><th>Product QR-Code No</th></tr>'
                output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+str(digital_signature)+'</td></tr>'
                f = open("output.html", "w")
                f.write(output)
                f.close()
                # webbrowser.open("output.html",new=1)
                flag = False
                break
    if flag:
        text.insert(END,str(digital_signature)+", This Product is Fake \n")
        text.insert(END,"Uploaded Product Barcode Authentication Failed")
# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;
def changeowner():
    text.delete('1.0', END)
    if(len(ifQRSCANNED)==0):
        text.insert(END, "NO QR SCANNED")
    else:
        mydb = mysql.connector.connect(
        host="localhost",
        user="yash",
        password="123456",
        database="reg1"
        )
        mycursor = mydb.cursor()
        mycursor.execute("update curr_owner set owner = %s where pid = %s;", (tf2.get(), ifQRSCANNED[-1]))
        # myresult = mycursor.fetchall()
        # print(myresult)
        mydb.commit()
        mydb.close()
        text.insert(END, "New owner of this product is :" + str(tf2.get()))

def authenticateProductWeb():
    text.delete('1.0', END)
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        digital_signature = None
        for obj in decodedObjects:
            digital_signature_=obj.data
            digital_signature=digital_signature_.decode("utf-8")
            print(digital_signature)
            break
        if(digital_signature):
            break
        cv2.imshow("QR-Code scanner", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            ifQRSCANNED.append(arr[0])
            if arr[5] == digital_signature:
                mydb = mysql.connector.connect(
                host="localhost",
                user="yash",
                password="123456",
                database="reg1"
                )
                mycursor = mydb.cursor()
                # print(arr[0] + " here is the ")
                mycursor.execute("SELECT owner FROM curr_owner where pid = %s", [arr[0]])

                myresult = mycursor.fetchall()
                print(myresult)
                output = ''
                text.insert(END,"Uploaded Product Barcode Authentication Successfull\n")
                text.insert(END,"Details extracted from Blockchain after Validation\n\n")
                text.insert(END,"Product ID                   : "+arr[0]+"\n")
                text.insert(END,"Product Name                 : "+arr[1]+"\n")
                text.insert(END,"Company/User Details         : "+arr[2]+"\n")
                text.insert(END,"Address Details              : "+arr[3]+"\n")
                text.insert(END,"Scan Date & Time             : "+arr[4]+"\n")
                #text.insert(END,"Product Qr code              : "+str(bytes) +"\n")
                text.insert(END,"Product QR-Code              : "+str(digital_signature)+"\n")
                text.insert(END,"Current Owner                : "+ str(myresult[0][0]))
                output='<html><body><table border=1>'
                output += '<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th><th>Product digital Signature</th></tr>'
                output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+str(digital_signature)+'</td></tr>'
                f = open("output.html", "w")
                f.write(output)
                f.close()
                # webbrowser.open("output.html",new=1)
                flag = False
                break
    if flag:
        text.insert(END,str(digital_signature)+",  this hash is not present in the blockchain \n")
        text.insert(END,"Uploaded Product Barcode Authentication Failed")
        
        
 
    
    

main.wm_attributes('-transparentcolor', '#ab23ff')
font = ('times', 30, 'bold')
title = Label(main, text='QRIntegrity -  Ensuring Integrity via Blockchain QR')
title.config(bg='black', fg='white')  
title.config(font=font)           
title.config(height=3, width=50)       
title.place(x=170,y=5)

font1 = ('times', 13, 'bold')


def run12():
    main.destroy()
    import Main
    

scanButton = Button(main, text="Home Page", bg="dark orange", command = run12)
scanButton.place(x=1400,y=200)
scanButton.config(font=font1)

scanButton = Button(main, text="Authenticate Scan", command=authenticateProduct)
scanButton.place(x=420,y=300)
scanButton.config(font=font1)

scanButton = Button(main, text="Change Owner",bg="blue", command=changeowner)
scanButton.place(x=1400,y=500)
scanButton.config(font=font1)

tf2 = Entry(main,width=30)
tf2.config(font=font1)
tf2.place(x=1530,y=504)

scanButton = Button(main, text="Authenticate web Scan", command=authenticateProductWeb)
scanButton.place(x=850,y=300)
scanButton.config(font=font1)

font1 = ('times', 13, 'bold')
text=Text(main,height=15,width=100)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=300,y=450)
text.config(font=font1)

main.config(bg='cornflower blue')
main.mainloop()
