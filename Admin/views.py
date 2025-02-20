from django.shortcuts import render
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
                return render(request, 'exito.html', {'correo': usuario.correo, 'contraseña': usuario.contraseña})
            except Usuario.DoesNotExist:
                # Si el correo no existe, mostrar mensaje de error
                return render(request, 'ingresar_correo.html', {'form': form, 'error': 'El correo ingresado no existe.'})
        else:
            # Manejar errores de validación del formulario
            return render(request, 'ingresar_correo.html', {'form': form})
    else:
        form = CorreoForm()

    return render(request, 'ingresar_correo.html', {'form': form})
