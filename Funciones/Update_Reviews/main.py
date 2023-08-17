from google.cloud import bigquery 

def cargar_incremental_y_contar(request): 
    client = bigquery.Client() 
    
    # Realiza la carga incremental 
    
    query = """ 
    INSERT INTO buoyant-purpose-394321.google_yelp.review 
    (ID_Business, State, User_ID, Stars, Text, Date, APP) 
    SELECT 
    nr.ID_Business, 
    nr.State, 
    nr.User_ID, 
    CAST(nr.Stars AS INT64) AS Stars, 
    nr.Text, 
    nr.Date, 
    nr.APP 
    FROM 
    buoyant-purpose-394321.new_sources.new_reviews AS nr 
    JOIN 
    buoyant-purpose-394321.google_yelp.business AS r 
    ON 
    nr.ID_Business = r.ID_Business 
    LEFT JOIN 
    buoyant-purpose-394321.google_yelp.review AS ex 
    ON 
    nr.User_ID = ex.User_ID 
    AND nr.ID_Business = ex.ID_Business 
    AND nr.Text = ex.Text 
    WHERE 
    ex.User_ID IS NULL 
    OR ex.ID_Business IS NULL 
    OR ex.Text IS NULL 
    """ 
    
    query_job = client.query(query) 
    query_job.result() 
    
    # Obtiene el recuento total de filas en la tabla review 

    dataset_id = 'google_yelp' 
    table_id = 'review' 
    
    table_ref = client.dataset(dataset_id).table(table_id) 
    table = client.get_table(table_ref) 
    
    query_count = f"SELECT COUNT(*) FROM `{table.dataset_id}.{table.table_id}`" 
    query_job_count = client.query(query_count) 
    
    result = query_job_count.result() 
    row_count = next(result)[0] 
    
    return f"Carga incremental completada. Total rows in table: {row_count}"