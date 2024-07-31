from typing import Final
import json
import google.generativeai as genai
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from telegram._replykeyboardmarkup import ReplyKeyboardMarkup, KeyboardButton
from geopy.geocoders import Nominatim

TOKEN: Final = '6993107338:AAEW4znT1DkoVRKHc1uFb7RdBFdiWgS8NHE'
USUARIO_BOT: Final = '@JDJ_DeltoBot'

GeminiAPIKEY: Final = 'AIzaSyB59Ckx9p8LEuSE6ScZ5VQ6BLtMGEojTxo'

genai.configure(api_key=GeminiAPIKEY)

conversacion = {}


# Funciones

def cargar_datos_usuarios():
    try:
        with open('datos_usuarios.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def guardar_datos_usuarios(datos_usuarios):
    with open('datos_usuarios.json', 'w') as f:
        json.dump(datos_usuarios, f)


def obtener_clima(update: Update, context: CallbackContext, datos: dict):
    descripcion = datos['weather'][0]['description']
    temperatura = datos['main']['temp']
    sensacion = datos['main']['feels_like']
    temp_min = datos['main']['temp_min']
    temp_max = datos['main']['temp_max']
    humedad = datos['main']['humidity']

    soleado = ['clear sky', 'few clouds']

    nublado = ['scattered clouds', 'broken clouds']

    lluvioso = ['shower rain', 'rain', 'thunderstorm']

    if descripcion.lower() in soleado:
        recomendacion = f"Hoy es un hermoso día soleado en {update.message.text}."
    elif descripcion in nublado:
        recomendacion = (
            f"El día hoy en {update.message.text} está un poco nublado. No salgas a tomar sol, ¡no te vas a "
            f"broncear!")
    elif descripcion in lluvioso:
        recomendacion = f"¡Agarra un paraguas, hoy llueve en {update.message.text}!"
    elif descripcion == "snow":
        recomendacion = "¡Esta nevando! ¡A hacer angelitos de nieve!"
    else:
        recomendacion = "Cuidado si conduces, hay mucha niebla."

    if temp_min < 15:
        recomendacion += " Abrígate, ¡va a estar frío!"
    elif temp_min > 20:
        recomendacion += " No te olvides de hidratarte, ¡hace calor!"

    mensaje = (
        f"Clima en {update.message.text}:\n\n"
        f"Descripcion: {descripcion}\n"
        f"Temperatura: {temperatura}°C\n"
        f"Sensación térmica: {sensacion}°C\n"
        f"Min: {temp_min}°C  Max: {temp_max}°C\n\n"
        f"Humedad: {humedad}%\n"
        f"\n"
        f"{recomendacion}\n"
        f"\n"

    )

    return mensaje


def guardar_mensaje(usuario_id, mensaje, remitente):
    if usuario_id not in conversacion:
        conversacion[usuario_id] = []

    conversacion[usuario_id].append({'remitente': remitente, 'mensaje': mensaje})


# Comandos
async def start(update: Update, context: CallbackContext):
    # Teclado
    boton1 = KeyboardButton('¡Quiero saber el clima!')
    boton2 = KeyboardButton('¡Quiero contar!')
    boton3 = KeyboardButton('Enviar chat a IA')
    boton4 = KeyboardButton('Obtener contador')
    boton5 = KeyboardButton('Quiero cocinar algo')
    botones = [boton1, boton2, boton3, boton4, boton5]
    teclado1 = ReplyKeyboardMarkup([botones])

    usuario_id = str(update.message.from_user.id)
    datos_usuarios = cargar_datos_usuarios()

    if usuario_id not in datos_usuarios:
        datos_usuarios[usuario_id] = {
            'contador': 0,
        }

    guardar_datos_usuarios(datos_usuarios)

    guardar_mensaje(usuario_id, update.message.text, 'usuario')

    respuesta = 'Hola. Esta es la prueba tecnica de Juan Diego Jacques.\n\n¿Qué necesitas?'

    guardar_mensaje(usuario_id, respuesta, 'bot')

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=respuesta,
                                   reply_markup=teclado1)


