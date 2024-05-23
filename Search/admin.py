from django.contrib import admin
from .models import Document, Index

class FrequencyFilter(admin.SimpleListFilter):
    title = 'frequency'
    parameter_name = 'frequency'

    def lookups(self, request, model_admin):
        return (
            ('<5', 'Less than 5'),
            ('5-10', '5 to 10'),
            ('>10', 'More than 10'),
        )

    def queryset(self, request, queryset):
        if self.value() == '<5':
            return queryset.filter(frequency__lt=5)
        if self.value() == '5-10':
            return queryset.filter(frequency__gte=5, frequency__lte=10)
        if self.value() == '>10':
            return queryset.filter(frequency__gt=10)
        return queryset

class WeightFilter(admin.SimpleListFilter):
    title = 'weight'
    parameter_name = 'weight'

    def lookups(self, request, model_admin):
        return (
            ('>0.1', 'More than 0.1'),
            ('<0.1', 'Less than 0.1'),
            ('0.1-0.5', '0.1 to 0.5'),
            ('>0.5', 'More than 0.5'),
        )

    def queryset(self, request, queryset):
        if self.value() == '<0.1':
            return queryset.filter(weight__lt=0.1)
        if self.value() == '0.1-0.5':
            return queryset.filter(weight__gte=0.1, weight__lte=0.5)
        if self.value() == '>0.5':
            return queryset.filter(weight__gt=0.5)
        return queryset
    
class AlgorithmFilter(admin.SimpleListFilter):
    title = 'algorithm'
    parameter_name = 'algorithm'

    def lookups(self, request, model_admin):
        return [
            ('boolean', 'Boolean'),
            ('extended_boolean', 'Extended Boolean'),
            ('vector', 'Vector'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(algorithm=self.value())
        return queryset


class IndexAdmin(admin.ModelAdmin):
    list_display = ('term', 'document', 'frequency', 'weight','algorithm')
    search_fields = ('term', 'document__title')
    list_filter = (AlgorithmFilter,FrequencyFilter, WeightFilter)

admin.site.register(Index, IndexAdmin)
admin.site.register(Document)
