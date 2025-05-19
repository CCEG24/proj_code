from django.shortcuts import render
from django.conf import settings
import io
import base64
import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

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

def display(request):
    try:
        # Set up date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        location = 'Kenilworth, GB'
        
        # Open-Meteo API coordinates for Kenilworth
        latitude = 52.3493  # Kenilworth latitude
        longitude = -1.5827  # Kenilworth longitude
        
        # Open-Meteo API call
        url = f'https://archive-api.open-meteo.com/v1/archive'
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'daily': 'temperature_2m_max,temperature_2m_min,temperature_2m_mean,windspeed_10m_max',
            'timezone': 'Europe/London'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Convert data to DataFrame
        df = pd.DataFrame({
            'datetime': data['daily']['time'],
            'max_temp': data['daily']['temperature_2m_max'],
            'min_temp': data['daily']['temperature_2m_min'],
            'temp': data['daily']['temperature_2m_mean'],
            'max_wind_spd': data['daily']['windspeed_10m_max']
        })
        
        # Format dates consistently
        df['datetime'] = pd.to_datetime(df['datetime']).dt.strftime('%Y-%m-%d')
        
        # Create a copy of the DataFrame for plotting before any modifications
        plot_df = df.copy()
        
        # Adjust the dates for plotting to match the actual data dates
        plot_df['datetime'] = pd.to_datetime(plot_df['datetime']) - pd.Timedelta(days=1)
        
        # Calculate statistics while we still have numeric values
        avg_temp = df['temp'].mean()
        max_temp = df['max_temp'].max()
        min_temp = df['min_temp'].min()
        max_wind = df['max_wind_spd'].max()
        avg_wind = df['max_wind_spd'].mean()

        # Get latest available day's data
        # Try the last row first, if it has NaN values, try the second-to-last row
        latest_day = df.iloc[-1]
        if pd.isna(latest_day['temp']) or pd.isna(latest_day['max_temp']) or pd.isna(latest_day['min_temp']) or pd.isna(latest_day['max_wind_spd']):
            latest_day = df.iloc[-2]  # Use second-to-last row if last row has NaN values
        
        latest_temp = latest_day['temp']
        latest_max_temp = latest_day['max_temp']
        latest_min_temp = latest_day['min_temp']
        latest_max_wind = latest_day['max_wind_spd']
        latest_date = latest_day['datetime']
        
        # Now replace NaN with 'Not Available' for display
        df = df.fillna('Not Available')
        
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
        
        # Handle NaN in latest day data and round numeric values
        if pd.isna(latest_temp): latest_temp = 'Not Available'
        else: latest_temp = round(latest_temp, 1)
        if pd.isna(latest_max_temp): latest_max_temp = 'Not Available'
        else: latest_max_temp = round(latest_max_temp, 1)
        if pd.isna(latest_min_temp): latest_min_temp = 'Not Available'
        else: latest_min_temp = round(latest_min_temp, 1)
        if pd.isna(latest_max_wind): latest_max_wind = 'Not Available'
        else: latest_max_wind = round(latest_max_wind, 1)

        # Create two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Temperature plot
        ax1.plot(plot_df['datetime'], plot_df['min_temp'], marker='o', label='Minimum Temperature (°C)')
        ax1.plot(plot_df['datetime'], plot_df['max_temp'], marker='s', label='Maximum Temperature (°C)')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Temperature (°C)')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True)
        ax1.set_title('Temperature Data')
        ax1.legend()

        # Wind speed plot
        ax2.plot(plot_df['datetime'], plot_df['max_wind_spd'], marker='o', color='green', label='Max Wind Speed (m/s)')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Wind Speed (m/s)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True)
        ax2.set_title('Wind Speed Data')
        ax2.legend()

        plt.tight_layout()

        # Save the plot to a BytesIO buffer
        with io.BytesIO() as buffer:
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

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
            'current_temp': latest_temp,
            'current_max_temp': latest_max_temp,
            'current_min_temp': latest_min_temp,
            'current_max_wind': latest_max_wind,
            'current_date': latest_date,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        }

        return render(request, 'display.html', context)

    except Exception as e:
        return render(request, 'display.html', {
            'error': 'An unexpected error occurred. Please try again later.',
            'location': location,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        })