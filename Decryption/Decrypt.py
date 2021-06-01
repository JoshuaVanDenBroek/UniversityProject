import io
import os
import PySimpleGUI as sg
from PIL import Image
import os, io
from google.cloud import vision

#-----------------------------------------------------------------------------

def keyword_input():
    layout = [
        [
            sg.Text("Keyword: "),
            sg.Input(size=(25, 1), key="keyword_data"),
            sg.Button("Submit"),
        ],
    ]
    window = sg.Window("Please Enter Your Keyword: ", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Submit":
            global The_Keyword
            The_Keyword = values["keyword_data"]
            The_Keyword = The_Keyword.upper()
            print(The_Keyword)
            window.close()
            file_selection()

#-----------------------------------------------------------------------------

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
def file_selection():
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
        ],
    ]
    window = sg.Window("Image Viewer", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            global FILE_NAME
            FILE_NAME = values["-FILE-"]
            print(FILE_NAME)
            window.close()
            google_vision()

#-----------------------------------------------------------------------------

def google_vision():
    
    print("Google Vision TEST")

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'PERMISSION.json'

    client = vision.ImageAnnotatorClient()

    with io.open(FILE_NAME, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
        
    texts = response.text_annotations

    global testoutput
    testoutput = ""
        
    holder = []
    for text in texts:
        print(text.description)
        holder.append(str(text.description))

    print(holder)
        
    G=1
    while G < len(holder):
        testoutput = testoutput+" "+str(holder[G])
        G=G+1

    print(testoutput)
    
    text_validation()

#-----------------------------------------------------------------------------

def text_validation():
    layout = [
        [
            sg.Text("Ciphertext: "),
            sg.InputText(testoutput, size=(60, 1), key="ciphertext_data"),
            sg.Button("Submit"),
        ],
    ]
    window = sg.Window("Is this text correct? ", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Submit":
            global modified_input
            modified_input = values["ciphertext_data"]
            print(modified_input)
            window.close()
            decrypt()

#-----------------------------------------------------------------------------

def decrypt():  #decryption
    
    layout = [
        [
            sg.Text("Decryption Currently In Progress"),
        ],
    ]
    window = sg.Window("Please Wait...", layout)

    
    Ciphertext = modified_input
    Keyword = The_Keyword

    print(Ciphertext)
    print(Keyword)
 
    KeywordList = list(Keyword) #Keyword converted into list of letters
    KeywordDinaryForm = list()
    KeywordDinaryForm1 = list()
    Counter = 0
    
    for x in KeywordList:
        KeywordDinaryForm.append(ord(x)) #Keyword converted into denary form (ascii) (added to new list)

    for x in KeywordDinaryForm:
        KeywordDinaryForm1.append(x-Counter) #Keyword denary value as counter added each repeat
        Counter -= 1
    KeywordList.clear() #Original keyword list is cleared
    
    for x in KeywordDinaryForm1:
        KeywordList.append(chr(x)) #Keyword converted back into characters from denary

    Keyword = ""

    for x in KeywordList:
        Keyword = Keyword+x

    Cipher2 = list(Ciphertext)

    Cipher3 = list()

    Amount = (len(Cipher2))
    y = 0
    Repeats = 0

    for x in range(len(Keyword)):
        Repeats = Repeats + (ord(Keyword[x])-64)

    while Repeats != 0:
        Repeats = Repeats-1
        Cipher3.clear()

        Amount = (len(Cipher2))
        y = 0

        for x in range(len(Cipher2)):
            if x != Amount:
                if y != len(Keyword)-1:
                    y += 1
                else:
                    y = 0
                Value = (ord(Keyword[y]))
                Temp = (ord(Cipher2[x])-Value)
                if(Temp)<32:
                    while(Temp)<32:
                        Temp = ((Temp-32)+126)
                    Cipher3.append(Temp)
                else:
                    Cipher3.append(ord(Cipher2[x])-Value)         #Here we are taking away the denary value of each keyword character from
                                                            #each of the denary values of the ciphertext characters to obtain the original denary values again
        Cipher2.clear()
        for x in range(len(Cipher3)):
            Cipher2.append(chr(Cipher3[x]))
    
    Cipher4 = list()
    for x in range(len(Cipher3)):
        Cipher4.append(chr(Cipher3[x])) #The new denary values are then converted back into characters (letters) (ascii) again
        
    Cipher5 = list()
    Pos = -2
    done = 0

    while done == 0:
        if Pos == len(Cipher4)-2: #Here we are unscrambling the characters so that we can get the plaintext back
            Pos += 1
            Cipher5.append(Cipher4[Pos])
            done = 1
            while done == 1:
                if Pos == len(Cipher4)-1:
                    Pos -= 2
                    Cipher5.append(Cipher4[Pos]) #Ever other letter is taken and put into a new list
                else:
                    Pos -= 2
                    Cipher5.append(Cipher4[Pos]) #The remaining letters are then added to the end of the new list

                if len(Cipher5) == len(Cipher4):
                    done = 2
        else:
            Pos += 2
            Cipher5.append(Cipher4[Pos]) #However it is still scrambled as we scrambled it twice during encryption
                                         #and have to descramble it twice during decryption to get the plaintext back
    Cipher6 = list()
    Pos = -2
    done = 0
    
    while done == 0:
        if Pos == len(Cipher5)-2:
            Pos += 1
            Cipher6.append(Cipher5[Pos]) #Here is the second set of descrambling
            done = 1
            while done == 1:
                if Pos == len(Cipher5)-1:
                    Pos -= 2
                    Cipher6.append(Cipher5[Pos]) #again every other letter is taken and put into a
                                                 #new list and then the remaining letters are put at the end of the new list
                else:
                    Pos -= 2
                    Cipher6.append(Cipher5[Pos])

                if len(Cipher6) == len(Cipher5):
                    done = 2
        else:
            Pos += 2
            Cipher6.append(Cipher5[Pos]) #At this point the plaintext is back but we still have to remove
                                         #the keyword from the start and the end of the plaintext to make it better for the user when it is outputted
    if(Keyword[-1] != 'X'): #This system fixes the issues with the final plaintext still having the 'X' on the end making it even not odd
        Cipher6.pop()
    else:
        print("Error")

    Plaintext = ""

    for x in Cipher6:
        Plaintext = Plaintext+x

    global Output
    Output = Plaintext
    
    window.close()
    plaintext_output()
    
#-----------------------------------------------------------------------------

def plaintext_output():
    layout = [
        [
            sg.Text("Plaintext: "),
            sg.Text(Output),
            sg.Button("Try Again"),
        ],
    ]
    window = sg.Window("Plaintext Output: ", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Try Again":
            window.close()
            keyword_input()

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    keyword_input()
