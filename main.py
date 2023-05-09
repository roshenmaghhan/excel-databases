import customtkinter
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import pyperclip
from peewee import *
import database_handler as dh
import remote_db_handler as rh
from models import *
from tkinter.messagebox import askyesno
import time, threading

'''
GUI for file list frame
'''
class FileListFrame(customtkinter.CTkScrollableFrame):
    
    file_mapping = {} # Maps : obj_instance -> file_name
    id_mapping = {} # Maps : file_name -> unique_id
    
    # Constructor
    def __init__(self, master, **kwargs):
        
        # Checks if file_list attribute exists
        self.file_list = kwargs["file_list"]
        kwargs.pop("file_list")

        self.id_mapping = kwargs["id_mapping"]
        kwargs.pop("id_mapping")

        super().__init__(master, **kwargs)

        # Builds the initial file list
        self.build_file_list(file_list=self.file_list)

    # Builds the file list
    def build_file_list(self, file_list, type="BUILD") :
        for idx, i in enumerate(file_list) : 
            u_id = self.id_mapping[i]

            ctkframe = customtkinter.CTkFrame(self, width=570, height=80, fg_color=("#5B5B5B", "#5B5B5B"))
            upl_lbl_file = customtkinter.CTkLabel(ctkframe, text=f"FILE NAME : {os.path.basename(i)}", text_color="#e5e5e5", font=("Songti TC", 15))
            upl_lbl_uid = customtkinter.CTkLabel(ctkframe, text=f"UNIQUE ID : {u_id}", text_color="#e5e5e5", font=("Songti TC", 15))
            cpy_btn = customtkinter.CTkButton(master=ctkframe, text="COPY ID", fg_color="#1abc9c", hover_color="#27ae60",  command=lambda cont = ctkframe : self.copy_uid(cont))
            cpy_btn.place(x=490, y=57.5, anchor=tkinter.CENTER)             
            del_button = customtkinter.CTkButton(master=ctkframe, text="DELETE", fg_color="#e74c3c", hover_color="#c0392b", command=lambda cont = ctkframe : self.delete_file(cont))
            del_button.place(x=490, y=22.5, anchor=tkinter.CENTER)
            upl_lbl_file.place(x=20, y=15)
            upl_lbl_uid.place(x=20, y=35)
            row_idx = idx if type == "BUILD" else (len(self.file_list) - 1)
            self.file_mapping[ctkframe] = i
            ctkframe.grid(row=row_idx * 2, column=0, padx=10, pady=10)

    # Updates the file list
    def update_file_list(self, new_file) :
        self.id_mapping.update(new_file)
        self.build_file_list([self.file_list[len(self.file_list) - 1]], type="UPDATE")

    # Deletes files removed by user
    def delete_file(self, obj) :
        file_name = self.file_mapping[obj]
        ans = askyesno(title='confirmation', message=f"Are you sure you want to delete {os.path.basename(file_name)}? Deleting this entry would result in this table being deleted as well.")
        if ans : 
            self.file_list.remove(file_name)
            del_id = self.id_mapping.pop(file_name)
            for k, v in self.file_mapping.items() :
                k.destroy()
            self.file_mapping = {}
            FileList.get(FileList.filepath == file_name).delete_instance()
            FileLogging.get(FileLogging.file_id == del_id).delete_instance()
            trh = rh.RemoteDB(del_id, file_name)
            trh.delete_table()
            self.build_file_list(file_list=self.file_list)

    # Copy Unique ID
    def copy_uid(self, obj) :
        file_name = self.file_mapping[obj]
        u_id = self.id_mapping[file_name]
        pyperclip.copy(u_id)

