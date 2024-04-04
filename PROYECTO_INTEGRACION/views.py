from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from sentiment_analysis_spanish import sentiment_analysis





def sistema(request):
    if request.method == 'POST' and 'datos' in request.FILES:
        datos = request.FILES['datos']
        textos = [line.decode('utf-8') for line in datos.readlines()]
        
        #Procesamiento de textos por defecto
        textos_procesados = procesar_textos_default(textos)

        #Analisis de sentimientos.
        analisis = analisis_de_sentimiento(textos_procesados)

        #Etiquetado.
        izq = 0.1   #Valor por default
        der = 0.7   #Valor por default
        etiquetas = etiquetar (analisis, izq, der)


        # Prepara los datos para pasar a la plantilla html.
        contexto = {'contenido_tabla': list(zip(textos, textos_procesados, analisis, etiquetas)),
                    'izq': izq,
                    'der': der,
                    'minusculas': True,
                    'stopwords': True,
                    'numeros': True,
                    'signos': True,
                    'urls': False,
                    'correos': False,
                    'emojis': False,
                    'ortografia': False,
                    'lematizacion': True,
                    'Stemming': False
                    }
        # Almacena los datos del contexto en la sesión del usuario
        request.session['datos_contexto'] = contexto

        # Manejo de la carga y la presentación en la misma página.
        return render(request, 'sistema.html', contexto)

            # Verifica si se llamó al botón "modificar rango"
    elif 'modificar_rango' in request.POST:
        # Recupera los datos almacenados en la sesión del usuario
        datos_contexto = request.session.get('datos_contexto', None)
        izq = float(request.POST.get('izqNeutro'))
        der = float(request.POST.get('derNeutro'))

        if der < izq:
            alerta = "Rango Erroneo."
            datos_contexto['alerta'] = alerta
            return render(request, 'sistema.html', datos_contexto)



        textos = [item[0] for item in datos_contexto['contenido_tabla']]
        textos_procesados = [item[1] for item in datos_contexto['contenido_tabla']]
        analisis = [item[2] for item in datos_contexto['contenido_tabla']]
        etiquetas = etiquetar(analisis, izq, der)

        #Datos del contexto que se modifican
        datos_contexto['contenido_tabla'] = list(zip(textos, textos_procesados, analisis, etiquetas))
        datos_contexto['izq'] = izq
        datos_contexto['der'] = der



        request.session['datos_contexto'] = datos_contexto
            # Manejo de la carga y la presentación en la misma página.
        return render(request, 'sistema.html', datos_contexto)
        
    elif 'aplicar_cambios' in request.POST:
        datos_contexto = request.session.get('datos_contexto', None)
        textos = [item[0] for item in datos_contexto['contenido_tabla']]
        textos_procesados = textos
        # Verificar opciones del checkbox
        if 'urls' in request.POST.getlist('limpieza_opciones'):
            textos_procesados = eliminar_urls(textos_procesados)
            datos_contexto['urls'] = True
        else:
            datos_contexto['urls'] = False
        if 'correos' in request.POST.getlist('limpieza_opciones'):
            textos_procesados = eliminar_correos_electronicos(textos_procesados)
            datos_contexto['correos'] = True
        else:
            datos_contexto['correos'] = False
        if 'minusculas' in request.POST.getlist('limpieza_opciones'):
            textos_procesados = convertir_minusculas(textos_procesados)
            datos_contexto['minusculas'] = True
        else:
            datos_contexto['minusculas'] = False
        if 'stopwords' in request.POST.getlist('limpieza_opciones'):
            textos_procesados = eliminar_stopwords(textos_procesados)
            datos_contexto['stopwords'] = True
        else:
            datos_contexto['stopwords'] = False
        if 'numeros' in request.POST.getlist('limpieza_opciones'):
            textos_procesados = eliminar_numeros(textos_procesados)
            datos_contexto['numeros'] = True
        else:
            datos_contexto['numeros'] = False
        if 'signos' in request.POST.getlist('limpieza_opciones'):
            textos_procesados = eliminar_signos(textos_procesados)
            datos_contexto['signos'] = True
        else:
            datos_contexto['signos'] = False
        
        if 'emojis' in request.POST.getlist('limpieza_opciones'):
            textos_procesados =  convertir_emojis(textos_procesados)
            datos_contexto['emojis'] = True
        else:
            datos_contexto['emojis'] = False
        if 'ortografia' in request.POST.getlist('limpieza_opciones'):
            textos_procesados = corregir_ortografia(textos_procesados)
            datos_contexto['ortografia'] = True
        else:
            datos_contexto['ortografia'] = False

        # Verificar si se seleccionó lematización o stemming
        tecnica_normalizacion = request.POST.get('tecnica_normalizacion')

        if tecnica_normalizacion == 'lematizacion':
            # Aplicar lematización a los textos
            textos_procesados = lematizar_textos(textos_procesados)
            datos_contexto['lematizacion'] = True
            datos_contexto['stemming'] = False
        elif tecnica_normalizacion == 'stemming':
            # Aplicar stemming a los textos
            textos_procesados = stemming(textos_procesados)
            datos_contexto['lematizacion'] = False
            datos_contexto['stemming'] = True
        


        #Analisis de sentimientos.
        analisis = analisis_de_sentimiento(textos_procesados)

        #Etiquetado.
        izq = datos_contexto.get('izq', None)
        der = datos_contexto.get('der', None)
        etiquetas = etiquetar (analisis, izq, der)

        datos_contexto['contenido_tabla'] = list(zip(textos, textos_procesados, analisis, etiquetas))

    
        request.session['datos_contexto'] = datos_contexto
            # Manejo de la carga y la presentación en la misma página.
        return render(request, 'sistema.html', datos_contexto)


   
    # Si no hay un archivo cargado o el método de solicitud no es POST, 
    # simplemente renderiza la plantilla de carga de archivo
    return render(request, 'sistema.html')





