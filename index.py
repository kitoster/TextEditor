from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title('TextPad')
root.geometry("1200x660")

#set variable for open file name
global open_status_name
open_status_name = False

global selected
selected = False

#Create a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)


#Create main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

#Create scroll bar for text box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

#Create text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text.pack()

#Configure scrollbar
text_scroll.config(command=my_text.yview)

#Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#create new file function
def new_file():
	my_text.delete("1.0", END)
	root.title('New File - TextPad')
	status_bar.config(text="New File     ")

	global open_status_name
	open_status_name = False

#Open file
def open_file():
	#delete previous text
	my_text.delete("1.0", END) 

	#grab filename 
	text_file = filedialog.askopenfilename(title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
	
	#check to see if there is a file name
	if text_file:
		#filename global so we can access later
		global open_status_name
		open_status_name = text_file


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
		status_bar.config(text=f'Saved: {name}        ')
		root.title(f'{name} - TextPad')

		#save the file
		text_file = open(text_file, 'w')
		text_file.write(my_text.get(1.0, END))
		#close opened file
		text_file.close()

#save file
def save_file():
	global open_status_name
	if open_status_name:
		#save the file
		text_file = open(open_status_name, 'w')
		text_file.write(my_text.get(1.0, END))
		#close opened file
		text_file.close()

		status_bar.config(text=f'Saved: {open_status_name}        ')
	else:
		save_as_file()

#Cut text
def cut_text(e):
	global selected
	if my_text.selection_get():
		#grab selected text from text box
		selected = my_text.selection_get()
		#delete selected text from text box
		my_score.delete("sel.first", "sel.last") #grabs whatever is first and last highlighted and everything in between those

#Cut text
def copy_text(e):
	global selected
	if my_text.selection_get():
		#grab selected text from text box
		selected = my_text.selection_get()

#Cut text
def paste_text(e):
	if selected:
		position = my_text.index(INSERT)
		my_text.insert(position, selected)

#Bold Text
def bold_it():
	#Create font
	bold_font = font.Font(my_text, my_text.cget("font"))
	bold_font.configure(weight="bold")

	#Configure tag
	my_text.tag_configure("bold", font=bold_font)

	#Define current tags
	current_tags = my_text.tag_names("sel.first")

	#If statement to see if tag has been set
	if "bold" in current_tags:
		my_text.tag_remove("bold", "sel.first", "sel.last")
	else:
		my_text.tag_add("bold", "sel.first", "sel.last")

#Italics Test
def italics_it():
	#Create font
	italics_font = font.Font(my_text, my_text.cget("font"))
	italics_font.configure(slant="italic")

	#Configure tag
	my_text.tag_configure("italic", font=italics_font)

	#Define current tags
	current_tags = my_text.tag_names("sel.first")

	#If statement to see if tag has been set
	if "italic" in current_tags:
		my_text.tag_remove("italic", "sel.first", "sel.last")
	else:
		my_text.tag_add("italic", "sel.first", "sel.last")

#Forgoing keyboard bindings for the above functions, works without them. Part 4 went over key bindings, I want to add different ones to learn. 

#add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#add edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False)) #False because we have to pass something
edit_menu.add_command(label="Copy", command=lambda: copy_text(False))
edit_menu.add_command(label="Paste", command=lambda: paste_text(False))
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)") #no binding needed
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")

#add status bar to bottom of app
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

#Set font of bold button
f = font.Font(weight="bold")

#Bold Button
bold_button = Button(toolbar_frame, text="B", command=bold_it)
bold_button['font'] = f
bold_button.grid(row=0, column=0, sticky=W, padx=5)

#Italics Button
italics_button = Button(toolbar_frame, text="I", command=italics_it)
italics_button.grid(row=0, column=1, padx=5)

#Undo/Redo Buttons
undo_button = Button(toolbar_frame, text="Undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)

redo_button = Button(toolbar_frame, text="Redo", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

#Create event loop.
root.mainloop()
