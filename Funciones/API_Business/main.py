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

    state_results = [] 
    
    for place in places_result.get('results', []): 

        name = place.get('name', 'Nombre no disponible') 
        address = place.get('vicinity', 'Dirección no disponible') 
        rating = place.get('rating', 'Calificación no disponible') 
        types = ', '.join(place.get('types', [])) 
        place_id = place.get('place_id', 'Place ID no disponible') 
        
        # Obtén los detalles completos del lugar, incluyendo las reseñas 

        place_details = gmaps.place(place_id=place_id, fields=['reviews', 'address_component']) 
        
        # Obtén las reseñas de los usuarios 
        
        reviews = place_details.get('result', {}).get('reviews', []) 

        num_reviews = len(reviews) 
        
        # Obtén detalles de la dirección 

        address_components = place_details.get('result', {}).get('address_components', []) 

        state = next((comp.get('long_name') for comp in address_components if 'administrative_area_level_1' in comp.get('types', [])), 'Estado no disponible') 
        
        # Cambia los códigos de estado a nombres completos 

        if state == 'CA': 
            state = 'California' 
        elif state == 'IA': 
            state = 'Iowa' 
        elif state == 'KY': 
            state = 'Kentucky' 
        elif state == 'TX': 
            state = 'Texas' 
        elif state == 'IN': 
            state = 'Indiana' 
        
        # Obtén las coordenadas del lugar 
        lat = place['geometry']['location']['lat'] 
        lng = place['geometry']['location']['lng'] 
        
        # Realiza una llamada a la API de Geocodificación inversa para obtener información adicional 
        
        geocode_result = gmaps.reverse_geocode((lat, lng)) 
        county = next((comp.get('long_name') for comp in geocode_result[0]['address_components'] if 'administrative_area_level_2' in comp.get('types', [])), 'Condado no disponible') 
        postal_code = next((comp.get('long_name') for comp in address_components if 'postal_code' in comp.get('types', [])), 'Código Postal no disponible') 
        
        # Verifica si el lugar ofrece entrega (delivery) 

        delivery = 1 if 'delivery' in place and place['delivery'] else 0 
        
        state_results.append({ 
            'Name': name, 
            'Address': address, 
            'Stars': rating, 
            'Category': types, 
            'ID_Business': place_id, 
            'Review_count': num_reviews, 
            'City': county, 
            'State': state, 
            'Postal_code': postal_code, 
            'Delivery': delivery, 
            'APP': 'Google' 
            }) 
        
        results.extend(state_results) 
    
    # Guarda los resultados en un archivo JSON en tu bucket de Cloud Storage 

    bucket_name = 'etl-goo-transformado' 
    file_name = 'new_business.json' 
    client = storage.Client() 
    bucket = client.bucket(bucket_name) 
    blob = bucket.blob(file_name) 
    blob.upload_from_string(json.dumps(results, indent=1, separators=(',', ': '))) 
    
    return f'Resultados guardados en gs://{bucket_name}/{file_name}'