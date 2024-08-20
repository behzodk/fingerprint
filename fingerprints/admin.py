from django.contrib import admin
from .models import Worker, Fingerprint

# Register your models here.
admin.site.register(Worker)
admin.site.register(Fingerprint)