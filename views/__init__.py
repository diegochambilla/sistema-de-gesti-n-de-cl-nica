from .auth_view import login, register
from .admin_view import dashboard, estadisticas
from .usuario_view import index as usuario_index, create as usuario_create, edit as usuario_edit
from .medico_view import index as medico_index, create as medico_create, edit as medico_edit, horarios as medico_horarios
from .paciente_view import index as paciente_index, create as paciente_create, edit as paciente_edit
from .especialidad_view import index as especialidad_index, create as especialidad_create, edit as especialidad_edit
from .cita_view import index as cita_index, create as cita_create, edit as cita_edit
from .consulta_view import crear as consulta_crear, detalle as consulta_detalle, agregar_receta as consulta_agregar_receta
from .receta_view import index as receta_index, create as receta_create
from .servicio_view import index as servicio_index, create as servicio_create, edit as servicio_edit
from .factura_view import index as factura_index, create as factura_create, detalle as factura_detalle
from .configuracion_view import index as configuracion_index, create as configuracion_create, edit as configuracion_edit

# También puedes exportar todo con nombres más específicos si prefieres
__all__ = [
    # Auth
    'login', 'register',
    
    # Admin
    'dashboard', 'estadisticas',
    
    # Usuario
    'usuario_index', 'usuario_create', 'usuario_edit',
    
    # Medico
    'medico_index', 'medico_create', 'medico_edit', 'medico_horarios',
    
    # Paciente
    'paciente_index', 'paciente_create', 'paciente_edit',
    
    # Especialidad
    'especialidad_index', 'especialidad_create', 'especialidad_edit',
    
    # Cita
    'cita_index', 'cita_create', 'cita_edit',
    
    # Consulta
    'consulta_crear', 'consulta_detalle', 'consulta_agregar_receta',
    
    # Receta
    'receta_index', 'receta_create',
    
    # Servicio
    'servicio_index', 'servicio_create', 'servicio_edit',
    
    # Factura
    'factura_index', 'factura_create', 'factura_detalle',
    
    # Configuración
    'configuracion_index', 'configuracion_create', 'configuracion_edit'
]