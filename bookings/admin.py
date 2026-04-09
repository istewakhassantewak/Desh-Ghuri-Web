from django.contrib import admin

# Register your models here.


from .models import Packages,PackageHighlights,TourLocation,Transport

admin.site.register(Packages)
admin.site.register(PackageHighlights)
admin.site.register(TourLocation)
admin.site.register(Transport)