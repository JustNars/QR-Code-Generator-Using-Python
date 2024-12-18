from customtkinter import *
import pyqrcode, os, png, random
from PIL import Image

set_appearance_mode("dark")

class MainApp(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("550x300")
        self.resizable(False, False)
        self.title("QR Code Generator!")
        self.iconbitmap(None)

        self.main_frame = CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, expand=True, fill="both")

        self.type = None
        self.dict = {"Color": None, "Text": None, "directory": None, "onoff": None}

        # this func just creates a folder call QR Codes
        self.make_directory()

        # show main widgets
        self.show_widgets()

    def show_widgets(self):
        for children in self.main_frame.winfo_children():
            children.destroy()

        title_label = CTkLabel(self.main_frame, text=f"QR Code Generator!", font=("Roboto", 25), text_color="white")
        title_label.pack(side="top", pady=5)

        self.entry_widget = CTkEntry(self.main_frame, corner_radius=10, placeholder_text="Enter An URL", placeholder_text_color="white",
                                height=50, width=345, font=("Roboto", 15))
        self.entry_widget.pack(side="top", pady=20)

        self.name_entry = CTkEntry(self.main_frame, corner_radius=10, placeholder_text="Enter An Name", placeholder_text_color="white",
                                height=30, width=150, font=("Roboto", 15))
        self.name_entry.place(x=85, y=125)

        self.combo_box = CTkComboBox(self.main_frame, values=[".png", ".svg", ".eps"], command=self.type_file,font=("Roboto", 15),
                                     corner_radius=10, height=30, width=150)
        self.combo_box.place(x=275, y=125)

        # button
        self.get_code_button = CTkButton(self.main_frame, text="Create!", fg_color="#575858", text_color="white", command=self.check,
                                    height=35, width=300, font=("Roboto", 20), hover_color="#3E3F3F")
        self.get_code_button.pack(side="top", pady=45)

    
    # this just shows the code if the user wants to
    def show_code(self):
        show_code_window = CTkToplevel(self)
        show_code_window.title(self.name)
        show_code_window.geometry("500x500")
        show_code_window.resizable(False, False)

        qr_code_img = CTkImage(Image.open(f"{self.qr_codes_path}\\{self.name}{self.type}"), size=(500, 500))

        display_img = CTkLabel(show_code_window, text="", image=qr_code_img)
        display_img.pack(side="top")


    def type_file(self, i):
        self.type = i

    def show_qr_code_widgets(self):
        for children in self.main_frame.winfo_children():
            children.destroy()

        # labels
        self.text_label = CTkLabel(self.main_frame, text=self.dict["Text"], font=("JetBrains Mono", 50), text_color=self.dict["Color"])
        self.dir_label = CTkLabel(self.main_frame, text=self.dict["directory"], font=("Roboto", 20), text_color="white")
        self.text_label.pack(side="top", pady=20)
        self.dir_label.pack(side="top")

        # buttons
        return_to_menu_button = CTkButton(self.main_frame, text="Return", command=self.show_widgets, fg_color="#575858",
                                          text_color="white", height=35, width=150, font=("Roboto", 20), hover_color="#3E3F3F")
        return_to_menu_button.place(x=85, y=185)

        self.show_code_button = CTkButton(self.main_frame, text="Show Code", command=self.show_code, fg_color="#575858",
                                          text_color="white", height=35, width=150, font=("Roboto", 20), hover_color="#3E3F3F", state=self.dict["onoff"])
        self.show_code_button.place(x=255, y=185)

    # this func checks if the user typed anything. if not then it will yell at the user
    def check(self):

        # stores the input before the widgets gets deleted
        self.url = self.entry_widget.get()
        self.name = f"QRCODE_{str(random.randint(25, 185))}" if not self.name_entry.get() else self.name_entry.get()

        if not self.url:
            self.dict["Color"] = "#BE2530"
            self.dict["Text"] = "Failed"
            self.dict["directory"] = "Enter a valid Url."
            self.dict["onoff"] ="disabled"

        else:
            self.dict["Color"] = "#25BE35"
            self.dict["Text"] = "Successful"
            self.dict["directory"] = f"Directory: {self.qr_codes_path}\nName: {self.name}"
            self.dict["onoff"] ="normal"

            # make the image
            self.save_img()

        self.show_qr_code_widgets()


    def make_directory(self):
        self.qr_codes_path = os.path.join(os.path.expanduser("~"), "Pictures", "QR Codes")
        print(self.qr_codes_path)

        if not os.path.exists(self.qr_codes_path):
            os.makedirs(self.qr_codes_path, exist_ok=True)
    
    # this func will make the qr code
    def save_img(self):
        try:
            code = pyqrcode.create(self.url)

            match self.type:
                case ".eps":
                    code.eps(f"{self.qr_codes_path}\\{self.name}.eps", scale=8)
                case ".svg":
                    code.svg(f"{self.qr_codes_path}\\{self.name}.svg", scale=8)
                case _:
                    code.png(f"{self.qr_codes_path}\\{self.name}.png", scale=8)
                    self.type = ".png"

        except Exception: self.show_widgets()
            
if __name__ == "__main__":
    MainApp().mainloop()
