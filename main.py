from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import together
import os
import urllib.request
import whisper
import logging
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

togetherApiKey=os.environ.get('togetherApiKey')
print(togetherApiKey)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')  #Twilio auth para descargar el audio
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')    

dolarApi = 'https://dolarapi.com/v1/dolares/tarjeta'

def dolarTarjeta(monto_usd):
    dolarRequest = requests.get(dolarApi)
    dolarData = dolarRequest.json()
    dolar = dolarData['venta']
    return dolar * monto_usd

client = together.Client(api_key=togetherApiKey)

def interpretar_mensaje_together_ai(mensaje_entrante):
    # Llama a la API de Together AI para analizar el mensaje
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {"role": "system", "content": "Eres un asistente que ayuda a convertir USD a ARS."},
            {"role": "user", "content": f"Sos un convertidor de ARS y USD, Necesito que entiendas el mensaje para saber si se esta hablando de una conversion de monedas. En caso de que si, necesito que respondas sola y unicamente con el monto. Ejemplo: 'Necesito convertir 180 dolares' contestar solo con '180', el mensaje es el siguiente: '{mensaje_entrante}'"}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    respuesta = MessagingResponse()
    mensaje = respuesta.message()

    num_media = int(request.form.get('NumMedia', 0))

    if num_media > 0:
        media_url = request.form.get('MediaUrl0')
        media_content_type = request.form.get('MediaContentType0')


        # Verifica si el contenido es un archivo de audio
        if 'audio' in media_content_type:
            try:
                audio_filename = 'audio_message.ogg'  # Asegurarse de la extension

                response = requests.get(
                    media_url,
                    auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                )               #Descarga el audio con la auth de twilio

                if response.status_code == 200:
                    with open(audio_filename, 'wb') as f:
                        f.write(response.content)
                else:
                    error_message = f"Error al descargar el archivo de audio: {response.status_code} {response.reason}"
                    mensaje.body("Hubo un error al descargar tu mensaje de audio.")
                    return str(respuesta)

                model = whisper.load_model("base") 

                result = model.transcribe(audio_filename, language='es')        #Transcribe el audio al español

                mensaje_entrante = result['text'].lower()

                # Elimina el archivo de audio después de procesarlo
                os.remove(audio_filename)
            except Exception as e:
                mensaje.body(f"Hubo un error al procesar tu mensaje de audio: {e}")
                return str(respuesta)
        else:
            mensaje.body("Por favor, envía un mensaje de audio o texto con tu consulta.")
            return str(respuesta)
    else:
        # Cambia el mensaje entrante a lower
        mensaje_entrante = request.form.get('Body').lower()

    # Llama a Together AI para analizar el mensaje y obtener el monto en USD, si se menciona.
    chatgpt_respuesta = interpretar_mensaje_together_ai(mensaje_entrante)

    try:
        monto_usd = float(chatgpt_respuesta)
        monto_ars = dolarTarjeta(monto_usd)
        mensaje.body(f'El dolar esta {dolarTarjeta(1)}, por lo que {monto_usd} USD son {round(monto_ars)} ARS')
    except ValueError:
        # Si ChatGPT no respondió con un número, asume que no era una solicitud de conversión
        mensaje.body("Hola, puedo ayudarte a convertir USD a ARS. Envia un mensaje como '35 USD a ARS'. También puedo responder a preguntas relacionadas.")

    return str(respuesta)

if __name__ == "__main__":
    app.run(debug=True)