def procesar_textos_default(textos):

    #Eliminar signos
    textos_procesados = eliminar_signos(textos)

    #Eliminar numeros
    textos_procesados = eliminar_numeros(textos_procesados)

    #Convertir texto a minusculas
    textos_procesados = convertir_minusculas (textos_procesados)
    
    #Eliminación de stopwords
    textos_procesados = eliminar_stopwords(textos_procesados)

    #Lematizacion
    textos_procesados = lematizar_textos(textos_procesados)

    return textos_procesados





def analisis_de_sentimiento(textos):
    sentiment = sentiment_analysis.SentimentAnalysisSpanish()
    # Analiza cada línea de contenido y almacena los resultados
    analisis = [sentiment.sentiment(texto) for texto in textos]
    return analisis


# Limpieza de texto.

#Eliminar signos de puntuación
import re
import string

def eliminar_signos(textos):
    textos_sin_signos = [re.sub(rf'[{string.punctuation}¡¿\\«»°¬]', ' ', texto) for texto in textos]
    return textos_sin_signos


#Eliminar números en el texto
def eliminar_numeros(textos):
    # Eliminar números
    textos_sin_numeros = [re.sub(r'\d+', '', texto) for texto in textos]
    return textos_sin_numeros

#Eliminar URLs
def eliminar_urls(textos):
    # Eliminar URLs de cada texto en la lista
    textos_sin_urls = [re.sub(r'https?://\S+|www\.\S+', '', texto) for texto in textos]
    return textos_sin_urls

#Eliminar direcciones de correo electronico
def eliminar_correos_electronicos(textos):
  
    textos_sin_correos = [re.sub(r'[\w\.-]+@[\w\.-]+(\.[a-zA-Z]+)+', '', texto) for texto in textos]
    return textos_sin_correos


#Convertir el texto a minusculas.   
def convertir_minusculas(textos):
    # Convertir todos los textos a minúsculas utilizando una comprensión de listas
    textos_minusculas = [texto.lower() for texto in textos]
    return textos_minusculas
    

# Convertir emojis a texto
import emoji
def convertir_emojis(textos):
  
    textos_sin_emojis = [ emoji.demojize(texto, language= "es").replace(":"," ").replace("_"," ") for texto in textos]
    return textos_sin_emojis

#Corrector Ortográfico
from autocorrect import Speller
def corregir_ortografia(textos):
    spell = Speller(lang="es")

    textos_corregidos = [spell(texto) for texto in textos]
    return textos_corregidos



