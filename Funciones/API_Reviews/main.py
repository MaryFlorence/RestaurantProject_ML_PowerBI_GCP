import os 
import re 
import json 
import googlemaps 
from google.cloud import storage 

def call_google_maps_api(request): 

    # Configura la clave de API de Google Maps 

    api_key = 'API' 

    gmaps = googlemaps.Client(key=api_key) 
    
    # Define el área geográfica de cada estado (coordenadas y radio) 

    states = { 

    'California': (36.7783, -119.4179), 
    'Iowa': (41.8780, -93.0977), 
    'Kentucky': (37.8393, -84.2700), 
    'Mississippi': (32.3547, -89.3985), 
    'Texas': (31.9686, -99.9018), 
    'Indiana': (40.2672, -86.1349) 
    } 
    
    radius = 50000 
    
    # Lista para almacenar los resultados 
    
    results = [] 
    
    # Obtén la información para cada estado 
    for state_code, location in states.items(): 
        
        places_result = gmaps.places_nearby( 
            location=location, 
            radius=radius, 
            type='restaurant' 
        ) 
        
    state_reviews = [] 
    
    for place in places_result.get('results', []): 
        place_id = place.get('place_id', 'Place ID no disponible') 
        place_details = gmaps.place(place_id=place_id, fields=['reviews']) 
        reviews = place_details.get('result', {}).get('reviews', []) 
        
        for review in reviews: 
            user_id_url = review.get('author_url', 'ID de Usuario no disponible') 
            user_id_match = re.search(r'/(\d+)/reviews$', user_id_url) 
            if user_id_match: 
                user_id = user_id_match.group(1) 
            else: 
                user_id = 'ID no encontrado' 
            
            stars = review.get('rating', 'Calificación no disponible')
            text = review.get('text', 'No text')
            date = review.get('time', 'No date') 
            
            state_reviews.append({ 
                'ID_Business': place_id, 
                'State' : state_code, 
                'User_ID': user_id, 
                'Stars': stars, 
                'Text': text,
                'Date': date, 
                'APP' : 'Google' 
            }) 
        
    results.extend(state_reviews) 
    
    # Guarda los resultados en un archivo JSON en tu bucket de Cloud Storage 

    bucket_name = 'etl-goo-transformado' 
    file_name = 'resultados_google_maps.json' 
    client = storage.Client() 
    bucket = client.bucket(bucket_name) 
    blob = bucket.blob(file_name) 
    blob.upload_from_string(json.dumps(results, indent=1, separators=(',', ': '))) 
    
    return f'Resultados guardados en gs://{bucket_name}/{file_name}'