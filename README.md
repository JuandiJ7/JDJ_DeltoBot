# Prueba técnica  - DeltoBot  - Juan Diego Jacques
JDJ_DeltoBot es un bot de Telegram diseñado para facilitar tareas cotidianas, como obtener el clima, gestionar un contador personalizado, y proporcionar recetas de cocina basadas en los ingredientes disponibles. Este proyecto es una prueba técnica para demostrar distintas habilidades.

## Tecnologías utilizadas
### Telegram Bot
Se utiliza la API de Telegram para crear y manejar el bot, incluyendo la gestión de comandos y la interfaz de usuario con teclados personalizados.

### Geopy
La biblioteca Geopy se usa para geocodificación, permitiendo convertir nombres de ciudades en coordenadas geográficas.

### OpenWeather API
Se integra la API de OpenWeather para proporcionar información climática precisa basada en las coordenadas geográficas obtenidas.

### Gemini API
La API Gemini se utiliza tanto para generar respuestas adicionales al clima de las ciudades, asi como también para buscar y proporcionar recetas de cocina en base a los ingredientes que los usuarios tienen disponibles y el tipo de comida que desean preparar. A su vez, se encuentra la opción de enviar la conversación para que Gemini analice el sentimiento de la misma y de una breve explicación.

## Funcionalidad adicional
### Recetas de cocina en base a ingredientes
Viendo que la funcionalidad del bot se enfoca más en lo cotidiano, y no tanto en otros aspectos, se implementó una funcionalidad acorde. El botón "Quiero cocinar algo" genera una solicitud por parte del bot, en la que el usuario debe ingresar los ingredientes disponibles en su casa, y el tipo de comida que quiere comer. La API Gemini obtiene esta información y ofrece una receta con los ingredientes y del tipo mencionados.
![image](https://github.com/user-attachments/assets/83f6b298-fde8-4f77-bab1-2a075e78188d)

## Recursos utilizados:
- How To Create A Telegram Bot With Python - YouTube. (2024). En YouTube. Google. https://www.youtube.com/watch?v=NwBWW8cNCP4
- Telegram. (n.d.). ReplyKeyboardMarkup. Telegram Bot API. https://core.telegram.org/bots/api#replykeyboardmarkup
- Telegram. (n.d.). Features. Telegram Bot API. https://core.telegram.org/bots/features
- Python Telegram Bot Tutorial: Demo and Intro #1 | Python project - YouTube. (2024). En YouTube. Google. https://www.youtube.com/watch?v=cX8m3sp_w84
- ArnauCS03. (2024). Weather-Forecast-Telegram-Bot/OpenWeather.py. GitHub. https://github.com/ArnauCS03/Weather-Forecast-Telegram-Bot/blob/main/OpenWeather.py
- OpenWeather. (n.d.). Weather Conditions. OpenWeather. https://openweathermap.org/weather-conditions
