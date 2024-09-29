import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opciones de voz
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id3 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'

# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.5

        # informar que comenzo la grabacion
        print('ya puedes hablar')

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language='ES-MX')

            # prueba de que pudo ingresar
            print('Dijiste: ' + pedido)

            #devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print('ups, no entendi')

            # devolver error
            return 'sigo esperando'

        # en caso de no resolver el audio
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print('ups, no hay servicio')

            # devolver error
            return 'sigo esperando'


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id3)

    # pronunciar el mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():

    # crear variable con daots de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con los dias de la semana
    calendario = {0: 'Lunes',
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # decir el dia de la semana
    hablar(f'hoy es: {calendario[dia_semana]}, {dia}')


# informar que hora es
def pedir_hora():

    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'Iván, en este momento son las {hora.hour} hora con {hora.minute} minutos, hoy {hora.date()}'
    print(hora)

    # decir la hora
    hablar(hora)


# Saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas Tardes'

    # decir el saludo
    hablar(f'{momento}, Soy Nieve, tu asistente personal, '
           f'por favor dime en que te puedo ayudar Iván')


# funcion central de asistente
def pedir_cosas():

    # activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop while
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        # activar el micro y guardar el pedido en un string

        if 'abrir cursos' in pedido:
            hablar('Claro, es hora de seguir aprendiendo')
            webbrowser.open('https://www.udemy.com/course/python-total/learn/lecture/29685024#content')
        elif 'abrir youtube' in pedido:
            hablar('Claro, para que veas cualquier cosa')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'qué dia es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar(f'wikipedia dice lo siguiente: {hablar(resultado)}')
            continue
        elif 'busca en internet' in pedido:
            hablar('En eso estoy')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('eso fue lo que encontre en internet')
            continue
        elif 'reproducir' in pedido:
            hablar('Va, ya te lo busco en youtube')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'ggogle': 'GOOGL'}

            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:

                hablar('Perdón, pero no la he encontrado')
                continue
        elif 'mandar whatsapp' in pedido:
            hablar('¿Qué le quieres mandar?')
            pedido = pedido.replace('mandar whatsapp','')
            pywhatkit.sendwhatmsg_instantly('+528119091733', 'hola, como estas')
            hablar('Listo ya se lo envie')
            continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, dime si necesitas algo mas')
            break


pedir_cosas()

















