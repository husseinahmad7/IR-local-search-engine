from django import forms

class IndexingForm(forms.Form):
    directory = forms.CharField(label='Directory', max_length=255)
    language = forms.ChoiceField(choices=[('en', 'English'), ('ar', 'Arabic')])
    # algorithm = forms.ChoiceField(choices=[('boolean', 'Boolean'), ('extended_boolean', 'Extended Boolean'), ('vector', 'Vector')])

class SearchForm(forms.Form):
    query = forms.CharField(label='Query', max_length=255)
    algorithm = forms.ChoiceField(choices=[('boolean', 'Boolean'), ('extended_boolean', 'Extended Boolean'), ('vector', 'Vector')])
