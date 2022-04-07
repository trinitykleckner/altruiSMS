from django.contrib import admin
from .models import Beneficiary, Location, Organization

admin.site.register(Beneficiary)
admin.site.register(Location)
admin.site.register(Organization)