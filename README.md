# Conversor de USD a ARS para WhatsApp
Convierte tanto audio como texto a ARS tomando en cuenta el valor de dolar tarjeta en el momento

Este proyecto es un bot de WhatsApp construido en Flask que permite a los usuarios enviar mensajes o archivos de audio para convertir dólares estadounidenses (USD) a pesos argentinos (ARS) utilizando la API de Together AI y la biblioteca Whisper de OpenAI para transcribir el audio. También utiliza la API de Twilio para gestionar la comunicación por WhatsApp.

**Usa dolar Tarjeta para hacer la conversion, en cualquier caso se puede cambiar desde la variable dolartarjetaApi**
https://dolarapi.com/docs/argentina/

## Requerimientos
- Python 3.8 o superior
- Paquetes especificados en requirements.txt

### Variables de entorno:
- togetherApiKey: clave de API para Together AI.
- TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN: autenticación de Twilio para gestionar mensajes de audio.


## Funcionamiento del Código
Endpoint /whatsapp: El bot responde a mensajes de WhatsApp que pueden contener texto o archivos de audio. En el caso de mensajes de audio, el bot:

Descarga el archivo mediante la API de Twilio.
Lo transcribe a texto utilizando el modelo de Whisper de OpenAI.

### Lógica de Conversión:

Usa la API de Together AI para interpretar si el mensaje contiene una solicitud de conversión de moneda. En caso afirmativo, extrae el monto en USD.
Llama a la API de dolarapi.com para obtener el valor actual del dólar y realiza el cálculo correspondiente.
Mensajes de Respuesta:

Si se detecta un monto en USD en el mensaje, responde con la conversión de USD a ARS.
Si no se detecta un monto, responde con un mensaje informativo indicando cómo el usuario puede solicitar la conversión.

## Estructura del Código

Importaciones: El código importa varias bibliotecas necesarias para manejar las solicitudes HTTP, procesamiento de archivos, y transcripción de audio.
Variables de Entorno: togetherApiKey, TWILIO_ACCOUNT_SID, y TWILIO_AUTH_TOKEN

## Ejecución
Para ejecutar el proyecto en modo local:

python main.py
El servidor estará en funcionamiento en http://127.0.0.1:5000 y podrás probar el bot en la plataforma configurada en Twilio.

*Para poder probarlo recomiendo usar ngrok*
