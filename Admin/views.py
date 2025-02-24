import os, time
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
                # Construir la URL de la API de login usando variables de entorno
                api_url = f"{settings.API_BASE_URL}{settings.LOGIN_ENDPOINT}"
                payload = {
                    "address": usuario.correo,
                    "password": usuario.contraseña
                }
                response = requests.post(api_url, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    token = data.get("token")
                
                    # Esperamos para consultar los mensajes
                    time.sleep(2)
                    
                    # Consultar los mensajes hasta que se logre la consulta
                    while (True):
                        # Construir la URL de la API de mensajes usando variables de entorno
                        messages_url = f"{settings.API_BASE_URL}{settings.MESSAGES_ENDPOINT}?page=1"
                        headers = {
                            "Authorization": f"Bearer {token}"
                        }
                        messages_response = requests.get(messages_url, headers=headers)

                        if messages_response.status_code == 200:
                            messages_data = [{
                                "id": msg["id"], 
                                "from.address": msg["from"]["address"], 
                                "subject": msg["subject"], 
                                "createdAt": msg["createdAt"].split("T")[0], 
                                "downloadUrl": ""
                                } for msg in messages_response.json().get("hydra:member", []) if "¿Solicitaste actualizar tu Hogar con Netflix?" in msg.get("intro", "")]
                            
                            if len(messages_data) > 0:
                                # Consultamos el detalle de cada mensaje para obtener el enlace de descarga
                                for message in messages_data:
                                    while (True):
                                        message_detail_url = f"{settings.API_BASE_URL}{settings.MESSAGES_ENDPOINT}/{message['id']}"
                                        message_detail_response = requests.get(message_detail_url, headers=headers)
                                        if message_detail_response.status_code == 200:
                                            message_detail_data = message_detail_response.json()
                                            message["html"] = message_detail_data.get("html", "")[0]
                                            break
                                        else:
                                            time.sleep(2)
                                
                                # obtener todos los links del contenido html del mensaje
                                for message in messages_data:
                                    html = message["html"]
                                    links = []
                                    while 'href="' in html:
                                        start = html.find('href="') + 6
                                        end = html.find('"', start)
                                        links.append(html[start:end])
                                        html = html[end:]
                                    message["links"] = links
                                
                                # Buscamos el enlace de descarga en el contenido HTML de cada mensaje
                                for message in messages_data:
                                    for link in message["links"]:
                                        if "update-primary-location" in link:
                                            message["downloadUrl"] = link
                                            break
                                    if message["downloadUrl"] != "":
                                        break
                            
                                return render(request, 'mensajes.html', {'correo': usuario.correo, 'mensajes': messages_data})
                            return render(request, 'ingresar_correo.html', {'form': form, 'error': 'El correo enviado no posee mensajes visibles.'})
                        else:
                            time.sleep(2)
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
