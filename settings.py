from dotenv import load_dotenv
import sys
import os

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
load_dotenv()

load_dotenv(verbose=True)
