from django import forms

class CorreoForm(forms.Form):
    correo = forms.EmailField(label='Correo Electrónico', max_length=255)
