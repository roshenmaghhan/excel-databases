import customtkinter
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import uuid
import pyperclip

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

        super().__init__(master, **kwargs)

        # Builds the initial file list
        self.build_file_list(file_list=self.file_list)

    # Builds the file list
    def build_file_list(self, file_list, type="BUILD") :
        for idx, i in enumerate(file_list) : 
            u_id = str(uuid.uuid4().fields[-1])[:5]

            if i in self.id_mapping : 
                u_id = self.id_mapping[i]
            else :
                self.id_mapping[i] = u_id

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
    def update_file_list(self) :
        self.build_file_list([self.file_list[len(self.file_list) - 1]], type="UPDATE")

    # Deletes files removed by user
    def delete_file(self, obj) :
        file_name = self.file_mapping[obj]
        self.file_list.remove(file_name)
        self.id_mapping.pop(file_name)
        for k, v in self.file_mapping.items() :
            k.destroy()
        self.file_mapping = {}
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

    auth_token = "AgdxW2IUdhs"
    file_list = []

    def __init__(self):
        super().__init__()

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
        self.my_frame = FileListFrame(master=self, width=600, height=200, file_list=self.file_list)
        self.my_frame.grid(row=4, column=0, padx=20, pady=0)

    '''
    Uploads the file
    '''
    def upload_file(self, event=None) :
        filename = filedialog.askopenfilename()
        if filename :
            file_path, file_extension = os.path.splitext(filename)
            if file_extension not in ['.parquet', '.csv', '.xlsx'] :
                tkinter.messagebox.showinfo(title="File type not supported", message="This file type isn't supported. Only .parquet, .csv and .xlsx are allowed.")
                return

            if filename in self.file_list :
                tkinter.messagebox.showinfo(title="Duplicate File Found", message="This file has already been tracked, please enter a different file.")
                return

            self.file_list.append(filename)
            filename = os.path.basename(filename)

            # Indicate, and disable file upload
            self.file_label_string.set(f"Uploading {filename} ...")
            self.button_upload.configure(state="disabled")

            self.my_frame.update_file_list()
            return
    
    '''
    Copies the auth token,
    onto clipboard
    '''
    def copy_token(self) :
        pyperclip.copy(self.auth_token)


app = App()
app.mainloop()