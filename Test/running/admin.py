from dataclasses import field
from django.contrib import admin

# Register your models here.
from .models import Country, Province, Area, City

class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + [ field.name for field in obj._meta.fields ] + [ field.name for field in obj._meta.many_to_many ]

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields ]

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# @admin.register(Country)
# class CountryAdmin(ReadOnlyAdmin):
#     search_fields = ('chn_name', 'eng_name', )

# @admin.register(Province)
# class ProvinceAdmin(ReadOnlyAdmin):
#     search_fields = ('chn_name', 'eng_name')

# class CityAdmin(ReadOnlyAdmin):
# #     #list_display = ('city_id', 'counrtyid', 'areadid', 'provinceid' , 'chn_name', 'eng_name' )
#     autocomplete_fields = ['provinceid','countryid',]
