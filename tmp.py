from pynput.keyboard import Key, Controller
import time
import pyautogui

keyboard = Controller()
time.sleep(2)

pyautogui.key('w')
time.sleep(10)
pyautogui.keyUp('w')

