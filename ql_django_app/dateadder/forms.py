from django import forms
 
class DateAdderForm(forms.Form):
    input_date = forms.DateField(label="Date de départ", widget=forms.DateInput(attrs={'type': 'date'}))
 
 