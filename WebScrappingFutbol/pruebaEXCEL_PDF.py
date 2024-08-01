import matplotlib
import pandas as pd



# Supongamos que tienes un DataFrame llamado df
df = pd.DataFrame({
    'Columna1': [1, 2, 3],
    'Columna2': ['A', 'B', 'C']
})

# Guardar el DataFrame en un archivo Excel
df.to_excel('dataframe.xlsx', index=False)


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Supongamos que tienes un DataFrame llamado df
df = pd.DataFrame({
    'Columna1': [1, 2, 3],
    'Columna2': ['A', 'B', 'C']
})

# Guardar el DataFrame como una imagen
fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
fig.savefig('dataframe.png')

# Crear un archivo PDF y agregar la imagen
pdf_file = 'dataframe.pdf'
c = canvas.Canvas(pdf_file, pagesize=letter)
c.drawImage('dataframe.png', 30, 500, width=500, height=200)
c.save()
