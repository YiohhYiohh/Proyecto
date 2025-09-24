# solicitudesF/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Para mostrar notificaciones al usuario
from .models import Solicitud, TipoSolicitud
from django.contrib.auth.decorators import login_required
from .forms import SolicitudForm, CustomUserCreationForm # Importa el nuevo formulario aquí
from django.contrib.auth import login, logout # Importa logout


@login_required
def lista_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, 'lista_solicitudes.html', {'solicitudes': solicitudes})

def crear_solicitud(request):
    tipo_id = request.GET.get('tipo_id')
    tipo_solicitud_seleccionado = None

    if tipo_id:
        try:
            tipo_solicitud_seleccionado = get_object_or_404(TipoSolicitud, id=tipo_id)
        except ValueError:
            pass

    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            
            # --- Aquí está el cambio para asociar el usuario ---
            if request.user.is_authenticated:
                solicitud.usuario = request.user
            
            if tipo_solicitud_seleccionado:
                solicitud.tipo_solicitud = tipo_solicitud_seleccionado
            
            solicitud.save()

            messages.success(request, "✅ Tu solicitud fue enviada exitosamente.")
            return redirect('solicitudesF:solicitud_exitosa')
        else:
            messages.error(request, "⚠️ Por favor revisa los errores en el formulario.")
    else:
        initial_data = {}
        if tipo_solicitud_seleccionado:
            initial_data['tipo_solicitud'] = tipo_solicitud_seleccionado
        form = SolicitudForm(initial=initial_data)

    context = {
        'form': form,
        'tipo_solicitud_seleccionado': tipo_solicitud_seleccionado
    }
    return render(request, 'solicitudesF/formulario_solicitud.html', context)

def solicitud_exitosa(request):
    """
    Vista que confirma que la solicitud fue enviada con éxito.
    """
    return render(request, 'solicitudesF/solicitud_exitosa.html')


def home(request):
    """
    Vista de la página de inicio.
    """
    return render(request, 'solicitudesF/home.html')

@login_required
def listar_tipos_solicitud(request):
    """
    Vista que lista los diferentes tipos de solicitud disponibles.
    """
    tipos_solicitud = TipoSolicitud.objects.all()
    context = {
        'tipos_solicitud': tipos_solicitud,
        'nombre_usuario': 'Rodrigo Andrés'  # Placeholder: más adelante se tomará del usuario logeado
    }
    return render(request, 'solicitudesF/listar_tipos_solicitud.html', context)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ya no iniciamos sesión automáticamente.
            messages.success(request, "✅ Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect("login") # Redirige al usuario a la página de login
        else:
            messages.error(request, "⚠️ Error en el registro. Por favor, revisa los campos.")
    else:
        form = CustomUserCreationForm()
    return render(request, "solicitudesF/register.html", {"form": form})

# PROYECTO/solicitudesF/views.py

@login_required
def lista_solicitudes(request):
    solicitudes = Solicitud.objects.all() # Obtiene todas las solicitudes de la base de datos
    return render(request, 'solicitudesF/lista_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def mis_solicitudes(request):
    """
    Muestra una lista de todas las solicitudes creadas por el usuario autenticado.
    """
    solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'solicitudesF/mis_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def detalle_solicitud(request, solicitud_id):
    """
    Muestra los detalles de una solicitud específica.
    """
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id, usuario=request.user)
    return render(request, 'solicitudesF/detalle_solicitud.html', {'solicitud': solicitud})