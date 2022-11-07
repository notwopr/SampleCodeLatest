import plotly.graph_objects as go
import plotly.io as pio

'''dcc.Graph settings'''
dccgraph_config = {
    'displayModeBar': True,
    'scrollZoom': True,
    'doubleClick': 'autosize',
    'displaylogo': False,
    }

'''FIGURE SETTINGS'''

'''FIGURE_LAYOUT SETTINGS'''
'''
built-in templates
[
    'ggplot2',
    'seaborn',
    'simple_white',
    'plotly',
    'plotly_white',
    'plotly_dark',
    'presentation',
    'xgridoff',
    'ygridoff',
    'gridon',
    'none'
]
'''
pio.templates["global"] = go.layout.Template(
    layout={
        'transition_duration': 500,
        'uirevision': 'some-constant'
        }
)

figure_layout_mastertemplate = 'plotly_dark+global'
