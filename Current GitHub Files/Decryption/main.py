from kivy.app import App
#from kivy.uix.button import Button
#from kivy.uix.widget import Widget
#from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os, io
from google.cloud import vision

#List of imports needed for software to function

#from android import activity, mActivity
#from android.permissions import request_permissions, Permission
#from android.storage import primary_external_storage_path
#request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

Builder.load_file('updatelabel.kv') #Connection to Kivy external file

def decrypt():  #decryption
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
    
##------------------------------------------------------------------------------------

class Step1(Screen):
    def press(self):
        input_keyword = self.ids.keyword_data.text
        global The_Keyword
        The_Keyword = input_keyword.upper()
        print(The_Keyword)

##------------------------------------------------------------------------------------

class Step2(Screen):
    def selected(self, filename):
        global FILE_NAME
        FILE_NAME = filename[0]
        print(filename[0])
        try:
            self.ids.my_image.source = filename[0]

        except:
            pass
    
    def googleimage(self, *args):
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

        self.manager.get_screen('Stage3').ids.text_verify.text = testoutput

##------------------------------------------------------------------------------------

class Step3(Screen):
    def text_verification(self):
        print("BIG TEST")
        global modified_input
        modified_input = ""
        modified_input = self.ids.text_verify.text.strip()
        print(modified_input)
        decrypt()
        self.manager.get_screen('Stage4').ids.output_label.text = Output

##------------------------------------------------------------------------------------

class Step4(Screen):
    def output_main(self):
        print("TEST")

##------------------------------------------------------------------------------------

class Decryption_App(App):
    def build(self):
        
        sm = ScreenManager()
        sm.add_widget(Step1(name='Stage1'))
        sm.add_widget(Step2(name='Stage2'))
        sm.add_widget(Step3(name='Stage3'))
        sm.add_widget(Step4(name='Stage4'))

        return sm

if __name__ == '__main__':
    app = Decryption_App()
    app.run()


