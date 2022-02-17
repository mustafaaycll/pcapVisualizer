from kivy.config import Config
Config.set('graphics', 'resizable', False)

from msilib.schema import SelfReg
from pickle import TRUE
from sqlite3 import Row
from webbrowser import BackgroundBrowser
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from scapy.all import *

def pcapparser(packets):
    print(len(packets))
    print(packets)

class pcapVisualizer(App):
    
    def build(self):
        #Window management
        Window.clearcolor = (0.0705,0.0705,0.0705,1) # values differ in between 0 and 1, #121212 hex color is euqal to rgba(18,18,18,1) and 18 is 7.05 percent of 255

        self.window = GridLayout() # A window consisting of only one column, so every add_widget() adds to next row
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        
        #Attribute declaration
        self.row = GridLayout(cols=2) # Another grid for button allignment, spacing is initially equal to [0,0]: [horizontal,vertical] spacing of children widgets
        self.row.size_hint = (0.6, 0.7)
        self.row.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.filepath = "" # storage of actual file path
        if self.filepath == "":
            self.pathmessage = Label(text="NO FILE SELECTED")
        else:
            self.pathmessage = Label(text=self.filepath) # display message
        
        #Buttons
        self.pick_button = Button(text="SELECT PCAP", bold=True, background_color='#3F88C5', background_normal="")
        self.pick_button.bind(on_press=self.pickFile)

        self.visualize_button = Button(text="VISUALIZE PCAP", size_hint=(0.3,0.3), bold=True, background_color='#00c896', background_normal="")
        self.visualize_button.bind(on_press=self.visualize)

        self.remove_button = Button(text="DESELECT PCAP", size_hint=(0.3,0.3), bold=True, background_color='#E13419', background_normal="")
        self.remove_button.bind(on_press=self.removeFile)

        #Widget Addition
        self.window.add_widget(Image(source="logo.png"))
        self.window.add_widget(self.pathmessage)
        
        #self.row will be changed from 'one children grid' (pick_button) to 'two children grid' (remove and visualize buttons) in accordance
        self.row.add_widget(self.pick_button)
        self.window.add_widget(self.row)
        
        return self.window

    def pickFile(self, instance):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.filepath = askopenfilename(filetypes=[("PCAP files", "*.pcap")])
        if self.filepath != "":
            self.pathmessage.text = "FILE SELECTED: " + self.filepath
            self.window.remove_widget(self.row)
            self.row.spacing = [5,0]
            self.row.remove_widget(self.pick_button)
            self.row.add_widget(self.remove_button)
            self.row.add_widget(self.visualize_button)
            self.window.add_widget(self.row)
        else:
            self.pathmessage.text = "NO FILE SELECTED"

    def removeFile(self, instance):
        self.pathmessage.text = "NO FILE SELECTED"
        self.window.remove_widget(self.row)
        self.row.spacing = [0,0]
        self.row.remove_widget(self.remove_button)
        self.row.remove_widget(self.visualize_button)
        self.row.add_widget(self.pick_button)
        self.window.add_widget(self.row)

    def visualize(self, instance):
        # Main program will work here
        pcapparser(rdpcap(self.filepath))

if __name__ == "__main__":
    pcapVisualizer().run()