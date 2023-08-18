# Sistema de recomendación de restaurantes

Sistema que utiliza el filtrado colaborativo y la similitud por coseno para recomendar restaurantes a usuarios que cuenten con al menos una
reseña en Google Maps o Yelp. Se consideran restaurantes ubicados en Estados Unidos y registrados en las plataformas anteriormente mencionadas,
en las cuales pueden dejarse reseñas y asignar estrellas del 1 al 5.

## Tecnologías Utilizadas

| ![Imagen 1](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/Python-logo-notext.png) | ![Imagen 2](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/Visual_Studio_Code_1.35_icon.svg.png) | ![Imagen 3](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/Pandas_logo.svg.png) | ![Imagen 4](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/2560px-Scikit_learn_logo_small.svg.png) 
|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
|    Python        |    Visual Studio Code        |    Pandas        |    Scikit-learn        

| ![Imagen 4](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/uvicorn.png) | ![Imagen 5](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/1_UQpQJjVtSuUFxXmb64hqYw.png) | ![Imagen 6](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/MRd3wYu7.png) | ![Imagen 7](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/image27_frqkzv.png) |
|:-----------------------:|:-----------------------:|:-----------------------:|:-----------------------:|
|    Uvicorn        |    FastAPI        |    render.com        |    streamlit        


## Uso

Cualquier persona puede acceder a nuestro sistema de recomendación mediante este [link](https://prueba13ago2023.onrender.com/docs).
Se deberá ingresar un id de usuario y el sistema retornará recomendación de restaurantes cercanos al usuario.

## Estructura del Proyecto

El algoritmo de recomendación se desarrolló utilizando el lenguaje de programación Python, y consta de la siguiente estructura:

### 1. Eliminación de reviews del mismo usuario: 
Transformaremos nuestro dataset para quedarnos con una sola review por cada usuario.
Si un usuario tiene registradas más de 1 review, solo se considerará la efectuada más recientemente y las demás se eliminaran.
(El desarrollo de esta transformación puede considerarse para una carga incremental)

### 2. Creación de una función para obtener los restaurantes top que visitó un usuario: 
Con nuestro dataset ya transformado, proseguiremos a crear nuestras funciones necesarias para nuestro sistema de
recomendación final. Primero crearemos una función cuya entrada sea un id de usuario y que retorne en formato conjunto 
todos los id de los restaurantes que el usuario visitó y que tengan una calificación promedio mínima de 4.5 estrellas.

### 3. Creación de una función para obtener los restaurantes top de un estado:
Ahora crearemos una función cuya entrada sea el nombre de un estado de Estados Unidos y cuyo retorno sea un conjunto de los
id de negocios que pertenezcan a dicho estado, tengan por lo menos 15 reviews, y una calificación promedio mínima de 4.5 estrellas.

### 4. Creación de una función para obtener una tabla (DataFrame) de las 5 mejores reviews de determinados negocios:
Creamos una función cuya entrada sea una lista de id de negocios y cuyo retorno sea un Dataframe conteniendo a los negocios con sus
mejores 5 reviews asignadas (es decir, sus 5 reviews con mayor asignación de estrellas).

### 5. Creación de una función para obtener todos los estados de las reviews de un usuario:
Función que tiene como entrada el id de un usuario y retorna una lista de los estados a los que pertenecían los restaurantes
de sus reviews.

### 6. Creación de una función para convertir una lista de id de negocios a una lista de sus nombres respectivos:
Función que tiene como entrada una lista de id de negocios y que retorna una lista con los nombres asignados a cada id
respectivamente.

### 7. Creación de una función para obtener la reseña con más estrellas de un usuario:
Una función que tiene como entrada el id de un usuario y que retorna en formato string su reseña con más estrellas 
(si hay más de una solo se considera la más reciente)


### 8. Función Similitud de Coseno:
Función que tiene como entrada todas las reviews y que retorna una lista de los 5 negocios con mayor reputación
en las reseñas escritas por sus usuarios.

### 9. Función Recomendación:
Es nuestra función final. Como entrada se espera el id de un usuario, y en el proceso se utilizarán todas las funciones mencionadas
anteriormente con el objetivo de finalmente recomendar los 5 mejores restaurantes para el usuario (si el usuario anteriormente ha
dejado reviews en varios estados, se le recomendará restaurantes de más de un estado). En esencia, esta función de recomendación 
utiliza los intereses de usuarios con gustos similares, restaurantes con mejores calificaciones y mejores reseñas, y que pertenezcan a
estados en los que el usuario haya estado antes o cercanos.



## Ejemplos

Al ingresar a la página web, la interfaz será la siguiente:
![Captura_pantalla1](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/web_1.png)
Se deberá ingresar un id y una contraseña, y el sistema hará las recomendaciones:
![Captuda_pantalla2](https://github.com/hernandroz/testeo13ago2023/blob/main/imagenes_readme/web_2.png)

## Licencia

Algoritmo desarrollado  por los Data Scientist Hernán Hernández Rodríguez y Fernando Cabrera Contreras 
