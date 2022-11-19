from django.contrib import admin
from .models import Dossier, Lot, Operateur, Profile, Utils, Op_Dos
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(Dossier)
admin.site.register(Profile)
admin.site.register(Utils)
admin.site.register(Operateur)
admin.site.register(Op_Dos)
admin.site.register(Lot)



# Register your models here.