# Handlers
flag_conv: int = 0


async def handle_mensaje(update: Update, context: CallbackContext):
    global flag_conv
    text: str = update.message.text
    usuario_id = str(update.message.from_user.id)
    datos_usuarios = cargar_datos_usuarios()
    localizador = Nominatim(user_agent="MyApp")
    print(f'Usuario {usuario_id} envio el siguiente mensaje: {text}')
    respuesta: str

    if text == '¡Quiero saber el clima!':
        guardar_mensaje(usuario_id, text, 'usuario')
        respuesta = "Ingrese la ciudad de la cual desea saber el clima."
        flag_conv = 1

    elif text == '¡Quiero contar!':
        guardar_mensaje(usuario_id, text, 'usuario')
        datos_usuarios[usuario_id]['contador'] += 1

        guardar_datos_usuarios(datos_usuarios)

        respuesta = 'Su contador ha sido incrementado'
        flag_conv = 0

    elif text == 'Enviar chat a IA':
        guardar_mensaje(usuario_id, text, 'usuario')
        modelo = genai.GenerativeModel('gemini-pro')
        r = modelo.generate_content(
            f'Analiza el sentimiento de esta conversacion. Clasificala como positiva, negativa o neutral y dame una '
            f'breve explicacion\n'
            f'\n'
            f'{conversacion}')
        respuesta = r.text
        flag_conv = 0

    elif text == "Obtener contador":
        guardar_mensaje(usuario_id, text, 'usuario')
        contador = datos_usuarios[usuario_id]["contador"]
        respuesta = f"Su contador es: {contador}"
        flag_conv = 0

    elif text == "Quiero cocinar algo":
        guardar_mensaje(usuario_id, text, 'usuario')
        respuesta = "Ingrese los ingredientes que tiene en su casa y/o que tipo de comida quiere comer."
        flag_conv = 2

    else:
        if flag_conv == 1:
            guardar_mensaje(usuario_id, text, 'usuario')
            ubicacion = localizador.geocode(text)
            latitud = round(ubicacion.latitude, 4)
            longitud = round(ubicacion.longitude, 4)

            api_url = "https://api.openweathermap.org/data/2.5/weather"
            params = {'lat': latitud, 'lon': longitud, 'appid': '9216f2e29fa7f9b5bed2764a4ed082ab', 'units': 'metric'}

            r = requests.get(api_url, params=params)
            datos = r.json()
            flag_conv = 0

            if r.status_code == 200:
                respuesta = obtener_clima(update, context, datos)

                modelo = genai.GenerativeModel('gemini-pro')
                adicional = modelo.generate_content(
                    f'Proporciona una respuesta creativa (sugerencias según el clima e información interesante de la '
                    f'ciudad) para el siguiente mensaje:\n{respuesta}. Es para un mensaje de Telegram')
                respuesta += adicional.text

            else:
                respuesta = f'No se encontró su ciudad.'
        elif flag_conv == 2:
            guardar_mensaje(usuario_id, text, 'usuario')
            modelo = genai.GenerativeModel('gemini-pro')
            r = modelo.generate_content(f'Quiero cocinar algo. Tengo estos ingredientes. {text}. ¿Me puedes dar una '
                                        f'receta?')
            respuesta = r.text
            flag_conv = 0

        else:
            guardar_mensaje(usuario_id, text, 'usuario')
            respuesta = f'No entiendo su mensaje.'

    guardar_mensaje(usuario_id, respuesta, 'bot')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} ha causado el siguiente error {context}')


# Ejecucion
if __name__ == '__main__':
    print('Iniciando bot...')

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('iniciar', start))

    app.add_handler(MessageHandler(filters.TEXT, handle_mensaje))

    app.add_error_handler(error)

    print('Buscando interacciones...')
    app.run_polling(poll_interval=3)
