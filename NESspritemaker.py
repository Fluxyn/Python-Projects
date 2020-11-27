from tkinter import *
from tkmacosx import Button
from tkinter.filedialog import asksaveasfile

_2C02palette = ['#484848', '#000858', '#000878', '#000870', '#380050', '#580010', '#580000', '#400000', '#100000', '#001800', '#001E00', '#00230A', '#001820', '#000000', '#080808', '#080808', '#A0A0A0', '#0048B8', '#0830E0', '#5818D8', '#A008A8', '#D00058', '#D01000', '#A02000', '#604000', '#085800', '#006800', '#006810', '#006070', '#080808', '#080808', '#080808', '#F8F8F8', '#20A0F8', '#5078F8', '#9868F8', '#F868F8', '#F870B0', '#F87068', '#F88018', '#C09800', '#70B000', '#28C020', '#00C870', '#00C0D0', '#282828', '#080808', '#080808', '#F8F8F8', '#A0D8F8', '#B0C0F8', '#D0B0F8', '#F8C0F8', '#F8C0E0', '#F8C0C0', '#F8C8A0', '#E8D888', '#C8E090', '#A8E8A0', '#90E8C8', '#90E0E8', '#A8A8A8', '#080808', '#080808']
palette = []
color_number = 0
mode = 'draw'

counter = 0
for c in _2C02palette:
    globals()[hex(counter)] = c
    counter += 1

class ColorPalettePicker:
    def __init__(self, master):
        global palette
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        frame=Frame(master, bg = 'black')
        frame.grid(row=0, column=0, sticky=N+S+E+W)
        def contrasting_color(hex_str):
            (r, g, b) = hex_str[1:2], hex_str[3:5], hex_str[5:]
            luminance = (1 - (int(r, 16) * 0.299 + int(g, 16) * 0.587 + int(b, 16) * 0.114) / 255)
            if luminance < 0.5:
                return '#000000'
            else:
                return '#ffffff'
        def btn_click(num, idnum):
            palette.append(num)
            btn_ids[idnum].config(state="disabled")
        color = 0
        btn_ids = []
        for row_index in range(4):
            Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(16):
                Grid.columnconfigure(frame, col_index, weight=1)
                btn = Button(frame, bg=_2C02palette[color], text=hex(color), fg=contrasting_color(_2C02palette[color]), borderless = 1, font='GB18030Bitmap', command=lambda txt=hex(color), idn=color: btn_click(txt, idn))
                btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)
                color += 1
                btn_ids.append(btn)
        while True:
            master.update()
            if len(palette) == 3:
                master.destroy()
                break

root1 = Tk()
root1.title('Color Palette Picker')
root1.geometry('600x100')
def donothing():
    pass
root1.protocol("WM_DELETE_WINDOW", donothing)
app = ColorPalettePicker(root1)
root1.mainloop()

class PixelEditor:
    def __init__(self, master):
        global palette
        tiles = []
        bin_tiles = []
        for _ in range(8):
            bin_tiles.append(['0', '0', '0', '0', '0', '0', '0', '0'])
        def callback(event, mode):
            col_width = c.winfo_width()/8
            row_height = c.winfo_height()/8
            col = event.x//col_width
            row = event.y//row_height
            try:
                if mode == 'draw':
                    c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=globals()[palette[color_number]], outline='')
                    bin_tiles[int(row)][int(col)] = str(color_number+1)
                else:
                    c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill='white', outline='')
                    bin_tiles[int(row)][int(col)] = '0'
            except:
                pass
        frame1=Frame(master)
        frame1.pack(side=TOP)
        c = Canvas(frame1, width=200, height=200, borderwidth=0, background='white')
        c.pack()
        key = 'B1-Motion'
        c.bind(('<'+key+'>'), lambda event: callback(event, 'draw'))
        c.bind(('<Command-'+key+'>'), lambda event: callback(event, 'erase'))
        button_frame = Frame(master, height=200)
        button_frame.pack(fill=X)
        def change_color(colnum):
            global color_number
            color_number = colnum
        def new():
            c.delete('all')
            palette.clear()
            tiles.clear()
            bin_tiles.clear()
            for _ in range(8):
                tiles.append([None, None, None, None, None, None, None, None])
                bin_tiles.append(['0', '0', '0', '0', '0', '0', '0', '0'])
            top = Toplevel()
            top.title('Color Palette Picker')
            top.geometry('600x100')
            def donothing():
                pass
            top.protocol("WM_DELETE_WINDOW", donothing)
            app = ColorPalettePicker(top)
            color1.config(bg=globals()[palette[0]], command=lambda: change_color(0))
            color2.config(bg=globals()[palette[1]], command=lambda: change_color(1))
            color3.config(bg=globals()[palette[2]], command=lambda: change_color(2))
        def save():
            final = []
            for a in bin_tiles:
                for b in a:
                    final.append(b)
            bin_final = []
            for i in final:
                binary = str(bin(int(i))[2:])
                if binary == '0':
                    bin_final.append('0'+binary)
                elif binary == '1':
                    bin_final.append('0'+binary)
                else:
                    bin_final.append(binary)
            tmp1 = ''.join([i[0] for i in bin_final])
            sprite1 = [tmp1[i:i+8] for i in range(0, len(tmp1), 8)]
            tmp2 = ''.join([i[1] for i in bin_final])
            sprite2 = [tmp2[i:i+8] for i in range(0, len(tmp2), 8)]
            sprite1 = [hex(int(i, 2)) for i in sprite1]
            sprite2 = [hex(int(i, 2)) for i in sprite2]
            finalhexsprite = sprite1 + sprite2
            file = asksaveasfile(mode ='wb', defaultextension='*.bin')
            if file != None:
                file.write(bytes([int(x, 16) for x in finalhexsprite]))
                file.close()
        color1 = Button(button_frame, height=20, width=30, borderless = 1, bg=globals()[palette[0]], command=lambda: change_color(0))
        color1.pack(side=LEFT)
        color2 = Button(button_frame, height=20, width=30, borderless = 1, bg=globals()[palette[1]], command=lambda: change_color(1))
        color2.pack(side=LEFT)
        color3 = Button(button_frame, height=20, width=30, borderless = 1, bg=globals()[palette[2]], command=lambda: change_color(2))
        color3.pack(side=LEFT)
        newbtn = Button(button_frame, text='New', height=20, width=50, borderless = 1, command=new)
        newbtn.pack(side=RIGHT)
        savebtn = Button(button_frame, text='Save', height=20, width=50, borderless = 1, command=save)
        savebtn.pack(side=RIGHT)

root2 = Tk()
root2.title('Pixel Editor')
root2.geometry('200x235')
root2.resizable(False, False)
app = PixelEditor(root2)
root2.mainloop()

