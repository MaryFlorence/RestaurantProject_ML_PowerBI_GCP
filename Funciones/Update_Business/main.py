from google.cloud import bigquery 

def cargar_incremental_business(request): 
    
    client = bigquery.Client()
    query = """ 
    INSERT INTO buoyant-purpose-394321.google_yelp.business 
    (ID_Business, Name, Address, City, State, Category, Stars, Review_count, Delivery, APP) 
    SELECT 
    nr.ID_Business, 
    nr.Name, 
    nr.Address, 
    nr.City, 
    nr.State, 
    nr.Category, 
    nr.Stars, 
    nr.Review_count, 
    nr.Delivery, 
    nr.APP 
    FROM 
    buoyant-purpose-394321.new_sources.new_business AS nr 
    LEFT JOIN 
    buoyant-purpose-394321.google_yelp.business AS ex 
    ON 
    nr.Name = ex.Name 
    AND nr.Address = ex.Address 
    AND nr.State = ex.State 
    WHERE 
    ex.Name IS NULL 
    """ 
    
    query_job = client.query(query) 
    query_job.result() 
    
    # Obtiene el recuento total de filas en la tabla business 

    dataset_id = 'google_yelp' 
    table_id = 'business' 
    
    table_ref = client.dataset(dataset_id).table(table_id) 
    table = client.get_table(table_ref) 
    
    query_count = f"SELECT COUNT(*) FROM `{table.dataset_id}.{table.table_id}`" 
    query_job_count = client.query(query_count) 
    
    result = query_job_count.result() 
    row_count = next(result)[0] 
    
    return f"Carga incremental completada. Total rows in table: {row_count}" 