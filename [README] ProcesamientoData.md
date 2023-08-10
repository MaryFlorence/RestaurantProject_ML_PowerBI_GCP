# Procesamiento de Datos y carga incremental

Este proyecto se enfoca en el procesamiento y almacenamiento de datos provenientes de la API de Google Maps, utilizando servicios de Google Cloud para automatizar y organizar eficientemente el flujo de trabajo.

## Arquitectura del Proyecto
1. Configuración del Almacenamiento
Google Cloud Storage: Se comenzó configurando un bucket en Google Cloud Storage, donde se almacenarán los datos crudos en formato JSON procedentes de la API de Google Maps.

3. Funciones de Procesamiento
Función de Extracción de la API: Esta función tiene como tarea conectar con la API de Google Maps, obtener la información necesaria y almacenarla directamente en un archivo JSON dentro del bucket previamente configurado en Google Cloud Storage.

4. Función ETL (Extract, Transform, Load): Una vez los datos están en nuestro bucket, se ejecuta esta función para extraer los datos del archivo JSON, procesarlos (transformarlos según nuestras necesidades) y finalmente cargarlos en una tabla específica para su análisis y consulta.

5. Función de Carga Incremental: Esta función no solo se encarga de mantener actualizados los datos originales, sino que realiza una carga incremental de cualquier nueva información que se haya generado, asegurando eficiencia y evitando la repetición de datos ya existentes.

6. Automatización con Google Cloud Scheduler
Para garantizar que nuestros datos estén siempre actualizados, se ha configurado Google Cloud Scheduler para que ejecute nuestra función de carga incremental todos los días a las 11 a.m. Esto nos asegura que todos los días tengamos la información más reciente disponible para su análisis.
