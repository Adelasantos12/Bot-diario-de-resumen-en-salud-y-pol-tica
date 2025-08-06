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
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    # Manejo de errores
    if r.status_code != 200:
        print("🔴 Error al conectar con OpenAI:", r.status_code)
        print("🧾 Respuesta:", r.text)
        return "Error al obtener el resumen."

    try:
        return r.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        print("⚠️ Error al procesar la respuesta de OpenAI:", e)
        print("Respuesta cruda:", r.text)
        return "Error al procesar la respuesta del modelo."

def enviar_resumen():
    resumen = obtener_resumen()
    mensaje = f"📰 *Resumen del día ({datetime.now().strftime('%d/%m/%Y')})*\n\n{resumen}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    enviar_resumen()
