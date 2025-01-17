# Predefined templates
This section describes the templates that are provided with Dash Labs.

Here is a full example, specifying the `FlatDiv` template.  The following examples will only contain code for the template declaration line.

[demos/all_templates.py](./demos/all_templates.py)

```python
import dash
import dash_labs as dl
import numpy as np
import plotly.express as px

# Make template
tpl = dl.templates.FlatDiv()

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])

@app.callback(
    args=dict(
        fun=tpl.dropdown_input(["sin", "cos", "exp"], label="Function"),
        figure_title=tpl.textbox_input("Initial Title", label="Figure Title"),
        phase=tpl.slider_input(1, 10, label="Phase"),
        amplitude=tpl.slider_input(1, 10, value=3, label="Amplitude"),
    ),
    output=tpl.graph_output(),
    template=tpl
)
def callback(fun, figure_title, phase, amplitude):
    xs = np.linspace(-10, 10, 100)
    np_fn = getattr(np, fun)

    # Let parameterize infer output component
    x = xs
    y = np_fn(xs + phase) * amplitude
    return px.line(x=x, y=y).update_layout(title_text=figure_title)


app.layout = tpl.layout(app)

if __name__ == "__main__":
    app.run_server(debug=True)
```

### FlatDiv
The `FlatDiv` template arranges all the input and output containers as children of a top-level `Div` component, and makes no attempt to make the result look nice.

```python=
tpl = dl.templates.FlatDiv()
```

