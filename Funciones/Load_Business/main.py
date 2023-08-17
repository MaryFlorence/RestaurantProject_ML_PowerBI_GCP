from google.cloud import bigquery 
from datetime import datetime 
import pandas as pd 

def procesar_datos_y_cargar_en_bigquery(request): 
    
    # Configurar cliente de BigQuery 
    client = bigquery.Client() 
    
    # Referencia a la tabla en BigQuery 
    table_ref = client.dataset('new_sources').table('new_business') 

    # Open the JSON file and load it into a DataFrame 

    file_name = "new_business.json" 
    df = pd.read_json(f"gs://etl-goo-transformado/{file_name}")  

    # Reemplazar 'Calificación no disponible' con 0 

    df['Stars'] = df['Stars'].replace('Calificación no disponible', 0) 

    # Borramos columna 'Postal_code'

    df.drop(columns=['Postal_code'], inplace=True) 
    df = df.dropna()  

    # Guardar en formato Parquet 

    parquet_file_name = "new_business.parquet" 
    df.to_parquet(f"gs://etl-goo-transformado/{parquet_file_name}", index=False, engine="fastparquet") 

    # Configurar el trabajo de carga 

    job_config = bigquery.LoadJobConfig( 
        schema=[ 
            bigquery.SchemaField("ID_Business", "STRING"), 
            bigquery.SchemaField("Name", "STRING"), 
            bigquery.SchemaField("Address", "STRING"), 
            bigquery.SchemaField("City", "STRING"), 
            bigquery.SchemaField("State", "STRING"), 
            bigquery.SchemaField("Category", "STRING"), 
            bigquery.SchemaField("Stars", "FLOAT"), 
            bigquery.SchemaField("Review_count", "INTEGER"), 
            bigquery.SchemaField("Delivery", "INTEGER"), 
            bigquery.SchemaField("APP", "STRING") 
        ], 
        source_format=bigquery.SourceFormat.PARQUET, 
    ) 

    # Ruta al archivo Parquet en Google Cloud Storage 

    uri = f"gs://etl-goo-transformado/{parquet_file_name}" 
    
    # Cargar datos en BigQuery 
    
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config) 
    load_job.result() # Esperar a que se complete el trabajo 
    
    return "Datos procesados y guardados en Parquet, y cargados en BigQuery correctamente."