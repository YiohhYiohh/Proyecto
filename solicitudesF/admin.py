from django.contrib import admin


from .models import Solicitud, TipoSolicitud # Asegúrate de importar TipoSolicitud

admin.site.register(Solicitud)
admin.site.register(TipoSolicitud) # Registra el nuevo modelo