import requests
import os
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def obtener_resumen():
    prompt = (
        "Dame un resumen actualizado de las principales noticias de hoy en el mundo y en México "
        "sobre gobernanza sanitaria, sistemas de salud, leyes sanitarias y temas políticos relevantes. "
        "Formato claro, lenguaje científico, sin redundancias."
    )
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return r.json()["choices"][0]["message"]["content"]

def enviar_resumen():
    resumen = obtener_resumen()
    mensaje = f"📰 *Resumen del día ({datetime.now().strftime('%d/%m/%Y')})*\n\n{resumen}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
