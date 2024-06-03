from django.contrib import admin
from .models import CustomeUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

class CustomAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomeUser
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Personal Information",{
                "fields" : (
                    'id_number',
                    'phone_number',
                    'next_of_kin',
                    'next_of_kin_phone_number',
                    'blood_group',
                    'is_doctor',
                    'is_patient',
                    'is_donor',
                    'is_verified'
                )
            }
        )
    )

  
 
    

admin.site.register(CustomeUser, CustomAdmin)

# Register your models here.
