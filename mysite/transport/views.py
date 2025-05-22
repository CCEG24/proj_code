from django.shortcuts import render
from django.conf import settings
import requests
from datetime import datetime
import json

def transport_view(request):
    """Render the transport page with traffic data"""
    # Kenilworth coordinates
    latitude = 52.3493
    longitude = -1.5827
    
    try:
        # Get weather data for context
        weather_url = 'https://api.open-meteo.com/v1/forecast'
        weather_params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m,precipitation_probability,weathercode',
            'timezone': 'Europe/London'
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Get current conditions
        current_hour = datetime.now().hour
        current_temp = weather_data['hourly']['temperature_2m'][current_hour]
        current_precip = weather_data['hourly']['precipitation_probability'][current_hour]
        
        context = {
            'latitude': latitude,
            'longitude': longitude,
            'traffic_condition': "Traffic data available on map",  # Google Maps will show traffic directly
            'current_temp': current_temp,
            'current_precip': current_precip,
            'current_time': datetime.now().strftime('%H:%M'),
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        }
        
    except requests.exceptions.RequestException as e:
        context = {
            'error': f'Error fetching data: {str(e)}',
            'latitude': latitude,
            'longitude': longitude,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        }
    except Exception as e:
        context = {
            'error': f'An unexpected error occurred: {str(e)}',
            'latitude': latitude,
            'longitude': longitude,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        }
    
    return render(request, 'transport/transport.html', context)
