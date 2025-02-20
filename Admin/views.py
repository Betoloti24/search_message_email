from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario 
from .forms import CorreoForm

def ingresar_correo(request):
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            print(f'Correo ingresado: {correo}')  # Imprime el correo en la consola
            return render(request, 'exito.html', {'correo': correo})
    else:
        form = CorreoForm()

    return render(request, 'ingresar_correo.html', {'form': form})