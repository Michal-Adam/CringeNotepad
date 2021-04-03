from tkinter import *
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)
root = Tk()
root.state("zoomed")
root.title("CringeNotepad")

headingFont = font.Font(family="Terminal", size=20, weight="bold")
textFont = font.Font(family="Helvetica", size=12, weight="normal")
fontList = ["Helvetica", *font.families()]
sizeList = ["8", "9", "10", "11", "12", "14", "16", "18", "20", "22", "24", "26", "28", "36", "48", "72"]
currentWeightColor = "#ee3e3e"
currentSlantColor = "#ee3e3e"


def new():
    question = messagebox.askyesno("Do you wish to proceed", "Any unsaved progress will be lost!")
    if question:
        notePad.delete(1.0, END)
    else:
        return


def save():
    saveFileQ = filedialog.asksaveasfile(filetypes=(("txt files", ".txt"), ("all files", "*.*")),
                                         defaultextension=".txt")
    if saveFileQ is None:
        return
    notePadInput = str(notePad.get(1.0, END))
    saveFileQ.write(notePadInput)
    saveFileQ.close()


def load():
    question = messagebox.askyesno("Do you wish to proceed", "Any unsaved progress will be lost!")
    if question:
        openFileQ = filedialog.askopenfile()
        if openFileQ is None:
            return
        else:
            notePad.delete(1.0, END)
            for line in openFileQ:
                notePad.insert(END, line)
        openFileQ.close()
    else:
        return


def theme(col1, col2, col3, col4):
    root.configure(bg=col1)
    mainLabel.configure(bg=col1, fg=col2)
    notePad.configure(bg=col3, fg=col4)
    mainFrame.configure(bg=col1)


def font_click(fontpicker, familyvalue, sizevalue):
    fontpicker.destroy()
    if familyvalue not in fontList:
        warningFamily = messagebox.showerror(title="Not a valid Font!", message="Your specified font couldn't be found")
    textFont.configure(family=familyvalue)
    textFont.configure(size=int(sizevalue))


def color_change(type, typeofbutton):
    global currentWeightColor
    global currentSlantColor
    if textFont[type] == "bold":
        typeofbutton.configure(bg="#ee3e3e")
        textFont.configure(weight="normal")
        currentWeightColor = "#ee3e3e"
    elif textFont[type] == "normal":
        typeofbutton.configure(bg="#63e281")
        textFont.configure(weight="bold")
        currentWeightColor = "#63e281"
    elif textFont[type] == "italic":
        typeofbutton.configure(bg="#ee3e3e")
        textFont.configure(slant="roman")
        currentSlantColor = "#ee3e3e"
    else:
        typeofbutton.configure(bg="#63e281")
        textFont.configure(slant="italic")
        currentSlantColor = "#63e281"


def font_pick():
    fontPicker = Tk()
    fontPicker.title("Font Picker")
    familyComboBox = ttk.Combobox(fontPicker, values=fontList)
    familyComboBox.set(textFont["family"])
    familyComboBox.grid(row=0, column=0)
    sizeComboBox = ttk.Combobox(fontPicker, values=sizeList)
    sizeComboBox.set(textFont["size"])
    sizeComboBox.grid(row=1, column=0)
    weightButton = Button(fontPicker, text="Bold/Normal", bg=currentWeightColor,
                          command=lambda: color_change("weight", weightButton))
    weightButton.grid(row=0, column=1, padx=5)
    slantButton = Button(fontPicker, text="Italic/Roman", bg=currentSlantColor,
                         command=lambda: color_change("slant", slantButton))
    slantButton.grid(row=1, column=1, padx=5)
    familyButton = Button(fontPicker, text="Set Font", command=lambda: font_click(fontPicker, familyComboBox.get(),
                                                                                  sizeComboBox.get()))
    familyButton.grid(row=2, column=0)


mainMenu = Menu(root)

fileMenu = Menu(mainMenu, tearoff=0)
fileMenu.add_command(label="New", command=new)
fileMenu.add_command(label="Save As...", command=save)
fileMenu.add_command(label="Open...", command=load)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.destroy)

themeMenu = Menu(mainMenu, tearoff=0)
themeMenu.add_command(label="Default Theme", command=lambda: theme("#F0F0F0", "black", "white", "black"))
themeMenu.add_command(label="Dark Theme", command=lambda: theme("#191919", "#8d2663", "#2d2d2d", "#ababab"))
themeMenu.add_command(label="Dark Rain Theme", command=lambda: theme("#0C1446", "#2B7C85", "#87ACA3", "#0C1446"))
themeMenu.add_command(label="Emerald Theme", command=lambda: theme("#013A20", "#478C5C", "#478C5C", "#CDD193"))

fontMenu = Menu(mainMenu, tearoff=0)
fontMenu.add_command(label="Font...", command=font_pick)

mainMenu.add_cascade(label="File", menu=fileMenu)
mainMenu.add_cascade(label="Themes", menu=themeMenu)
mainMenu.add_cascade(label="Font", menu=fontMenu)

mainFrame = Frame(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
mainFrame.grid_propagate(False)
mainFrame.pack(side="top", fill="both")
mainFrame.grid_columnconfigure(0, weight=1)
mainFrame.grid_rowconfigure(1, weight=1)

mainLabel = Label(mainFrame, text="CringeNotepad", font=headingFont)
mainLabel.grid(row=0, column=0, sticky="nsew")
notePad = Text(mainFrame, font=textFont, relief="sunken")
notePad.grid(row=1, column=0, sticky="nsew", padx=10)
mainFrame.grid()

root.config(menu=mainMenu)
root.mainloop()
