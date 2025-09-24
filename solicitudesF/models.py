# PROYECTO/solicitudesF/models.py

from django.db import models
from django.contrib.auth.models import User # ¡Nuevo!

class TipoSolicitud(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la Solicitud",
        help_text="Ej: Solicitud de reparación de baches"
    )
    direccion = models.CharField(
        max_length=100,
        verbose_name="Dirección Responsable",
        help_text="Ej: Dirección de Operaciones"
    )
    descripcion_corta = models.TextField(
        verbose_name="Descripción Corta",
        help_text="Breve descripción del objetivo de esta solicitud."
    )
    # Puedes añadir un campo para vincular a una imagen o ícono si lo deseas
    # icono = models.CharField(max_length=50, blank=True, null=True, help_text="Clase de ícono de Bootstrap o similar")

    def __str__(self):
        return f"{self.nombre} ({self.direccion})"

    class Meta:
        verbose_name = "Tipo de Solicitud"
        verbose_name_plural = "Tipos de Solicitudes"
        ordering = ['nombre'] # Ordena por nombre por defecto


class Solicitud(models.Model):
    # Nuevo campo para vincular con el usuario que crea la solicitud
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, # Permite que sea nulo para solicitudes anónimas
        blank=True, # Permite que sea opcional en formularios
        related_name='solicitudes',
        verbose_name="Usuario"
    )

    # Nuevo campo para vincular con TipoSolicitud
    tipo_solicitud = models.ForeignKey(
        TipoSolicitud, # Referencia directa al modelo TipoSolicitud
        on_delete=models.SET_NULL, # Si un TipoSolicitud se borra, este campo en Solicitud se pone a NULL
        null=True, # Permite que el campo sea NULL en la base de datos
        blank=True, # Permite que el campo sea opcional en el formulario
        related_name='solicitudes', # Nombre inverso para acceder desde TipoSolicitud
        verbose_name="Tipo de Solicitud"
    )

    # Campos del formulario (tus campos existentes)
    email = models.EmailField(
        verbose_name="Correo Electrónico",
        help_text="Ingresa tu correo electrónico."
    )
    telefono = models.CharField(
        max_length=12, # Ej: +56912345678 (considerando prefijo y 9 dígitos)
        verbose_name="Teléfono Celular",
        help_text="Formato: +56912345678"
    )
    descripcion = models.TextField(
        verbose_name="Descripción de la Solicitud",
        help_text="Detalla tu solicitud aquí."
    )
    adjunto = models.FileField(
        upload_to='solicitudes_adjuntos/', # Los archivos se guardarán aquí dentro de MEDIA_ROOT
        blank=True, # El campo no es obligatorio
        null=True, # Puede ser nulo en la BD
        verbose_name="Archivo Adjunto",
        help_text="Adjunta documentos relevantes (ej. PDF, imágenes)."
    )

    # Campos de Clave Única (se llenarán después de la autenticación)
    nombre_completo = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Nombre Completo (Clave Única)"
    )
    rut = models.CharField(
        max_length=12, # Ej: 12.345.678-K
        blank=True,
        null=True,
        verbose_name="RUT (Clave Única)"
    )

    # Metadatos de la solicitud
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, # Se asigna automáticamente al crear la solicitud
        verbose_name="Fecha de Creación"
    )
    estado = models.CharField(
        max_length=50,
        default='Pendiente',
        choices=[
            ('Pendiente', 'Pendiente'),
            ('En Proceso', 'En Proceso'),
            ('Resuelta', 'Resuelta'),
            ('Rechazada', 'Rechazada'),
        ],
        verbose_name="Estado de la Solicitud"
    )

    def __str__(self):
        # Muestra una representación legible del objeto en el panel de administración
        if self.usuario:
            return f"Solicitud de {self.usuario.username}"
        elif self.nombre_completo:
            return f"Solicitud de {self.nombre_completo}"
        else:
            return f"Solicitud Anónima - {self.fecha_creacion.strftime('%d-%m-%Y %H:%M')}"

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ['-fecha_creacion'] # Las solicitudes más recientes primero