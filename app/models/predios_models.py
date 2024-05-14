class Predios:

    def __init__(self, id_predio, predio, propietario, domicilio, colonia, ref_ubicacion, medidor):
        self.id_predio = id_predio
        self.predio = predio
        self.propietario = propietario
        self.domicilio = domicilio
        self.colonia = colonia
        self.ref_ubicacion = ref_ubicacion
        self.medidor = medidor
    
    def __repr__(self) -> str:
        return f"Predio(\
            predio={self.predio}, \
            propietario={self.propietario}, \
            domicilio={self.domicilio}, \
            colonia={self.colonia}, \
            ref_ubicacion={self.ref_ubicacion}, \
            medidor={self.medidor} \
        )"

        
