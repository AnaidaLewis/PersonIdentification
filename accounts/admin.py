from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Register your models here.

from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)


User = get_user_model()
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
                    'id',
                    'email',
                    'firstname',    
                    'lastname',     
                    'blood',        
                    'DOB',          
                    'is_active',    
                    'staff',        
                    'admin',        
                    'auth_provider',
                    ]
    list_display_links = [
                    'id',
                    'email',
                    'firstname',    
                    'lastname',
    ]
    list_editable = [
                    'is_active',    
                    'staff',        
                    'admin',
                    ]
    list_filter = [
                    'is_active',    
                    'staff',        
                    'admin',        
                    'auth_provider',
                    ]
    search_fields = [
                    'id',
                    'email',
                    'firstname',    
                    'lastname',     
                    'blood',        
                    'DOB',          
                    'is_active',    
                    'staff',        
                    'admin',        
                    'auth_provider',
                    ]

