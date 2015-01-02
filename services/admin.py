from django.contrib.gis import admin

# Register your models here.
from models import Police911Response

admin.site.register(Police911Response, admin.GeoModelAdmin)