from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly

with ui.sidebar():
    ui.input_text("text", label="Introduce el nombre del artista")

with ui.nav_panel("Gráfico 1"):
    
    with ui.card():
        ui.card_header("Tu artista es: ", 
                        style="color:white; background:#2A2A2A !important;")
        @render.text
        def text_out():
            return f"{input.text()}"
    
    @render_plotly
    def hist():
        import plotly.express as px
        return px.histogram(px.data.tips(), x="tip")

with ui.nav_panel("Gráfico 2"):
    "Page 2 content"