![](https://i.imgur.com/AV9yqRQ.png)

### HtmlCard

The `HtmlCard` template has no external dependencies and uses some basic inline CSS to place the input and output in a card with a title on top.  It currently puts very little effort into making the result look nice (although this could change).

```python=
tpl = dl.templates.HtmlCard(title="Dash Labs App", width="500px")
```

![](https://i.imgur.com/E9865h3.png)

### DbcCard

The `DbcCard` template introduces a dependency on the open source Dash Bootstrap Components library (https://dash-bootstrap-components.opensource.faculty.ai/).  It places all contents in a single bootstrap card, with a card title.

```python=
tpl = dl.templates.DbcCard(title="Dash Labs App", columns=6)
```

![](https://i.imgur.com/FiZAOFv.png)

### DbcRow

The `DbcRow` template places the inputs and outputs in separate cards and then arranges them in a Bootstrap row. This template is a great choice when integrating the components generated by the template into a larger app made with Dash Bootstrap Components.

```python=
tpl = dl.templates.DbcRow(title="Dash Labs App")
```

![](https://i.imgur.com/zW5z2Eh.png)

### DbcSidebar

The `DbcSidebar` template creates an app title bar and then includes the inputs in a sidebar on the left of the app, and the outputs in a card in the main app area.  This is a great choice when using a template to build an entire app.

```python=
tpl = dl.templates.DbcSidebar(title="Dash Labs App")
```

![](https://i.imgur.com/FEpzde2.png)

### DdkCard

The `DdkCard` template introduces a dependency on the proprietary Dash Design Kit library that is included with Dash Enterprise.  Like `DbcCard`, in places all the outputs and inputs in a single card, along with a card title.

```python=
tpl = dl.templates.DdkCard(title="Dash Labs App", width=50)
```

![](https://i.imgur.com/Vt2o8td.png)

### DdkRow

Like the `DbcRow` template, `DdkRow` places the input and output components in separate cards, and then places those cards in a ddk row container.


```python=
tpl = dl.templates.DdkRow(title="Dash Labs App")
```

![](https://i.imgur.com/iqgyeTf.png)

### DdkSidebar

The `DdkSidebar` template creates a full app experience with an app header, a sidebar for the input controls, and a large main area for the output components.

```python=
tpl = dl.templates.DdkSidebar(title="Dash Labs App")
```

![](https://i.imgur.com/OKYOFYY.png)

### Themed DbcSidebar

All of the `Dbc*` components can be themed using the Bootstrap themeing system. Simply pass the URL of a bootstrap theme css file as the `theme` argument of the template. Check out https://www.bootstrapcdn.com/bootswatch/ to browse available templates.

#### Bootstrap figure theming
Templates based on Dash Bootstrap Components have the ability to dynamically generate a plotly.py figure template from the bootstrap CSS theme file. This is enabled by setting `figure_template=True` in the constructor of a Dash Bootstrap Components template. 


```python=
tpl = dl.templates.DbcSidebar(
    title="Dash Labs App", 
    theme="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/superhero/bootstrap.min.css",
    figure_template=True
)
```

![](https://i.imgur.com/lLZrDfY.png)

or use the convenience theme values provided by Dash Bootstrap Components

```python
import dash_bootstrap_components as dbc
tpl = dl.templates.DbcSidebar(
    title="Dash Labs App",
    theme=dbc.themes.CYBORG,
)
```

### Themed DdkSidebar

Custom DDK themes created by hand, or using the DDK editor can be passed as the `theme` argument to any of the `Ddk*` templates.

Theme in [demos/ddk_theme.py](./demos/ddk_theme.py)

```python=
from my_theme import theme
tpl = dl.templates.DdkSidebar(title="Dash Labs App", theme=theme)
```

![](https://i.imgur.com/PIAywnx.png)

## Sidebar Tabs Templates
Dash Labs provides a more advanced template style that support displaying callback outputs across a collection of tabs.  These are `DbcSidebarTabs` and `DdkSidebarTabs` which use the Dash Bootstrap Components and Dash Design Kit libraries respectively.

These template have a required `tabs` argument that should be set to either:
  1. A list of tab titles. In this case the tab values will match the tab titles.
  2. A dict from tab values to tab titles.

Each tab value becomes a valid template `role`, making it possible to associate callback input and/or output components with individual tabs.

These templates also provide a `tab_input` method that returns an `dl.Input` dependency associated with the active tab value.  This can be used to pass the active tab value into the callback function.

Here is an example

```python
import dash
import dash_labs as dl
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])

# Load gapminder dataset
df = px.data.gapminder()
years = sorted(df.year.drop_duplicates())
continents = list(df.continent.drop_duplicates())

# Build Themed Template
theme_name = "darkly"
css_url = f"https://bootswatch.com/4/{theme_name}/bootstrap.css"

tpl = dl.templates.DbcSidebarTabs(
    ["Scatter", "Histogram"],
    title=f"Dash Labs - {theme_name.title()} Theme",
    theme=css_url, figure_template=True
)

@app.callback(
    args=dict(
        continent=tpl.checklist_input(continents, value=continents, label="Continents"),
        year=tpl.slider_input(
            years[0], years[-1], step=5, value=years[-1], label="Year"
        ),
        logs=tpl.checklist_input(
            ["log(x)"], value="log(x)", label="Axis Scale", role="Scatter"
        ),
        tab=tpl.tab_input(),
    ),
    output=[
        tpl.graph_output(role="Scatter"),
        tpl.graph_output(role="Histogram"),
    ],
    template=tpl,
)
def callback(year, continent, logs, tab):
    print(f"Active Tab: {tab}")
    logs = logs or []

    # Let parameterize infer output component
    year_df = df[df.year == year]
    if continent:
        year_df = year_df[year_df.continent.isin(continent)]

    if not len(year_df):
        return [go.Figure(), go.Figure()]

    title = f"Life Expectancy ({year})"
    scatter_fig = (
        px.scatter(
            year_df,
            x="gdpPercap", y="lifeExp",
            size="pop", color="continent",
            hover_name="country", log_x="log(x)" in logs,
            size_max=60,
        )
        .update_layout(title_text=title, margin=dict(l=0, r=0, b=0))
        .update_traces(marker_opacity=0.8)
    )

    hist_fig = px.histogram(
        year_df, x="lifeExp", color="continent", barnorm=""
    ).update_layout(
        title_text=title,
    )

    return scatter_fig, hist_fig

app.layout = tpl.layout(app)

if __name__ == "__main__":
    app.run_server(debug=True)
```

![](https://i.imgur.com/XH62pPe.gif)

## Creating custom templates
Custom templates can be created by subclassing the `dl.template.base.BaseTemplate` class. Or, for a custom Bootstrap Components template, subclass `dl.teamplates.dbc.BaseDbcTemplate`. Similarly, to create a custom DDK template, subclass `dl.templates.ddk.BaseDdkTemplate`.

Overriding a template may involve:
 1. Customizing the components that are constructed by `tp.dropdown_input`, `tp.graph_output`, etc.
 2. Specifying the representation of component labels.
 3. Specifying how a component and label are group together into a container.
 4. Specifying how the input and output containers created in (3) are combined into a single layout container
 5. Providing custom inline CSS which gets inserted into `index.html`.
 6. Providing custom roles (in addition to `"input"` and `"output"`).
