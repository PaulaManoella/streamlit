# import streamlit as st
# import plotly.express as px
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
# import plotly.io as pio

def gerar_pdf_streamlit(fig) -> BytesIO:
    # 1. Salvar gráfico como imagem temporária em memória
    img_bytes = fig.to_image(format="png", width=1000, height=600, engine="kaleido")
    img = Image.open(BytesIO(img_bytes))

    # 2. Criar PDF em memória
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, altura - 50, "Relatório - Gráfico de Médias por Questão")

    # Ajustar tamanho da imagem para caber no PDF
    img_width, img_height = img.size
    max_width = largura - 100
    max_height = altura - 150
    scale = min(max_width / img_width, max_height / img_height)

    new_width = img_width * scale
    new_height = img_height * scale

    x = (largura - new_width) / 2
    y = altura - new_height - 100

    # Salvar imagem no disco temporariamente porque reportlab não aceita BytesIO direto
    temp_path = "/tmp/temp_img.png"  # em deploy usa /tmp/
    img.save(temp_path)

    c.drawImage(temp_path, x, y, width=new_width, height=new_height)
    c.showPage()
    c.save()

    # 3. Retornar buffer com o conteúdo do PDF
    buffer.seek(0)
    return buffer