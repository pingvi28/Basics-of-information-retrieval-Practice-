from search_system import Search_system
from app_Frame import app_frame
import tkinter
import customtkinter

# CustomTkinter — это библиотека пользовательского интерфейса Python, основанная на Tkinter, которая предоставляет новые,
# современные и полностью настраиваемые виджеты. Они создаются и используются как обычные виджеты Tkinter, а также могут
# использоваться в сочетании с обычными элементами Tkinter.

customtkinter.set_appearance_mode("dark")  # Режимы: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Темы: blue (default), dark-blue, green
app = customtkinter.CTk()  # создайте окно CTk, как вы делаете это с окном Tk
app.title("Demo app: searcher system")
app.geometry("500x400")
x = (app.winfo_screenwidth() - app.winfo_reqwidth()) / 2
y = (app.winfo_screenheight() - app.winfo_reqheight() - 300) / 2
app.wm_geometry("+%d+%d" % (x, y))

@staticmethod
def search_links(self):
    searcher = Search_system()
    links = searcher.search(entry.get())
    links_frame.add_new(links)
    entry.delete('0', tkinter.END)

entry = customtkinter.CTkEntry(app)
entry.place(relx=0.65, y=35, anchor=tkinter.E)
entry.configure(state="normal", height=28, width=305)
entry.bind("<Return>", search_links)

button = customtkinter.CTkButton(master=app, text="Search", command=lambda: search_links(""))
button.place(relx=0.67, y=35, anchor=tkinter.W)

links_frame = app_frame(master=app, width=450, height=310)
links_frame.place(relx=0.5, y=230, anchor=tkinter.CENTER)

app.mainloop() #открытие окна