'''
Main GUI
'''
class App(customtkinter.CTk):

    auth_token = ""
    file_list = []
    id_mapping = {}

    def __init__(self, token, file_list):
        super().__init__()
        self.auth_token = token
        self.file_list = list(file_list.keys())
        self.id_mapping = file_list

        width = 700
        height = 780
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.title("Excel Databases")

        # Heading of the page
        auth_token = tkinter.StringVar()
        auth_token.set(f"AUTH TOKEN : {self.auth_token}")
        self.tkn_btn = customtkinter.CTkButton(self, text="COPY AUTH TOKEN", fg_color="#E5E5E5", text_color="#5b5b5b", hover_color="#999999", command=self.copy_token)
        self.heading = customtkinter.CTkLabel(self, text=auth_token.get(), text_color="#e5e5e5",font=("Copperplate", 20))
        self.heading.grid(row=0, column=0, padx=0, pady=(30,0))
        self.tkn_btn.grid(row=1, column=0, padx=0, pady=(15, 30))
        
        # Drag and drop frame
        self.frame = customtkinter.CTkFrame(self, width=600, height=300)
        self.frame.grid(row=2, column=0, padx=50, pady = 0)

        # Contents within drag and drop frame
        self.file_label_string = customtkinter.StringVar()
        self.file_label_string.set("SELECT A FILE FROM DIRECTORY")

        file_label = customtkinter.CTkLabel(self.frame, textvariable=self.file_label_string, text_color="#e5e5e5", font=("Copperplate", 15))
        file_label.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        self.button_upload = customtkinter.CTkButton(master=self.frame, text="SELECT FILE", state="normal", command=self.upload_file)
        self.button_upload.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        image1 = Image.open("upload.png")
        image1 = image1.resize((80, 80), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        label1 = customtkinter.CTkLabel(self.frame, image=test, text="")
        label1.image = test
        label1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        # Uploaded files heading
        heading_upl = customtkinter.CTkLabel(self, text="UPLOADED FILES : ", text_color="#e5e5e5",font=("Copperplate", 20))   
        heading_upl.grid(row=3, column=0, padx=0, pady = 30)

        # Frame for uploaded files content
        self.my_frame = FileListFrame(master=self, width=600, height=200, file_list=self.file_list, id_mapping=self.id_mapping)
        self.my_frame.grid(row=4, column=0, padx=20, pady=0)

    '''
    Uploads the file
    '''
    def upload_file(self, event=None) :
        filename = filedialog.askopenfilename()
        if filename :
            file_path, file_extension = os.path.splitext(filename)
            if file_extension not in ['.parquet', '.csv', '.xlsx', '.xls'] :
                tkinter.messagebox.showinfo(title="File type not supported", message="This file type isn't supported. Only .parquet, .csv and .xlsx are allowed.")
                return

            if filename in self.file_list :
                tkinter.messagebox.showinfo(title="Duplicate File Found", message="This file has already been tracked, please enter a different file.")
                return

            self.file_list.append(filename)
            filename_trunc = os.path.basename(filename)
            self.file_label_string.set(f"Uploading {filename_trunc} ...")
            self.button_upload.configure(state="disabled")
            
            res_uid = th.insert_file_upload(f_path=filename)
            trh = rh.RemoteDB(res_uid, filename)
            populate = trh.populate_table() #DONE: Check if values are properly populated
            
            if populate: #DONE : Delete entry if db population failed
                self.file_label_string.set("SELECT A FILE FROM DIRECTORY")
                self.button_upload.configure(state="normal")
                self.my_frame.update_file_list({filename : res_uid})
                th.insert_file_timestamp(file_id=res_uid, file_path=filename)
                self.id_mapping[filename] = res_uid
            else : # If it failed to populate
                th.delete_by_id(res_uid)

            return
        
    '''
    Monitors for a local update
    '''
    def monitor_local_update(self) :
        fs = FileLogging.select()
        for i in fs : 
            file_path = i.filepath
            last_update = i.file_update_time
            id = i.file_id
            cur_update = str(os.stat(file_path).st_ctime)
            
            print(f"{id} , {last_update}")

            if cur_update != last_update : 
                rh.RemoteDB(table_name=id, file=file_path).update_table()
                i.file_update_time = cur_update
                i.save()

        self.after(1000, self.monitor_local_update)
    
    '''
    Copies the auth token,
    onto clipboard
    '''
    def copy_token(self) :
        pyperclip.copy(self.auth_token)

th = dh.TableHandler()
file_list = th.get_file_uploads()
app = App(token=th.auth_token, file_list=file_list)
app.monitor_local_update()
app.mainloop()