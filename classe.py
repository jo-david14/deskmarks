import pandas as pd 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getdata_diago as gd

class WhatsAppBot:
    def __init__(self, excel_path,matiere,filiere,classe_name):
        self.path = excel_path
        self.df = gd.main(self.path)
        
        self.matiere = matiere
        self.filiere = filiere
        self.classe_name = classe_name
    

    def retrieve_data(self):
        if self.df.empty:
            print("The Excel file is empty.")
            return None
        else:
            print("Data retrieved successfully.")
            number =self.df['numéro']
            marks = self.df['notes']
            name = self.df['nom']
            moyenne=self.df['note_moyenne']
            note_max=self.df['note_max']
            note_min=self.df['note_min']
            first_name = self.df['prénom']
            return number, marks, name, first_name,moyenne,note_max,note_min
        
    def send_message(self):
        try:
            numero=self.retrieve_data()[0]
            notes=self.retrieve_data()[1]
            nom=self.retrieve_data()[2]
            prenom=self.retrieve_data()[3]
            moyenne=self.retrieve_data()[4]
            note_max=self.retrieve_data()[5]
            note_min=self.retrieve_data()[6]

            chromedriver_path = "C:\\Users\\hadem\\Documents\\hackaton\\chromedriver-win64\\chromedriver.exe"
            CHAT_URL = "https://web.whatsapp.com/send?phone={phone}&text&type=phone_number&app_absent=1"
            
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service)
            driver.get("https://web.whatsapp.com/")
            time.sleep(30)


            for i in range(len(numero)):
                    
                    message= f"Bonjour {prenom[i]} {nom[i]} en filiere {self.filiere} et de classe {self.classe_name},\n\nVotre note de {self.matiere} est : {notes[i]}\n\nLa moyenne de la classe est {moyenne[0]}, la note maximale est {note_max[0]} et la note minimale est {note_min[0]}\nCordialement,\nL'équipe pédagogique"

                    print(message)
                    driver.get(CHAT_URL.format(phone=numero[i]))
                    time.sleep(30)
                    
                    
                    #input_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]')
                    input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                    input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
                    input_box.send_keys(message)
                    input_box.send_keys(Keys.ENTER)

                    time.sleep(5)  
            print("Tous les messages ont été envoyés avec succès.")
            driver.quit()

        except Exception as e:
            print(f"Error retrieving data: {e}")
            
            
            