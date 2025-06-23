import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import openpyxl
import  classe as cl


root=tk.Tk()
root.geometry("800x600")
root.resizable(False,False)
root.configure(bg="#2E3440")  # Couleur de fond sombre
root.title("DeskMarks")
logo=tk.PhotoImage(file="C:\\Users\\hadem\\OneDrive\\Images\\Deskmarks.png")
root.iconphoto(False,logo)

excel_file_location =''
#Pour appliquer un thème sombre à la fenêtre
style=ttk.Style(root)
root.tk.call("source","forest-dark.tcl")
root.tk.call("source","forest-light.tcl")
style.theme_use("forest-dark")


combo_list=["AS","ISE"]
classes={"AS":["AS1","AS2","AS3"],"ISE":["ISEP1","ISEP2","ISEP3","ISE_MATHS","ISE-ECO"]}

#On crée des cadres pour séparer nos parties
frame=ttk.Frame(root)
frame.pack()



widget_frame=ttk.LabelFrame(frame,text="Champs")
widget_frame.grid(row=0,column=0,padx=20,pady=15,sticky="ns")


#Pour ajouter un widget dans le widget_frame

#Pour mettre une entrée pour le fichier excel
def browse_file():
    filetypes = (
        ('Fichiers Excel/CSV', '*.xlsx *.xls *.csv'),
        ('Tous les fichiers', '*.*')
    )
    filename = filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=filetypes)
    
    if filename:  # Si un fichier a été sélectionné
        if filename.lower().endswith(('.xlsx', '.xls', '.csv')):
            excel_doc_entry.delete(0, tk.END)
            excel_doc_entry.insert(0, filename)
            excel_file_location = filename.replace('/', '//')  # Remplacer les '/' par des '//'
            print(f"Fichier sélectionné : {excel_file_location}")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier Excel ou CSV")

def read_excel_doc():
    selected_doc=excel_doc_entry.get()
    df_sheets={}
    xls_file=None
    if not os.path.isfile(selected_doc):
        messagebox.showerror(title="Erreur",message="Erreur! Fichier introuvable")
    else:
        try:
            if selected_doc.lower().endswith(('.xlsx','.xls')):
                xls_file = pd.ExcelFile(selected_doc)
                feuilles = xls_file.sheet_names
                sheets["values"] = feuilles
                sheets.set("Choisir une feuille")
            else:
                df = pd.read_csv(selected_doc)
                df_sheets={"CSV": df}
                sheets["values"] = list(df_sheets[df])
                sheets.set("CSV")
                select_sheet()
            messagebox.showinfo(title="Info",message="Votre fichier a été chargé avec succès")
        except:
            messagebox.showerror(title="Erreur",message="Impossible de lire le fichier, veuillez réessayer !")

def select_sheet():
    selected_file=excel_doc_entry.get()
    if selected_file.lower().endswith(('.xlsx','.xls')):
        df=pd.read_excel(selected_file,sheet_name=sheets.get())
    else:
        df=pd.read_csv(selected_file)
    treeview.delete(*treeview.get_children())
    treeview["columns"]=list(df.columns)
    treeview["show"]="headings"
    for colmn in df.columns:
        treeview.heading(colmn,text=colmn)
        treeview.column(colmn,anchor="center")
    for _, row in df.iterrows():
        treeview.insert("","end",values=list(row))
    
ma_variable = tk.StringVar()
excel_doc_entry=ttk.Entry(widget_frame,textvariable=ma_variable)
excel_doc_entry.insert(0,"Entrez un fichier excel/CSV")
excel_doc_entry.bind("<FocusIn>",lambda a:excel_doc_entry.delete('0','end'))
excel_doc_entry.grid(row=0,column=0,padx=5,pady=5,sticky="ew")
browse=ttk.Button(widget_frame,text="Parcourir",command=browse_file)
browse.grid(row=1,column=0,padx=5,pady=5)


pursue=ttk.Button(widget_frame,text="Poursuivre",command=read_excel_doc)
pursue.grid(row=2,column=0,padx=5,pady=5)

separator1=ttk.Separator(widget_frame)
separator1.grid(row=3,column=0,padx=5,pady=10,sticky="ew")

#Donner son prénom
firstname_entry=ttk.Entry(widget_frame)
firstname_entry.insert(0,"Prénom")
firstname_entry.bind("<FocusIn>",lambda e:firstname_entry.delete('0','end'))
firstname_entry.grid(row=4,column=0,sticky="ew",padx=5,pady=5)

#Donner son nom de famille
lastname_entry=ttk.Entry(widget_frame)
lastname_entry.insert(0,"Nom")
lastname_entry.bind("<FocusIn>",lambda e:lastname_entry.delete('0','end'))
lastname_entry.grid(row=5,column=0,sticky="ew",padx=5,pady=5)

#Donner sa filière
def select_class(event):
    selected_field=field_combobox.get()
    class_list=classes.get(selected_field,[])
    class_combobox["values"]=class_list


field_combobox=ttk.Combobox(widget_frame,values=combo_list,state="readonly")
field_combobox.insert(0,"Filière")
field_combobox.current(0)
field_combobox.bind("<<ComboboxSelected>>",select_class)
field_combobox.grid(row=6,column=0,sticky="ew",padx=5,pady=5)

#Donner sa classe
class_combobox=ttk.Combobox(widget_frame, values=[])
class_combobox.insert(0,"Classe")
class_combobox.grid(row=7,column=0,sticky="ew",padx=5,pady=5)

# Pour envoyer les messages via WhatsApp
def sen_message():
    send=cl.WhatsAppBot(ma_variable.get())
    send.send_message()

#Créer un bouton
button=ttk.Button(widget_frame,text="Envoyer",command=sen_message)
button.grid(row=8,column=0,padx=5,pady=5)

separator2=ttk.Separator(widget_frame)
separator2.grid(row=9,column=0,padx=5,pady=10,sticky="ew")

def Toggle_mode():
    if switch.instate(['selected']):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")

switch=ttk.Checkbutton(widget_frame,text="Thème",style="Switch",command=Toggle_mode)
switch.grid(row=10,column=0,padx=5,pady=5,sticky="nsew")

treeframe=ttk.Frame(frame)
treeframe.grid(row=0,column=1,pady=10)
treeScroll=ttk.Scrollbar(treeframe)
treeScroll.pack(side="right",fill="y")


treeview=ttk.Treeview(treeframe,yscrollcommand=treeScroll.set,height=13)
treeview.pack(expand=True)
treeScroll.config(command=treeview.yview)


sheets=ttk.Combobox(treeframe)
sheets.pack(expand=True)
sheets.bind("<<ComboboxSelected>>",lambda a:select_sheet())





root.mainloop()
