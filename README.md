
# WhatsApp Bot - Envoi de Notes

Bot Python pour envoyer automatiquement des notes aux étudiants via WhatsApp depuis un fichier Excel.

## Installation

```bash
pip install pandas selenium openpyxl
```

**Télécharger ChromeDriver :**
- Aller sur [ChromeDriver](https://chromedriver.chromium.org/)
- Télécharger la version correspondant à votre Chrome
- Extraire et noter le chemin vers `chromedriver.exe`

## Configuration

Modifier le chemin vers ChromeDriver dans le code :
```python
chromedriver_path = "C:\\votre\\chemin\\vers\\chromedriver.exe"
```

## Format Excel

Votre fichier Excel doit avoir ces colonnes :

| nom | prénom | numéro | notes |
|-----|--------|--------|-------|
| Diop | Amadou | 701234567 | 15.5 |
| Fall | Fatou | 762345678 | 12.0 |

## Utilisation

```python
from whatsapp_bot import WhatsAppBot

bot = WhatsAppBot("votre_fichier.xlsx")
bot.send_message()
```

## Important

- **Première étape** : Le navigateur s'ouvre sur WhatsApp Web
- **Scanner le QR code** avec votre téléphone (vous avez 100 secondes)
- **Rester connecté** : ne fermez pas le navigateur pendant l'envoi
- **Tester d'abord** avec quelques contacts

## Message type

```
Bonjour Amadou Diop,

Votre note est : 15.5

Cordialement,
L'équipe pédagogique
```

## Durée d'envoi

- 30 secondes par message
- Pour 20 étudiants = ~10 minutes

C'est tout ! 🚀 

En autre l'app permet grace au chatbot de connaitre les stats generasles et permet aussi de visualiser le fichier excel
