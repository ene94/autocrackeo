import os
from pprint import pprint

try:
  from tkinter import *
  from tkinter import filedialog
  from tkinter import scrolledtext as st

  # modules to open autocrackeo in a new thread without blocking the tkinter GUI
  import threading
  from subprocess import Popen, PIPE
except ImportError as e:
  print(" [X] Module import failed: " + str(e))


# START GUI PROGRAM
root = Tk()
root.title("Autocrackeo GUI")
# TODO DESIGN AUTOCRACKEO ICON
#root.iconbitmap("D:\\proyects\\programming\\guis\\logo.ico") 

# --------- global variables -------------------------------------------------------------------------

#   Frame for input form
frame_args = Frame(root, width=150)
frame_args.pack(pady=5, padx=50)
frame_opts = Frame(root, width=150)
frame_opts.pack(pady=5, padx=50)
frame_buttons = Frame(root, width=150)
frame_buttons.pack(pady=5, padx=50)

#   Input fields
input_m = Entry(frame_args, width=100)
input_i = Entry(frame_args, width=100)
input_I = Entry(frame_args, width=100)
input_w = Entry(frame_args, width=100)
input_o = Entry(frame_args, width=100)
input_a = Entry(frame_args, width=100)
input_e = Entry(frame_opts, width=100)
entry_cmd = st.ScrolledText(root, width=100, height=5)

# ---------- My Methods ------------------------------------------------------------------------------

# clean data
def clean_data():
  input_m.delete(0, END)
  input_m.insert(0, "")
  input_i.delete(0, END)
  input_i.insert(0, "")
  input_w.delete(0, END)
  input_w.insert(0, "")
  input_o.delete(0, END)
  input_o.insert(0, "")
  input_a.delete(0, END)
  input_a.insert(0, "")
  input_e.delete(0, END)
  input_e.insert(0, "")

# Set example data
def set_example_data():

  autocrackeo_dir = os.path.abspath(os.path.dirname(__file__)) # get directory of this script location: ...\autocrackeo

  input_m.delete(0, END)
  input_m.insert(0, "1000")
  input_i.delete(0, END)
  input_i.insert(0, "\"" + os.path.join(autocrackeo_dir, "docs", "test_files", "ntlm.hash") + "\"")
  input_w.delete(0, END)
  input_w.insert(0, "\"" + os.path.join(autocrackeo_dir, "docs", "test_files", "custom.dic") + "\"")
  input_o.delete(0, END)
  input_o.insert(0, "\"" + os.path.join(autocrackeo_dir, "docs", "test_files", "results") + "\"")
  input_a.delete(0, END)
  input_a.insert(0, "\"quick_test\"")
  input_e.delete(0, END)
  input_e.insert(0, "\"--username\"")

# Select file path
def select_file_get_path(input_field):
  autocrackeo_dir = os.path.normpath(os.path.dirname(__file__))
  filename = filedialog.askopenfilename(initialdir=autocrackeo_dir, title="select file path")
  filename = os.path.normpath(filename)
  input_field.delete(0,END)
  input_field.insert(0,"\"" + filename + "\"")

# Select dir path
def select_dir_get_path(input_field):
  autocrackeo_dir = os.path.normpath(os.path.dirname(__file__))
  dirname = filedialog.askdirectory(initialdir=autocrackeo_dir, title="select dir path")
  dirname = os.path.normpath(dirname)
  input_field.delete(0,END)
  input_field.insert(0,"\"" + dirname + "\"")

# Generate selected command text
def show_command():

  m = input_m.get()
  i = input_i.get()
  w = input_w.get()
  o = input_o.get()
  a = input_a.get()
  e = input_e.get()
  f = feedback.get()
  v = verbose.get()
  
  autocrackeo_dir_path = os.path.abspath(os.path.dirname(__file__)) # get directory of this script location
  autocrackeo_path = os.path.join(autocrackeo_dir_path, "autocrackeo.py")

  #cmd = "python3 " + autocrackeo_path + " -m " + m + " -i " + i + " -w " + w + " -o " + o + " -a " + a + " -e=\"" + e + "\""
  cmd = "python3 " + autocrackeo_path

  if m:
    cmd += " -m " + m
  if i:
    cmd += " -i " + i
  if w:
     cmd += " -w " + w
  if o:
     cmd += " -o " + o
  if a:
     cmd += " -a " + a
  if e:
     cmd += " -e=" + e
  if f == "1":
    cmd += " --feedback"
  if v == "1":
    cmd += " --verbose"

  # write in the text box
  entry_cmd.delete("0.0",END)
  entry_cmd.insert("0.0",cmd)

  return cmd

