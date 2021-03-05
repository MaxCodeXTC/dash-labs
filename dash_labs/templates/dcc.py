from dash_labs.templates.base import BaseTemplate
import dash_html_components as html
import dash_core_components as dcc


class DccCard(BaseTemplate):
    _inline_css = """
        <style>
        .dcc-slider {
            padding: 12px 20px 12px 20px !important;
         }
        </style>"""

    def __init__(self, title=None, width=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.width = width

    def _perform_layout(self):
        # No callbacks here. Must be constant or idempotent
        children = []
        if self.title:
            children.append(html.H2(self.title))

        children.append(html.Div(self.get_containers("output")))
        children.append(html.Hr())
        children.append(html.Div(self.get_containers("input")))
        layout = html.Div(
            style={
                "width": self.width,
                "border": "1px solid lightgray",
                "padding": 10,
                "border-radius": "6px",
            },
            children=html.Div(children=children),
        )
        return layout