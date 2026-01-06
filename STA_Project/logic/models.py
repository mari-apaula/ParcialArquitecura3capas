from datetime import datetime

class LoteMango:
    def __init__(self, id_lote, fecha_cosecha):
        self.id_lote = id_lote
        self.fecha_cosecha = fecha_cosecha
        self.lavado = False
        self.empaquetado = False
        self.control_calidad = False
        self.temp_transporte = None
        self.fecha_entrega = None
        self.estado = "COSECHADO"

    def to_dict(self):
        return self.__dict__