from datetime import datetime

# Cadena de fecha y hora
cadena_fecha = "S-12/08 09:00"

# Definir el formato de la cadena de fecha
formato_fecha = "%a-%d/%m %H:%M"

# Convertir la cadena a un objeto datetime
fecha_valida = datetime.strptime(cadena_fecha, formato_fecha)

# Imprimir la fecha en formato datetime
print(fecha_valida)