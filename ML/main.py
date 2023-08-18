# IMPORTACIÓN DE LIBRERÍAS:

from fastapi import FastAPI
import pandas as pd
import pyarrow
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


app = FastAPI()

# LECTURA DE DATASETS:

df1 = pd.read_parquet('reviews_google_yelp_lote1.parquet')
df2 = pd.read_parquet('reviews_google_yelp_lote2.parquet')
df3 = pd.read_parquet('reviews_google_yelp_lote3.parquet')
df4 = pd.read_parquet('reviews_google_yelp_lote4.parquet')
df5 = pd.read_parquet('reviews_google_yelp_lote5.parquet')
df6 = pd.read_parquet('reviews_google_yelp_lote6.parquet')
#df7 = pd.read_parquet('reviews_google_yelp_lote7.parquet')
#df8 = pd.read_parquet('reviews_google_yelp_lote8.parquet')
#df9 = pd.read_parquet('reviews_google_yelp_lote8.parquet')
#df10 = pd.read_parquet('reviews_google_yelp_lote10.parquet')
#df11 = pd.read_parquet('reviews_google_yelp_lote11.parquet')
#df12 = pd.read_parquet('reviews_google_yelp_lote12.parquet')
df_general = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index = True)
df_general = df_general.reset_index(drop = True)

df_general = pd.read_parquet('asdf.parquet')
df_business = pd.read_parquet('business_google_yelp.parquet')


# FUNCIÓN PARA OBTENER LOS LUGARES QUE VISITÓ EL USUARIO:

def get_business_user(user_id):
    # Se ingresa un 'User_ID' y retorna un DataFrame con los negocios que visitó que tengan mayor o igual a 4 estrellas
    s = df_general[df_general['User_ID']==user_id]
    e = s[s['Stars']>=4]
    return set(e['ID_Business'])

# FUNCIÓN PARA OBTENER EL TOP DE LUGARES DE UN ESTADO:

def get_top_business_state2(state):
    # Filtramos el dataset por estado:
    top = df_business[df_business['State'] == state]
    # Para evitar un posible sesgo, solo tomaremos negocios que tengan un mínimo de 15 reseñas:
    top = top[top['Review_count']>=15]
    # Por último, nos quedaremos con aquellos negocios que tengan un mínimo de 4.5 estrellas de promedio:
    top = set(top[top['Stars']>=4.5]['ID_Business'])
    
    return top 

# FUNCIÓN PARA OBTENER UNA TABLA DE 5 FILAS DE ID DE NEGOCIOS CON SUS REVIEWS:

def get_tabla_idnegocio_reviews(id_negocios):
    tabla_idnegocio_reviews = df_general[df_general['ID_Business'].isin(id_negocios)]   
    tabla_idnegocio_reviews = tabla_idnegocio_reviews[tabla_idnegocio_reviews['Stars']>=4.5]
    tabla_idnegocio_reviews = tabla_idnegocio_reviews[tabla_idnegocio_reviews['Text'] != 'No text']
    # Ordenamos el DataFrame por 'ID_Business' y 'Date' de manera descendente:
    tabla_idnegocio_reviews = tabla_idnegocio_reviews.sort_values(by=['ID_Business', 'Date'], ascending=[True, False])
    # Agrupamos por 'ID_Business' y seleccionamos las primeras 5 filas de cada grupo:
    tabla_idnegocio_reviews = tabla_idnegocio_reviews.groupby('ID_Business').head(5)
    tabla_idnegocio_reviews = tabla_idnegocio_reviews[['ID_Business', 'Text']]
    return tabla_idnegocio_reviews


# FUNCIÓN PARA OBTENER LOS States DEL User_ID:

def get_states(User_ID):
    return list(df_general[df_general['User_ID'] == User_ID]['State'].unique())


# FUNCIÓN PARA CONVERTIR UNA LISTA DE ID_Business A UNA LISTA DE SUS NOMBRES DE NEGOCIO RESPECTIVOS:

