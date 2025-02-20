import os
import requests
from django.shortcuts import render
from django.conf import settings
from .forms import CorreoForm
from .models import Usuario

def ingresar_correo(request):
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            try:
                # Consultar la base de datos por el correo
                usuario = Usuario.objects.get(correo=correo)

                # Construir la URL de la API usando variables de entorno
                api_url = f"{settings.API_BASE_URL}/{settings.LOGIN_ENDPOINT}"
                payload = {
                    "address": usuario.correo,
                    "password": usuario.contraseña
                }
                
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("token")
                    return render(request, 'exito.html', {'correo': usuario.correo, 'contraseña': usuario.contraseña, 'token': token})
                else:
                    return render(request, 'ingresar_correo.html', {'form': form, 'error': 'Error al iniciar sesión en la API.'})
            except Usuario.DoesNotExist:
                # Si el correo no existe, mostrar mensaje de error
                return render(request, 'ingresar_correo.html', {'form': form, 'error': 'El correo ingresado no existe.'})
        else:
            # Manejar errores de validación del formulario
            return render(request, 'ingresar_correo.html', {'form': form})
    else:
        form = CorreoForm()

    return render(request, 'ingresar_correo.html', {'form': form})
