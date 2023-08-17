# Data Processing 

Para poder realizar este proceso en primera instancia de debieron tratar los datos para que queden limpios y organizados. A continuación se muestra el esquema del procesamiento de datos.   

![Data Processing](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/_src/Data_Processing.jpg)    

Se comenzo con un ETL de manera local a travez de **Python/Pandas** de los archivos de **google maps y yelp** disponibles. Una vez realizado el ETL en cada dataset se concatenaron ambas apps, de tal forma que nos queden 2 archivos, uno de **reviews** y otro de **business**. Luego se cargarón estos 2 archivos a nuestro **Data Lake**, en esta ocasión, ya que trabajamos con Google Cloud, usamos **Google Cloud Storage** debido a su interfaz de usuario facil y completa.   

![Data Lake](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/_src/Data_Lake1.jpg)    

**Función:** [ETL local de Business](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/Funciones/ETL-Google_Yelp-Local/ETL-Business.ipynb)   
**Función:** [ETL local de Reviews](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/Funciones/ETL-Google_Yelp-Local/ETL-Reviews.ipynb)   

Una vez ya disponibles los archivos en nuestro data lake, se utilizo **BigQuery** como nuestro *Data Warehouse* para crear tablas y poblarlas con los datos de estos archivos (google_yelp.businees y google_yelp.reviews). Mediante Google SQL podremos realizar nuestras propias consultas. **El equipo de Data Scientist y el equipo de Data Analytics** utilizarán estos datos estructurados para sus diferentes necesidades.  
El Data Warehouse podrá actualizarse con nuevos datos en cualquier momento desde fuentes externas.   

![BigQuery](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/_src/BigQuery1.jpg)     

# Api-Data-Pipeline-Integration 

Uno de los principales objetivos para este proyecto es el enriquecimiento de los datos estáticos de Google Maps y Yelp, por medio de API´s.   

![API Data Pipeline](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/_src/API-Data.jpg)   

Las primeras 2 funciones realizan una llamada a las **APIs** de donde vamos a obtener nuevos datos con respecto a los restaurantes y reviews de Google Maps. Esta funcion se va a correr todos los dias a las 11:15 AM mediante **Google Cloud Scheduler** permitiendo *automatizarla* y nos va a guardar los datos en un **JSON** en nuestro Data Lake.   

**Función:** [API_Business](https://github.com/MaryFlorence/ProyectoFinalDS/tree/main/Funciones/API_Business)     
**Función:** [API Reviews](https://github.com/MaryFlorence/ProyectoFinalDS/tree/main/Funciones/API_Reviews)   

Una vez guardados estos JSON en nuestro Data Lake, se realizan otras 2 funciones las cuales van a leer estos JSON, van a realizarle transformaciones y van a guardar los archivos en formato **Parquet**. Luego van a cargar este archivo parquet en 2 tablas de **BigQuery**, el Parquet de los comercios se va a cargar en **new_business** y el Parquet de las reviews de va a cargar en **new_reviews**.  
Estas 2 funciones tambien van a estar automatizadas por Google Cloud Scheduler y va a correr todos los dias a las 11:30 AM. 

![Data Lake](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/_src/Bucket2.jpg)  
![BigQuery](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/_src/BigQuery2.jpg)

**Función:** [Load Business](https://github.com/MaryFlorence/ProyectoFinalDS/tree/main/Funciones/Load_Business)     
**Función:** [Load Reviews](https://github.com/MaryFlorence/ProyectoFinalDS/tree/main/Funciones/Load_Reviews)     

Una vez ya cargados los datos en las tablas de BigQuery, se van a realizar las ultimas 2 funciones las cuales van a permitir la **carga incremental de datos**.   
La primera de estas funciones es de la Update_Business, que hace que los nuevos restaurantes (ubicados en new_business) se carguen en la tabla de restaurantes (business) donde se encuentran los demas restaurantes, siempre y cuando el restaurante nuevo no se encuentre ya en esta tabla.   
La segunda funcion es de la Update_Reviews y lo que hace es realizar una carga de las nuevas reviews (ubicadas en new_reviews) se carguen en la tabla de reviews (review) donde se encuentran las demas reviews, siempre y cuando la review nueva no se encuentra en esta tabla y ademas el ID_Business de la review este presente en la tabla business, de esta manera de evita que se carguen reviews de restaurantes que aun no se cargaron en la tabla business. 

**Función:** [Update Business](https://github.com/MaryFlorence/ProyectoFinalDS/tree/main/Funciones/Update_Business)   
**Función:** [Update Reviews](https://github.com/MaryFlorence/ProyectoFinalDS/tree/main/Funciones/Update_Reviews)   

## Google Cloud Scheduler 

A traves de esta herramienta podemos automatizar las funciones programandolas para que corran en un horario determinado cada ciertos dias.  

![Scheduler](https://github.com/MaryFlorence/ProyectoFinalDS/blob/main/_src/Scheduler.jpeg)
