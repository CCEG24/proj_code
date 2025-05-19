from django.db import models

# Create your models here.
class WeatherData(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    max_wind_speed = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.temperature}°C - {self.max_wind_speed} m/s"