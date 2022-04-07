from django.contrib import admin
from .models import Beneficiary, Organization

admin.site.register(Beneficiary)
admin.site.register(Organization)