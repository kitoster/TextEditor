from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('TextPad')
root.geometry("1200x660")

#Create main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

#Create scroll bar for text box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

#Create text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text.pack()

#Configure our scrollbar
text_scroll.config(command=my_text.yview)

#Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#create new file function
def new_file():
	my_text.delete("1.0", END)
	root.title('New File - TextPad')
	status_bar.config(text="New File     ")

#Open file
def open_file():
	#delete previous text
	my_text.delete("1.0", END) 

	#grab filename 
	text_file = filedialog.askopenfilename(title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
	
	#update status bars
	name = text_file
	status_bar.config(text=f'{name}        ')
	root.title(f'{name} - TextPad')

	#open the file
	text_file = open(text_file, 'r')
	stuff = text_file.read()
	#add file to text box
	my_text.insert(END, stuff)
	#close the opened file
	text_file.close()


#save as file
def save_as_file():
	text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
	if text_file:
		#update status bars
		name = text_file
		status_bar.config(text=f'{name}        ')
		root.title(f'{name} - TextPad')


#add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save")
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#add edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

#add status bar to bottom of app
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

#Create event loop.
root.mainloop()