def nombre_negocio(lista_ids):
    # Convierte una lista de id de negocios en una lista con los nombres respectivos de los negocios
    df_business = pd.read_parquet('business_google_yelp.parquet')
    recomendacion_texto2 = []
    for id in lista_ids:
        s = df_business[df_business['ID_Business'] == id]
        e = s['Name'].to_list()[0]
        recomendacion_texto2.append(e)
    return recomendacion_texto2


# FUNCIÓN PARA OBTENER LA RESEÑA QUE MEJOR HAYA CALIFICADO UN USUARIO:

# Se ingresa un id de usuario y retorna la reseña que mejor haya calificado 
# (si hay varias entonces se retornará la más reciente):
def get_mejor_calificacion(id_usuario):
    mejor_calificacion = df_general[df_general['User_ID'] == id_usuario]
    mejor_calificacion = mejor_calificacion.sort_values(by = ['Stars', 'Date'], ascending = False)
    mejor_calificacion = mejor_calificacion['Text'].head(1).to_list()[0]
    return mejor_calificacion    


# FUNCIÓN SIMILITUD DE COSENO:

def similitud_coseno(resumen_pelicula, tabla):
    i = tabla
    tfidf = TfidfVectorizer(stop_words="english")
    i["Text"] = i["Text"].fillna("")
    tfidf.fit(i["Text"])
    tfidf_matriz = tfidf.transform([resumen_pelicula])
    coseno_sim = linear_kernel(tfidf_matriz, tfidf.transform(i["Text"]))
    simil = list(enumerate(coseno_sim[0]))
    simil = sorted(simil, key=lambda x: x[1], reverse=True)
    simil = simil[1:11]
    movie_index = [i[0] for i in simil]
    lista = i["ID_Business"].iloc[movie_index].tolist()[:5]
    return lista


# FUNCIÓN RECOMENDACIÓN FINAL EN LA QUE USAREMOS TODAS LAS ANTERIORES FUNCIONES CREADAS:

@app.get("/recomendacion/{user_id}")

def recomendacion3(user_id):
    states = get_states(user_id)
    recomendacion_stateS = []
    for state in states:
        top_business = get_top_business_state2(state)
        business_user = get_business_user(user_id)
        recomendacion_state = top_business.difference(business_user) # conjunto que contiene los id de los negocios top menos los que el usuario ya visito
        # se llama a la funcion que con estos id de negocio crea un tabla de 2 columnas donde estan los id de solos estos negocios y sus respectivas
        # reseñas filtradas por estado, cantidad de reseñas minimas y cantidad de estrellas y almacena esta tabla en la variable tabla top negocios
        tabla_idnegocio_reviews = get_tabla_idnegocio_reviews(recomendacion_state)
        # se llama a la funcion que obtiene la mejor reseña que dio el usuario  y se almacena dentro de la variable resumen_pelicula(reseña_top_user)
        mejor_calificacion = get_mejor_calificacion(user_id)
        # se llama a la funcion similitud de reseñas que da como resultado los id de las reseñas que mejor se parece a la reseña top del usuario,
        # estos resultados se almacenan en una variable y se convierten a conjuntos para eliminar negocios repetido, luego se convierte en una lista
        # tomando los 5 primeros resutados
        recomendacion_state = similitud_coseno(mejor_calificacion, tabla_idnegocio_reviews)
        # una vez que se hace la diferencia, los negocios que te queden
        # introducirlos a la funcion para que los ordene de mayor a menor la similitu y de esos escoger los primeros 5
        recomendacion_stateS.append(recomendacion_state)
    recomendacion_texto = []
    for cantidad in range(len(states)):
        recomendado = nombre_negocio(recomendacion_stateS[cantidad])
        recomendacion_texto_base = "Para el estado de " + states[cantidad] + " te recomendamos los siguientes lugares: " + ", ".join(recomendado)
        recomendacion_texto.append(recomendacion_texto_base)
    return {"Recomendación": ". ".join(recomendacion_texto)}