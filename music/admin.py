from django.contrib import admin
from .models import Music, Stage, Term, Concert

admin.site.register(Music)
admin.site.register(Stage)
admin.site.register(Term)
admin.site.register(Concert)