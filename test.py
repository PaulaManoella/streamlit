import plotly.express as px
import plotly.io as pio
import tempfile

fig = px.line(x=["Q1", "Q2", "Q3"], y=[[10, 20, 30], [15, 25, 35], [20, 30, 40], [5, 10, 15]])

colors = ['red', 'orange', 'green', 'gray']
for i, color in enumerate(colors):
    fig.data[i].line.color = color

with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
    fig.write_image(tmp_img.name, engine="kaleido")
    print("Imagem salva em:", tmp_img.name)
