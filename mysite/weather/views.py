from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
import io
import base64
import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
import random
import logging

logger = logging.getLogger(__name__)

def index(request):
    """Render the main index page"""
    return render(request, 'index.html')

def generate_mock_weather_data(start_date, end_date):
    """Generate mock weather data for testing"""
    dates = pd.date_range(start=start_date, end=end_date)
    data = []
    
    # Base values for Kenilworth, UK
    base_temp = 15  # Average temperature in °C
    base_wind = 5   # Average wind speed in m/s
    
    for date in dates:
        # Generate random variations
        temp_variation = random.uniform(-5, 5)
        wind_variation = random.uniform(-2, 2)
        
        # Calculate daily values
        avg_temp = base_temp + temp_variation
        max_temp = avg_temp + random.uniform(2, 4)
        min_temp = avg_temp - random.uniform(2, 4)
        max_wind = base_wind + wind_variation + random.uniform(0, 3)
        
        data.append({
            'datetime': date.strftime('%Y-%m-%d'),
            'temp': round(avg_temp, 1),
            'max_temp': round(max_temp, 1),
            'min_temp': round(min_temp, 1),
            'max_wind_spd': round(max_wind, 1)
        })
    
    return pd.DataFrame(data)


def fetch_weather_json(url, params, cache_key, timeout=10, ttl=900):
    """Fetch weather JSON with cache fallback when provider rate-limits requests."""
    cached_data = cache.get(cache_key)

    try:
        response = requests.get(url, params=params, timeout=timeout)

        if response.status_code == 429:
            if cached_data is not None:
                return cached_data, True
            raise requests.exceptions.HTTPError(
                'Weather provider rate limit reached.', response=response
            )

        response.raise_for_status()
        payload = response.json()
        cache.set(cache_key, payload, ttl)
        return payload, False
    except requests.exceptions.RequestException:
        if cached_data is not None:
            logger.warning('Using cached weather data after API failure.')
            return cached_data, True
        raise

