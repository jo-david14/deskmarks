import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import info_use as iu
import classe as cl
import getdata_diago as gd
import bot as bt

class DeskMarksApp:
    def __init__(self):
        self.current_user = None
        self.users = {
            "admin": "password",
            "user": "123456",
            "demo": "demo"
        }
        self.init_login_window()
        self.path=''
    
    def init_login_window(self):
        """Initialise la fenêtre de connexion"""
        self.login_root = tk.Tk()
        self.login_root.geometry("400x300")
        self.login_root.resizable(False, False)
        self.login_root.configure(bg="#2E3440")
        self.login_root.title("DeskMarks - Connexion")
        
        try:
            logo = tk.PhotoImage(file="Deskmarks.png")
            self.login_root.iconphoto(False, logo)
        except:
            pass
        
        self.show_login()
    
    def show_login(self):
        """Affiche l'interface de connexion"""
        # Frame principal
        login_frame = ttk.Frame(self.login_root)
        login_frame.pack(expand=True, fill='both')
        
        # Frame central
        form_frame = ttk.LabelFrame(login_frame, text="Connexion", padding=30)
        form_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Titre
        title_label = ttk.Label(form_frame, text="DeskMarks", font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Champs de connexion
        ttk.Label(form_frame, text="Utilisateur:").grid(row=1, column=0, sticky='e', padx=5, pady=10)
        self.username_entry = ttk.Entry(form_frame, width=20)
        self.username_entry.grid(row=1, column=1, padx=5, pady=10)
        
        ttk.Label(form_frame, text="Mot de passe:").grid(row=2, column=0, sticky='e', padx=5, pady=10)
        self.password_entry = ttk.Entry(form_frame, width=20, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=10)
        
        # Bouton de connexion
        login_btn = ttk.Button(form_frame, text="Se connecter", command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Info utilisateurs de test
        info_label = ttk.Label(form_frame, text="Test: admin/password, user/123456, demo/demo", 
                              font=("Arial", 8), foreground="gray")
        info_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.username_entry.focus()
        self.login_root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Gère la connexion"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if username in self.users and self.users[username] == password:
            self.current_user = username
            messagebox.showinfo("Succès", f"Bienvenue {username}!")
            self.login_root.destroy()
            self.init_main_app()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects!")
            self.password_entry.delete(0, tk.END)
    
    def init_main_app(self):
        """Initialise l'application principale avec VOTRE CODE ORIGINAL"""
        # VOTRE CODE ORIGINAL EXACTEMENT
        self.root = tk.Tk()
        self.root.geometry("1200x800")  # Fenêtre plus grande comme demandé
        self.root.resizable(True, True)  # Permettre le redimensionnement
        self.root.configure(bg="#2E3440")
        self.root.title(f"DeskMarks - {self.current_user}")
        
        try:
            logo = tk.PhotoImage(file="Deskmarks.png")
            self.root.iconphoto(False, logo)
        except:
            pass
        
        self.excel_file_location = ''
        
        # Pour appliquer un thème sombre à la fenêtre - VOTRE CODE ORIGINAL
        style = ttk.Style(self.root)
        try:
            self.root.tk.call("source", "forest-dark.tcl")
            self.root.tk.call("source", "forest-light.tcl")
            style.theme_use("forest-dark")
        except:
            pass
        
        # VOS DONNÉES ORIGINALES
        combo_list = ["AS", "ISE"]
        classes = {"AS": ["AS1", "AS2", "AS3"], "ISE": ["ISEP1", "ISEP2", "ISEP3", "ISE_MATHS", "ISE-ECO"]}
        
        # AJOUT DU MENU (NOUVELLE FONCTIONNALITÉ)
        self.create_menu()
        
        # VOTRE CODE ORIGINAL - On crée des cadres pour séparer nos parties
        frame = ttk.Frame(self.root)
        frame.pack(fill='both', expand=True, padx=10, pady=10)  # MODIFIÉ: ajout de fill et expand
        
        widget_frame = ttk.LabelFrame(frame, text="Champs")
        widget_frame.grid(row=0, column=0, padx=20, pady=15, sticky="ns")
        
        # VOTRE CODE ORIGINAL - Pour ajouter un widget dans le widget_frame
        
        # Pour mettre une entrée pour le fichier excel - VOTRE FONCTION ORIGINALE
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
                    self.excel_file_location = filename.replace('/', '//')
                    self.mark='dans le dossier Archives'  
                    print(f"Fichier sélectionné : {self.excel_file_location}")
                else:
                    messagebox.showerror("Erreur", "Veuillez sélectionner un fichier Excel ou CSV")
        
        # VOTRE FONCTION ORIGINALE
        def read_excel_doc():
            selected_doc = excel_doc_entry.get()
            df_sheets = {}
            xls_file = None
            if not os.path.isfile(selected_doc):
                messagebox.showerror(title="Erreur", message="Erreur! Fichier introuvable")
            else:
                try:
                    if selected_doc.lower().endswith(('.xlsx', '.xls')):
                        xls_file = pd.ExcelFile(selected_doc)
                        feuilles = xls_file.sheet_names
                        sheets["values"] = feuilles
                        sheets.set("Choisir une feuille")
                    else:
                        df = pd.read_csv(selected_doc)
                        df_sheets = {"CSV": df}
                        sheets["values"] = list(df_sheets.keys())
                        sheets.set("CSV")
                        select_sheet()
                    messagebox.showinfo(title="Info", message=f"Votre fichier a été chargé avec succès le fichier contenant les statistics aussi {self.mark}")
                except:
                    messagebox.showerror(title="Erreur", message="Impossible de lire le fichier, veuillez réessayer !")
        
        # VOTRE FONCTION ORIGINALE
        def select_sheet():
            selected_file = excel_doc_entry.get()
            if selected_file.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(selected_file, sheet_name=sheets.get())
            else:
                df = pd.read_csv(selected_file)
            treeview.delete(*treeview.get_children())
            treeview["columns"] = list(df.columns)
            treeview["show"] = "headings"
            for colmn in df.columns:
                treeview.heading(colmn, text=colmn)
                treeview.column(colmn, anchor="center")
            for _, row in df.iterrows():
                treeview.insert("", "end", values=list(row))
        
        # VOTRE CODE ORIGINAL EXACT
        ma_variable = tk.StringVar()
        
        excel_doc_entry = ttk.Entry(widget_frame, textvariable=ma_variable)
        excel_doc_entry.insert(0, "Entrez un fichier excel/CSV")
        excel_doc_entry.bind("<FocusIn>", lambda a: excel_doc_entry.delete('0', 'end'))
        excel_doc_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        browse = ttk.Button(widget_frame, text="Parcourir", command=browse_file)

        self.path = excel_doc_entry.get()  # Stocker le chemin du fichier dans l'attribut de classe
        browse.grid(row=1, column=0, padx=5, pady=5)
        
        pursue = ttk.Button(widget_frame, text="Poursuivre", command=read_excel_doc)
        pursue.grid(row=2, column=0, padx=5, pady=5)
        
        separator1 = ttk.Separator(widget_frame)
        separator1.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        
        # Donner son prénom - VOTRE CODE ORIGINAL
        firstname_entry = ttk.Entry(widget_frame)
        firstname_entry.insert(0, "Prénom")
        firstname_entry.bind("<FocusIn>", lambda e: firstname_entry.delete('0', 'end'))
        firstname_entry.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        
        # Donner son nom de famille - VOTRE CODE ORIGINAL
        subject=tk.StringVar()
        lastname_entry = ttk.Entry(widget_frame, textvariable=subject)
        lastname_entry.insert(0, "matiere")
        lastname_entry.bind("<FocusIn>", lambda e: lastname_entry.delete('0', 'end'))
        lastname_entry.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        
        # Donner sa filière - VOTRE CODE ORIGINAL
        def select_class(event):
            selected_field = field_combobox.get()
            class_list = classes.get(selected_field, [])
            class_combobox["values"] = class_list
        
        field_combobox = ttk.Combobox(widget_frame, values=combo_list, state="readonly")
        field_combobox.insert(0, "Filière")
        field_combobox.current(0)
        field_combobox.bind("<<ComboboxSelected>>", select_class)
        field_combobox.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        
        # Donner sa classe - VOTRE CODE ORIGINAL
        class_combobox = ttk.Combobox(widget_frame, values=[])
        class_combobox.insert(0, "Classe")
        class_combobox.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
        
        # Pour envoyer les messages via WhatsApp - VOTRE CODE ORIGINAL
        def sen_message():
            send = cl.WhatsAppBot(ma_variable.get(),subject.get(), field_combobox.get(), class_combobox.get())
            send.send_message()
        
        # Créer un bouton - VOTRE CODE ORIGINAL
        button = ttk.Button(widget_frame, text="Envoyer", command=sen_message)
        button.grid(row=8, column=0, padx=5, pady=5)
        
        separator2 = ttk.Separator(widget_frame)
        separator2.grid(row=9, column=0, padx=5, pady=10, sticky="ew")
        
        # VOTRE FONCTION ORIGINALE
        def Toggle_mode():
            if switch.instate(['selected']):
                style.theme_use("forest-light")
            else:
                style.theme_use("forest-dark")
        
        switch = ttk.Checkbutton(widget_frame, text="Thème", style="Switch", command=Toggle_mode)
        switch.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")
        
        # Logo de l'application - version compacte
        try:
            logo_img = tk.PhotoImage(file="Deskmarks.png")
            # Redimensionner le logo pour qu'il soit petit et discret
            logo_img = logo_img.subsample(4, 4)  # Divise la taille par 4 pour être plus petit
            logo_label = ttk.Label(widget_frame, image=logo_img)
            logo_label.image = logo_img  # Garder une référence pour éviter que l'image soit supprimée
            logo_label.grid(row=11, column=0, padx=5, pady=5, sticky="")  # Moins de padding
        except:
            # Si le logo ne peut pas être chargé, afficher un texte discret
            logo_label = ttk.Label(widget_frame, text="DM", font=("Arial", 8), foreground="gray")
            logo_label.grid(row=11, column=0, padx=5, pady=5)
        
        # MODIFICATION PRINCIPALE ICI - Zone centrale agrandie
        treeframe = ttk.Frame(frame)
        treeframe.grid(row=0, column=1, pady=10, sticky="nsew", padx=(0, 20))  # MODIFIÉ: ajout sticky="nsew"
        
        # MODIFIÉ: Configuration pour que la zone centrale s'étende
        frame.grid_columnconfigure(1, weight=1)  # La colonne 1 (treeframe) prend tout l'espace disponible
        frame.grid_rowconfigure(0, weight=1)     # La ligne 0 s'étend verticalement
        
        treeScroll = ttk.Scrollbar(treeframe)
        treeScroll.pack(side="right", fill="y")
        
        # MODIFIÉ: Suppression de height=13 pour permettre l'expansion
        treeview = ttk.Treeview(treeframe, yscrollcommand=treeScroll.set)
        treeview.pack(fill='both', expand=True)  # MODIFIÉ: ajout de fill='both', expand=True
        treeScroll.config(command=treeview.yview)
        
        sheets = ttk.Combobox(treeframe)
        sheets.pack(fill='x', pady=(5, 0))  # MODIFIÉ: ajout de fill='x' et padding
        sheets.bind("<<ComboboxSelected>>", lambda a: select_sheet())
        
        # Lancer l'application
        self.root.mainloop()
    
    def create_menu(self):
        """Crée la barre de menu - NOUVELLE FONCTIONNALITÉ"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fonctionnalites(en developpemt)", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.logout)
        
        # Menu Outils
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Outils", menu=tools_menu)
        tools_menu.add_command(label="Assistant Q&A", command=self.show_qa_interface)
        tools_menu.add_command(label="info", command=lambda: messagebox.showinfo("Info", "Version 1.0\nDéveloppé par DeskMarks Team :\nMoustapha Diago \n Jonathan.D.Manga \n Anta Ndao"))
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command= iu.create_guide_file)
    
    def show_qa_interface(self):
        """Interface Q&A - NOUVELLE FONCTIONNALITÉ DEMANDÉE"""
        qa_window = tk.Toplevel(self.root)
        qa_window.title("Assistant Q&A")
        qa_window.geometry("600x500")
        qa_window.configure(bg="#2E3440")
        
        # Frame principal
        main_frame = ttk.Frame(qa_window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Assistant Questions & Réponses", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Zone de question
        question_frame = ttk.LabelFrame(main_frame, text="Votre Question")
        question_frame.pack(fill='x', pady=10)
        
        self.question_entry = tk.Text(question_frame, height=3, wrap='word')
        self.question_entry.pack(fill='x', padx=10, pady=10)
        
        # Bouton demander
        ask_btn = ttk.Button(question_frame, text="Poser la question", command=self.process_question)
        ask_btn.pack(pady=5)
        
        # Zone de réponse
        response_frame = ttk.LabelFrame(main_frame, text="Réponse")
        response_frame.pack(fill='both', expand=True, pady=10)
        
        # Text widget avec scrollbar pour la réponse
        response_text_frame = ttk.Frame(response_frame)
        response_text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.response_text = tk.Text(response_text_frame, wrap='word', state='disabled')
        response_scroll = ttk.Scrollbar(response_text_frame, orient='vertical', command=self.response_text.yview)
        self.response_text.configure(yscrollcommand=response_scroll.set)
        
        self.response_text.pack(side='left', fill='both', expand=True)
        response_scroll.pack(side='right', fill='y')
        
        # Focus sur le champ question
        self.question_entry.focus()
    
    def process_question(self):
        """Traite la question et affiche une réponse"""
        question = self.question_entry.get("1.0", tk.END).strip()
        print(self.excel_file_location)
        if not question:
            messagebox.showwarning("Attention", "Veuillez entrer une question!")
            return
        
        # Réponses simples basées sur des mots-clés
        
        handler = bt.get_handler(self.excel_file_location.replace('//','/'), question)

         
        
        # Recherche d'une réponse
        response = "Merci pour votre question!\n\n"
        response+=handler.get_response()
        question_lower = question.lower()
        
        
        
        
        
        # Affichage de la réponse
        self.response_text.config(state='normal')
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert("1.0", response)
        self.response_text.config(state='disabled')
    
    def logout(self):
        """Déconnexion"""
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter?"):
            self.root.destroy()
            self.init_login_window()
            self.login_root.mainloop()
    
    def run(self):
        """Lance l'application"""
        self.login_root.mainloop()

# Lancement de l'application
if __name__ == "__main__":
    app = DeskMarksApp()
    app.run()