import os
from jinja2 import Environment, FileSystemLoader
from graphs.nieuwbouw_graph import create_nieuwbouw_graph
from graphs.renovatie_graph import create_renovatie_graph
from graphs.sloop_graph import create_sloop_graph
from graphs.aandeel_flats_graph import create_aandeel_flats_graph
import shutil

def generate_report():
    """Generates the HTML report by combining graphs and the report template."""

    # Construct the path to the base directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(base_dir, 'template')
    output_dir = os.path.join(base_dir, 'output')
    output_report_path = os.path.join(output_dir, 'report.html')
    static_dir = os.path.join(base_dir, 'static')
    output_static_dir = os.path.join(output_dir, 'static')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')

    # Generate graphs
    nieuwbouw_plot = create_nieuwbouw_graph()
    renovatie_plot = create_renovatie_graph()
    sloop_plot = create_sloop_graph()
    aandeel_flats_plot = create_aandeel_flats_graph()

    # Prepare HTML representations of the graphs
    nieuwbouw_html = nieuwbouw_plot.to_html(full_html=False, include_plotlyjs='cdn')
    renovatie_html = renovatie_plot.to_html(full_html=False, include_plotlyjs='cdn')
    sloop_html = sloop_plot.to_html(full_html=False, include_plotlyjs='cdn')
    aandeel_flats_html = aandeel_flats_plot.to_html(full_html=False, include_plotlyjs='cdn')

    # Render the template with the graphs
    rendered_html = template.render(
        nieuwbouw_graph=nieuwbouw_html,
        renovatie_graph=renovatie_html,
        sloop_graph=sloop_html,
        aandeel_flats_graph=aandeel_flats_html
    )

    # Save the final HTML report
    with open(output_report_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    print(f"Report saved to {output_report_path}")

    # Copy the static folder to output directory
    if os.path.exists(static_dir):
        if os.path.exists(output_static_dir):
            shutil.rmtree(output_static_dir) # remove the old folder
        shutil.copytree(static_dir, output_static_dir)
        print(f"Copied static folder to {output_static_dir}")
    else:
        print(f"Warning: static folder not found at {static_dir}")

if __name__ == "__main__":
    generate_report()