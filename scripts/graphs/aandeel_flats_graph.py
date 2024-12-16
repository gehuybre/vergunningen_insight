#scripts\graphs\aandeel_flats_graph.py
import pandas as pd
import plotly.express as px
import json
import os

def create_aandeel_flats_graph():
    # Zorg ervoor dat de paden correct zijn ten opzichte van het huidige script
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    input_file = os.path.join(base_dir, 'data', 'aandeel_flats_pivot.csv')
    output_file = os.path.join(base_dir, 'graphs', 'aandeel_flats_pivot.html')
    config_file = os.path.join(base_dir, 'static', 'json', 'graphs-config.json')


    # Print de paden voor debugging
    print(f"Input file path: {input_file}")
    print(f"Output file path: {output_file}")
    print(f"Config file path: {config_file}")

    # Zorg ervoor dat de uitvoermap bestaat
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Controleer of het inputbestand bestaat
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Controleer of het configuratiebestand bestaat
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    # Lees het invoerbestand
    df = pd.read_csv(input_file)

    # Laad de configuratie
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Print the loaded configuration
    print("Loaded Config:", config)

    # Maak een Plotly-grafiek
    fig = px.line(
        df,
        x='Year-Quarter',
        y=['aandeel-flats'],
        labels={
            'value': 'Aantal wooneenheden',
            'variable': 'Type woning',
            'Year-Quarter': 'Kwartaal'
        },
        title='Vergunningsaanvragen voor aandeel_flats'
    )

    # Pas de lay-out aan op basis van de configuratie
    fig.update_layout(**config["layout"])

    # Pas trace-instellingen aan
    for trace, trace_config in zip(fig.data, config["traces"]["line"]):
        trace.update(line=dict(color=trace_config["color"], width=trace_config["width"]))

    # Sla de grafiek op als HTML
    fig.write_html(output_file)

    print(f"Graph saved to {output_file}")

    return fig

if __name__ == "__main__":
    create_aandeel_flats_graph()