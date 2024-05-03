'''
Author: Angus Chapman | u3257979

Last Editied: 1 May 2024

Description:
   GUI app that predicts the cost of diamonds
   using a pretrained decision tree regression model

Requirements:
   Numpy: *
   Tkinter: *
   SKLean: 1.2.2
'''

from sklearn.tree import DecisionTreeRegressor
from tkinter import ttk

import sklearn as sk
import numpy as np

import tkinter
import pickle

CUTS     = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
COLORS   = ["J", "I", "H", "G", "F", "E", "D"]
CLARITYS = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

def load_model(path: str) -> DecisionTreeRegressor:
   with open(path, "rb") as f:
      return pickle.load(f)

def is_float(x: str) -> bool:
   try:
      float(x)

      return True
   except:
      return False

class DiamondGUI:
   def __init__(self) -> None:
      BG = "#F0F0F0"
      FG = "#1F1F1F"

      # Load model
      self.model = load_model("model")

      # Initalise GUI
      self.window = tkinter.Tk()

      ttk.Style().theme_use("alt")

      self.window.title("Diamond Predict")
      self.window.geometry("675x265")
      self.window.resizable(False, False)
      self.window.configure(background = BG)

      # Header
      ttk.Label(
         self.window, 
         text = "Diamond Predict", 
         font = ("Arial 30"), 
         foreground = FG, 
         background = BG
      ).grid(row = 0, column = 0, columnspan = 4)

      # Diamond Image
      self.diaimg = tkinter.PhotoImage(file = "diamond.png")
      ttk.Label(
         self.window, 
         image = self.diaimg, 
         background = BG
      ).grid(row = 1, rowspan = 3, column = 3)

      # Carat
      ttk.Label(
         self.window, 
         text = "Carat: ", 
         font = ("Arial 16"), 
         background = BG, 
         foreground = FG
      ).grid(row = 1, column = 0, sticky = tkinter.SE, pady = 5)

      self.carat_val = tkinter.StringVar(value = "")
      ttk.Entry(
         self.window,
         textvariable = self.carat_val,
         validate = "all", 
         validatecommand = (self.window.register(lambda x: is_float(x) or x == ""), "%P")
      ).grid(row = 1, column = 1, sticky = tkinter.S, pady = 5)

      self.carat_val.trace("w", lambda *_: self.calculate())

      # Cut
      self.cut_val = tkinter.StringVar(value = "Cut")
      ttk.OptionMenu(
         self.window, 
         self.cut_val, 
         "Cut",
         *CUTS
      ).grid(row = 2, column = 0, sticky = tkinter.N)

      self.cut_val.trace("w", lambda *_: self.calculate())

      # Color
      self.color_val = tkinter.StringVar(value = "Color")
      ttk.OptionMenu(
         self.window, 
         self.color_val, 
         "Color",
         *COLORS
      ).grid(row = 2, column = 1, sticky = tkinter.N)

      self.color_val.trace("w", lambda *_: self.calculate())

      # Clarity
      self.clarity_val = tkinter.StringVar(value = "Clarity")
      ttk.OptionMenu(
         self.window, 
         self.clarity_val, 
         "Clarity",
         *CLARITYS
      ).grid(row = 2, column = 2, sticky = tkinter.N)

      self.clarity_val.trace("w", lambda *_: self.calculate())

      # Price
      self.price_val = tkinter.StringVar(value = "$?")
      ttk.Label(
         self.window, 
         textvariable = self.price_val,
         font = ("Arial 30"), 
         foreground = FG, 
         background = BG
      ).grid(row = 3, column = 0, columnspan = 3)

      # Credit
      ttk.Label(
         self.window, 
         text = "Angus Chapman | u3257979",
         font = ("Arial 12"), 
         foreground = FG, 
         background = BG
      ).grid(row = 4, column = 0, columnspan = 1, sticky = tkinter.SE)

      # Start GUI
      tkinter.mainloop()

   def calculate(self) -> None:
      # Check for invalid data
      if (self.carat_val.get()   == "" or 
          self.cut_val.get()     == "Cut" or 
          self.color_val.get()   == "Color" or 
          self.clarity_val.get() == "Clarity"):
         self.price_val.set(f"$?")
         return

      # Parse data
      carat   = float(self.carat_val.get())
      cut     = CUTS.index(self.cut_val.get())
      color   = COLORS.index(self.color_val.get())
      clarity = CLARITYS.index(self.clarity_val.get())

      # Compute price
      price = self.model.predict([[carat, cut, color, clarity]])[0]

      self.price_val.set(f"${price:.2f}")

if __name__ == "__main__":
   DiamondGUI()