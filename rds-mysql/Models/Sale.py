class Sale:
    def __init__(self, venta_id, cliente_cedula, total):
        self.venta_id = venta_id
        self.cliente_cedula = cliente_cedula

        if total <= 0:
            raise ValueError('El total debe ser mayor que cero.')

        self.total = total
    
    def toDict(self):
        return{
            "id" : self.venta_id,
            "cliente_cedula" : self.venta_id,
            "total" : self.total
        }