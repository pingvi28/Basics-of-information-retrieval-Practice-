import customtkinter
import webbrowser

def open_link(link):
    print(link)
    webbrowser.open(link)

class app_frame(customtkinter.CTkScrollableFrame):
    labels = []

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def add_new(self, links):
        for label in self.labels:
            label.destroy()
        self.labels = []
        for i in range(0, len(links)):
            link = links[i]
            label = customtkinter.CTkButton(master=self, text=link, command=lambda: open_link(link))
            label.grid(row=len(self.labels), column=0, padx=20)
            self.labels.append(label)