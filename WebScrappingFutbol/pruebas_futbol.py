import re

def extraer_nombre(scorer):
    # Usar expresión regular para capturar solo el nombre
    match = re.match(r"([^\d]+)", scorer)
    if match:
        return match.group(1).strip()
    return scorer.strip()

# Ejemplo de uso
scorer = "Dusan Vlahovic 19' (p),89(o)"
nombre = extraer_nombre(scorer)
print(nombre)  # Output: Dusan Vlahovic