# execute command read from text box
def exec_command():
  cmd = entry_cmd.get(0.0, END).strip()

  os.system("echo [*] " + cmd) # show
  # os.system(cmd) # exec
  # run process in a thread to avoid blocking gui
  t = threading.Thread(target=exec_in_thread)
  t.start()

def exec_in_thread():
  cmd = entry_cmd.get(0.0, END).strip()

  p = Popen(cmd,  universal_newlines=True)
  # print('process created with pid: {}'.format(p.pid))
  # TODO show results ¿?



# --------- Rest of the view components ---------------------------------------------------------

# Command parameter label and inputs
label1 = Label(frame_args, text="Main execution parameters:")
label1.grid(row=0, column=0, columnspan=2, pady=20)

# hash type
label_m = Label(frame_args, text="Hash type (-m): ")
label_m.grid(row=1, column=0, sticky=E)
input_m.grid(row=1, column=1)

# hash file
label_i = Label(frame_args, text="Hash file (-i): ")
label_i.grid(row=2, column=0, sticky=E)
input_i.grid(row=2, column=1)
button_i = Button(frame_args, text=" ... ", command=lambda:select_file_get_path(input_i), width=5)
button_i.grid(row=2, column=2)
# hash file list
'''
label_I = Label(frame_args, text="Hash files (-I): ")
label_I.grid(row=3, column=0, sticky=E)

input_I.grid(row=3, column=1)
'''

# custom wordlist
label_w = Label(frame_args, text="Custom wordlist (-w): ")
label_w.grid(row=4, column=0, sticky=E)
input_w.grid(row=4, column=1)
button_w = Button(frame_args, text=" ... ", command=lambda:select_file_get_path(input_w), width=5)
button_w.grid(row=4, column=2)

# output dir
label_o = Label(frame_args, text="Output dir (-o): ")
label_o.grid(row=5, column=0, sticky=E)
input_o.grid(row=5, column=1)
button_o = Button(frame_args, text=" ... ", command=lambda:select_dir_get_path(input_o), width=5)
button_o.grid(row=5, column=2)

# attacks config
label_c = Label(frame_args, text="Attacks file (-a all): ")
label_c.grid(row=6, column=0, sticky=E)
input_a.grid(row=6, column=1)

# Other parameter options

label1 = Label(frame_opts, text="Other options:")
label1.grid(row=0, column=0, columnspan=2, pady=20)

# extra params
label_e = Label(frame_opts, text="Extra params (-e): ")
label_e.grid(row=1, column=0, sticky=E)
input_e.grid(row=1, column=1)

# feedback
feedback = StringVar()
check_feedback = Checkbutton(frame_opts, text="Feedback (--feedback): ",
  variable=feedback)
check_feedback.deselect()
check_feedback.grid(row=2, column=1)

# verbose
verbose = StringVar()
check_verbose = Checkbutton(frame_opts, text="Verbose (--verbose): ",
  variable=verbose)
check_verbose.select()
check_verbose.grid(row=3, column=1)

# clean data button:
clean_button = Button(frame_buttons, text="Clean input data", command=clean_data)
clean_button.grid(row=1, column=1)

# ONLY FOR DEVELPMENT:
# set defaults button:
examples_button = Button(frame_buttons, text="Set example data", command=set_example_data)
examples_button.grid(row=1, column=2)

# show command button:
my_button = Button(frame_buttons, text="Show command", command=show_command)
my_button.grid(row=2, column=1)

# show command button:
exec_button = Button(frame_buttons, text="Execute command", command=exec_command)
exec_button.grid(row=2, column=2)

# scroll text for command copy
entry_cmd.pack(pady=20)

'''
TODO: help + version menu

'''


root.mainloop()