def display(request):
    location = 'Kenilworth, GB'
    # Kenilworth coordinates
    latitude = 52.3493
    longitude = -1.5827

    try:
        warning_message = None
        # Set timezone to UK
        uk_tz = pytz.timezone('Europe/London')
        now = datetime.now(uk_tz)
        
        # --- Get historical data from Open-Meteo (for plot and table) ---
        end_date = now.date()
        start_date = end_date - timedelta(days=30)
        
        historical_url = f'https://archive-api.open-meteo.com/v1/archive'
        historical_params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'daily': 'temperature_2m_max,temperature_2m_min,temperature_2m_mean,windspeed_10m_max',
            'timezone': 'Europe/London'
        }

        historical_cache_key = (
            f"weather:historical:{latitude}:{longitude}:"
            f"{start_date.strftime('%Y-%m-%d')}:{end_date.strftime('%Y-%m-%d')}"
        )
        historical_data, historical_from_cache = fetch_weather_json(
            historical_url,
            historical_params,
            historical_cache_key,
            ttl=3600,
        )
        if historical_from_cache:
            warning_message = (
                'Showing cached weather data because the weather provider is '
                'temporarily rate-limiting requests.'
            )
        
        # Convert historical data to DataFrame
        df = pd.DataFrame({
            'datetime': historical_data['daily']['time'],
            'max_temp': historical_data['daily']['temperature_2m_max'],
            'min_temp': historical_data['daily']['temperature_2m_min'],
            'temp': historical_data['daily']['temperature_2m_mean'],
            'max_wind_spd': historical_data['daily']['windspeed_10m_max']
        })
        
        # Convert dates to UK timezone
        df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize('Europe/London')
        
        # Create a copy of the DataFrame for plotting before any modifications
        plot_df = df.copy()
        
        # Calculate statistics while we still have numeric values
        avg_temp = df['temp'].mean()
        max_temp = df['max_temp'].max()
        min_temp = df['min_temp'].min()
        max_wind = df['max_wind_spd'].max()
        avg_wind = df['max_wind_spd'].mean()

        # Now replace NaN with 'Not Available' for display in the table
        df = df.fillna('Not Available')
        
        # Format dates for display
        df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d')

        # Handle NaN in statistics and round numeric values
        if pd.isna(avg_temp): avg_temp = 'Not Available'
        else: avg_temp = round(avg_temp, 1)
        if pd.isna(max_temp): max_temp = 'Not Available'
        else: max_temp = round(max_temp, 1)
        if pd.isna(min_temp): min_temp = 'Not Available'
        else: min_temp = round(min_temp, 1)
        if pd.isna(max_wind): max_wind = 'Not Available'
        else: max_wind = round(max_wind, 1)
        if pd.isna(avg_wind): avg_wind = 'Not Available'
        else: avg_wind = round(avg_wind, 1)

        # --- Get forecast data from Open-Meteo (for summary) ---
        forecast_url = 'https://api.open-meteo.com/v1/forecast'
        forecast_params = {
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'temperature_2m_max,temperature_2m_min,windspeed_10m_max,precipitation_probability_mean',
            'timezone': 'Europe/London',
            'forecast_days': 2  # Get 2 days to ensure we have tomorrow's data
        }

        tomorrow_max_temp = 'Not Available'
        tomorrow_min_temp = 'Not Available'
        tomorrow_max_wind = 'Not Available'
        tomorrow_precip_chance = 'Not Available'
        tomorrow_date = 'Not Available'

        try:
            forecast_cache_key = f"weather:forecast:{latitude}:{longitude}"
            forecast_data, forecast_from_cache = fetch_weather_json(
                forecast_url,
                forecast_params,
                forecast_cache_key,
                ttl=900,
            )

            if forecast_from_cache and not warning_message:
                warning_message = (
                    'Showing cached forecast because the weather provider is '
                    'temporarily rate-limiting requests.'
                )

            # Get tomorrow's forecast data (using index 1 for tomorrow)
            if 'daily' in forecast_data and len(forecast_data['daily']['time']) > 1:
                tomorrow_max_temp = forecast_data['daily']['temperature_2m_max'][1]
                tomorrow_min_temp = forecast_data['daily']['temperature_2m_min'][1]
                tomorrow_max_wind = forecast_data['daily']['windspeed_10m_max'][1]
                tomorrow_precip_chance = forecast_data['daily']['precipitation_probability_mean'][1]
                tomorrow_date = forecast_data['daily']['time'][1]
        except requests.exceptions.RequestException:
            if not warning_message:
                warning_message = (
                    'Live forecast is temporarily unavailable. Historical weather '
                    'data is still shown below.'
                )
        
        # Handle NaN in tomorrow's forecast data and round numeric values
        if isinstance(tomorrow_max_temp, (int, float)): tomorrow_max_temp = round(tomorrow_max_temp, 1)
        if isinstance(tomorrow_min_temp, (int, float)): tomorrow_min_temp = round(tomorrow_min_temp, 1)
        if isinstance(tomorrow_max_wind, (int, float)): tomorrow_max_wind = round(tomorrow_max_wind, 1)
        if isinstance(tomorrow_precip_chance, (int, float)): tomorrow_precip_chance = round(tomorrow_precip_chance, 1)

        # Create two subplots
        # The following block is commented out to save CPU on Render free tier.
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Format dates for plotting
        plot_dates = pd.to_datetime(plot_df['datetime']).dt.strftime('%Y-%m-%d')
        
        # Temperature plot
        ax1.plot(plot_dates, plot_df['min_temp'], marker='o', label='Minimum Temperature (°C)')
        ax1.plot(plot_dates, plot_df['max_temp'], marker='s', label='Maximum Temperature (°C)')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Temperature (°C)')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True)
        ax1.set_title('Temperature Data')
        ax1.legend()

        # Wind speed plot
        ax2.plot(plot_dates, plot_df['max_wind_spd'], marker='o', color='green', label='Max Wind Speed (m/s)')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Wind Speed (m/s)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True)
        ax2.set_title('Wind Speed Data')
        ax2.legend()

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        # Save the plot to a BytesIO buffer
        with io.BytesIO() as buffer:
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        """
        plot_data = None # Explicitly set plot_data to None here as graph generation is commented out

        # Pass the data to the template
        context = {
            'location': location,
            'plot_data': plot_data,
            'weather_data': list(reversed(df.to_dict(orient='records'))),  # Reverse the order for newest first
            'avg_temp': avg_temp,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'max_wind': max_wind,
            'avg_wind': avg_wind,
            'current_temp': tomorrow_max_temp,  # Using tomorrow's max temp as current (for summary)
            'current_max_temp': tomorrow_max_temp,
            'current_min_temp': tomorrow_min_temp,
            'current_max_wind': tomorrow_max_wind,
            'current_precip': tomorrow_precip_chance, # Using tomorrow's precip chance for summary
            'current_date': tomorrow_date,
            'warning': warning_message,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        }

        return render(request, 'display.html', context)

    except requests.exceptions.RequestException as e:
        status_code = getattr(getattr(e, 'response', None), 'status_code', None)
        if status_code == 429:
            error_message = (
                'Weather service is currently busy. Please try again in a few '
                'minutes.'
            )
        else:
            error_message = (
                'Unable to fetch weather data right now. Please try again shortly.'
            )
        return render(request, 'display.html', {
            'error': error_message,
            'location': location,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        })
    except Exception as e:
        return render(request, 'display.html', {
            'error': f'An unexpected error occurred: {str(e)}',
            'location': location,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        })