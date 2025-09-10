# PROYECTO/solicitudesF/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Solicitud, TipoSolicitud # ¡Asegúrate de importar TipoSolicitud!

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud # Asocia este formulario con el modelo Solicitud
        # ¡IMPORTANTE! Añade 'tipo_solicitud' aquí al inicio
        fields = ['tipo_solicitud', 'email', 'telefono', 'descripcion', 'adjunto']

        # Puedes personalizar los widgets para un mejor control del HTML y atributos
        widgets = {
            # Asegúrate de que el widget para tipo_solicitud también tenga clases de Bootstrap si lo deseas
            'tipo_solicitud': forms.Select(attrs={'class': 'form-select'}), # 'form-select' es la clase de Bootstrap para selects
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu.correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678', 'pattern': '\\+569[0-9]{8}'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe detalladamente tu solicitud...'}),
            'adjunto': forms.FileInput(attrs={'class': 'form-control'}),
        }
        # Los campos 'nombre_completo' y 'rut' no están aquí porque se llenarán con Clave Única.
        # Los campos 'fecha_creacion' y 'estado' son automáticos.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)        