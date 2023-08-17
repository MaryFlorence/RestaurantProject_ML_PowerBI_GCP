from google.cloud import bigquery 
from datetime import datetime 
import pandas as pd 

def procesar_datos_y_cargar_en_bigquery(request): 

    # Configurar cliente de BigQuery 
    client = bigquery.Client() 
    
    # Referencia a la tabla en BigQuery 
    table_ref = client.dataset('new_sources').table('new_reviews') 
    
    # Open the JSON file and load it into a DataFrame 
    file_name = "resultados_google_maps.json" 
    df = pd.read_json(f"gs://etl-goo-transformado/{file_name}") 
    
    # Ajustar las fechas 
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce') 
    df['Text'] = df['Text'].fillna('No text') 
    df = df.dropna() 
    
    # Convertir la columna Date a formato UNIX TIMESTAMP 

    df['Date'] = (df['Date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')  

    # Guardar en formato Parquet 

    parquet_file_name = "new_reviews.parquet" 
    df.to_parquet(f"gs://etl-goo-transformado/{parquet_file_name}", index=False, engine="fastparquet") 
    
    # Configurar el trabajo de carga 

    job_config = bigquery.LoadJobConfig( 
        schema=[ 
            bigquery.SchemaField("ID_Business", "STRING"), 
            bigquery.SchemaField("User_ID", "STRING"), 
            bigquery.SchemaField("Date", "TIMESTAMP"), 
            bigquery.SchemaField("Stars", "INTEGER"), 
            bigquery.SchemaField("Text", "STRING"), 
            bigquery.SchemaField("State", "STRING"), 
            bigquery.SchemaField("APP", "STRING") 
        ], 
        source_format=bigquery.SourceFormat.PARQUET, 
    ) 
    
    # Ruta al archivo Parquet en Google Cloud Storage 
    
    uri = f"gs://etl-goo-transformado/{parquet_file_name}" 
    
    # Cargar datos en BigQuery 

    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config) 
    load_job.result() # Esperar a que se complete el trabajo 
    
    return 'Datos procesados y guardados en Parquet, y cargados en BigQuery correctamente.' 