#Eliminar palabras vacías (stopwords)
import nltk
from nltk.corpus import stopwords

def eliminar_stopwords(textos):
    nltk.download("punkt")  # Descargar el tokenizador si no está disponible
    nltk.download("stopwords")  # Descargar los recursos necesarios (solo la primera vez)

    stopwords_espanol = set(stopwords.words("spanish"))

    textos_sin_stopwords = []
    for texto in textos:
        tokens = word_tokenize(texto, language='spanish')
        tokens_sin_stopwords = [token for token in tokens if token not in stopwords_espanol]
        texto_sin_stopwords = ' '.join(tokens_sin_stopwords)  # Unir los tokens sin stopwords en un texto
        textos_sin_stopwords.append(texto_sin_stopwords)

    return textos_sin_stopwords



#Tokenización
import nltk
from nltk.tokenize import word_tokenize

def tokenizar_textos(textos):
    nltk.download("punkt")  
    
    textos_tokenizados = []
    for texto in textos:
        tokens = word_tokenize(texto, language='spanish')
        textos_tokenizados.append(tokens)
    
    return textos_tokenizados

#Lematización (Forma canonica de los textos)
import es_core_news_sm
import spacy
pln= es_core_news_sm.load()

def lematizar_textos(textos):
    # Descargar y cargar el modelo pre-entrenado para español
    pln = spacy.load("es_core_news_sm")

    textos_lematizados = []
    for texto in textos:
        # Procesar el texto con Spacy para obtener el objeto doc
        doc = pln(texto)
        # Obtener los lemas de cada token en el texto
        lemas = [token.lemma_ for token in doc]
        # Concatenar los lemas en una cadena
        texto_lematizado = ' '.join(lemas)
        textos_lematizados.append(texto_lematizado)
    return textos_lematizados

#Stemming
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

def stemming(textos):
    nltk.download("punkt")  # Descargar el tokenizador si no está disponible
    stemmer = SnowballStemmer("spanish")
    textos_stemming = []

    for texto in textos:
        # Tokenizar el texto en palabras
        tokens = word_tokenize(texto, language='spanish')

        # Aplicar stemming a cada palabra
        stemmed_tokens = [stemmer.stem(token) for token in tokens]

        # Unir las palabras nuevamente en un texto
        texto_stemmed = " ".join(stemmed_tokens)
        textos_stemming.append(texto_stemmed)

    return textos_stemming


#Etiquetado
def etiquetar(analisis, izq, der):
    etiquetas = []
    #etiquetas = ["positivo" if resultado > 0.7 else "negativo" if resultado < 0.1 else "neutro" for resultado in analisis]

    for resultado in analisis:
        if resultado > der:
            etiquetas.append("positivo")
        elif resultado < izq:
            etiquetas.append("negativo")
        else:
            etiquetas.append("neutro")
            
    return etiquetas





#Descarga de archivos en formatos csv, xml y json
import pandas as pd
import json
import xml.etree.ElementTree as ET

def descargar_archivo(request):
    if request.method == 'POST':
        formato = request.POST.get('formato')

        etiquetas = []
        textos = []

        for clave, valor in request.POST.items():
            if clave.startswith('select_'):
                etiquetas.append(valor)
            elif clave.startswith('texto_'):
                textos.append(valor)
        
        # Crear un DataFrame con los textos y las etiquetas
        data = {'Texto': textos,
                    'Etiqueta': etiquetas}
        df = pd.DataFrame(data)

        # Exportar el DataFrame según el formato seleccionado (csv, json, xml)
        if formato == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="datos_etiquetados.csv"'
            df.to_csv(response, index=False, encoding="utf-8")
            return response


        if formato == 'json':
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="datos_etiquetados.json"'
            df.to_json(response, index=False, orient='records', force_ascii =False)  
            return response
        
        if formato == 'xml':
            response = HttpResponse(content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename="datos_etiquetados.xml"'
            df.to_xml(response, index= False, root_name='procesamientos', row_name='procesado')  
            return response

    else:
        return HttpResponseBadRequest("Método no permitido o formato no válido")



