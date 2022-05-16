from django.contrib import admin
from .models import Aadhar,Address,Qualification,Bank,PersonalDetails,PastJobExperience
# Register your models here.


class PastJobExperienceInlineAdmin(admin.StackedInline):
    model = PastJobExperience
    extra = 1


class PersonalDetailsInlineAdmin(admin.StackedInline):
    model = PersonalDetails
    extra = 1

class BankInlineAdmin(admin.StackedInline):
    model = Bank
    extra = 1

class QualificationInlineAdmin(admin.StackedInline):
    model = Qualification
    extra = 1

class AddressInlineAdmin(admin.StackedInline):
    model =Address
    extra = 1

class AadharInlineAdmin(admin.StackedInline):
    model = Aadhar
    extra = 1
    
@admin.register(Aadhar)
class AadharAdmin(admin.ModelAdmin):
    inlines = [PersonalDetailsInlineAdmin,AddressInlineAdmin,QualificationInlineAdmin,PastJobExperienceInlineAdmin,BankInlineAdmin,]
    list_display = [
                    'user',
                    'aadhar_number',
                    'active',
                    ]
    list_display_links = [
                    'user',
                    'aadhar_number',
    ]
    list_editable = [
                    'active',
                    ]
    list_filter = [
                    'active',
                    ]
    search_fields = [
                    'user',
                    'aadhar_number',
                    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
                    'user',   
                    'street', 
                    'city',   
                    'state',  
                    'pincode',
                    ]
    list_display_links = [
                    'user', 
    ]
    list_filter = [
                    'user',
                    ]
    search_fields = [
                    'user',   
                    'street', 
                    'city',   
                    'state',  
                    'pincode',
                    ]

@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = [
                    'user',
                    'email',
                    'contact',
                    ]
    list_display_links = [
                    'user',
    ]
    list_filter = [
                    'user',
                    ]
    search_fields = [
                    'user',
                    'email',
                    'contact',
                    ]

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = [
                    'user',
                    'name_of_college',
                    'year_of_passing',
                    'percentage',
                    ]
    list_display_links = [
                    'user',
                    'name_of_college',
    ]
    list_filter = [
                    'user',
                    'year_of_passing',
                    ]
    search_fields = [
                    'user',
                    'name_of_college',
                    'year_of_passing',
                    'percentage',
                    ]

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = [
                    'user',
                    'account_no',
                    'bank_name', 
                    'IFSC_code', 
                    ]
    list_display_links = [
                    'user',
                    'account_no',
                    'bank_name'
    ]
    list_filter = [
                    'user',
                    ]
    search_fields = [
                    'user',
                    'account_no',
                    'bank_name', 
                    'IFSC_code', 
                    ]

@admin.register(PastJobExperience)
class PastJobExperienceAdmin(admin.ModelAdmin):
    list_display = [
                    'user',
                    'company_name',
                    'job_role',
                    'year_experience',
                    ]
    list_display_links = [
                    'user',
                    'company_name',
    ]
    list_filter = [
                    'user',
                    ]
    search_fields = [
                    'user',
                    'company_name',
                    'job_role',
                    'year_experience',
                    ]
