# logic/services.py
from data.repositories import TraceabilityRepository, UserRepository

class TraceabilityService:
    def __init__(self):
        self.repo = TraceabilityRepository()

    def registrar_producto(self, data):
        if not data.get('lote'): raise ValueError("El lote es obligatorio")
        return self.repo.save(data)

    def obtener_trazabilidad(self):
        return self.repo.get_all()

    # NUEVOS MÉTODOS
    def obtener_producto(self, id):
        return self.repo.get_by_id(id)

    def actualizar_producto(self, id, data):
        return self.repo.update(id, data)

    def eliminar_producto(self, id):
        return self.repo.delete(id)

    def obtener_estadisticas(self):
        # Lógica simple para alimentar el Dashboard
        productos = self.repo.get_all()
        total = len(productos)
        rechazados = len([p for p in productos if p.calidad_ok == 'Rechazado'])
        alertas_temp = len([p for p in productos if p.temperatura_transporte > 10])
        return {
            'total': total,
            'rechazados': rechazados,
            'alertas': alertas_temp
        }

class AuthService:
    def __init__(self):
        self.repo = UserRepository()
    
    def inicializar_admin(self):
        self.repo.create_admin_if_not_exists()
        
    def validar_login(self, username, password):
        user = self.repo.get_by_username(username)
        return True if user and user.password == password else False