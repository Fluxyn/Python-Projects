import tkinter as tk, threading
import imageio
from PIL import Image, ImageTk
import time, sys
import playsound
from tkinter.filedialog import askopenfile 

root = tk.Tk()
root.geometry("500x500")
root.configure(bg='black')

filename = None
def openfile():
    global filename
    filename = askopenfile(parent=root, filetypes=[("Video file", ".mp4"),("Video file", ".flv"),("Video file", ".avi"),])
    if filename == None:
        sys.exit()
    
openfile()
try:
    video = imageio.get_reader(filename.name)
except UnicodeDecodeError:
    print('Video Error: Invald Video File')
    sys.exit()

frame_images = []

def playvideo(label):
    for image in video.iter_data():
        image_frame = Image.fromarray(image)          
        frame_image = ImageTk.PhotoImage(image_frame)
        label.config(image=frame_image)
        label.image = frame_image


def playaudio():
    try:
        s_musicfile = filename.name
        s_musicfile = s_musicfile.replace(' ', '%20')
        playsound.playsound(s_musicfile, False)
    except OSError:
        print('Sound Error: Invald Audio')
        sys.exit()

my_label = tk.Label(root)
my_label.pack()

if __name__ == "__main__":
    videothread = threading.Thread(target=playvideo, args=(my_label,))
    videothread.start()
    playaudio()
    root.mainloop()
