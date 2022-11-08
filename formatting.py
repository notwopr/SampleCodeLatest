import dash_bootstrap_components as dbc
from formatting_themes import theme_source
import plotly.graph_objects as go
import plotly.io as pio

# external
external_stylesheets = [
    dbc.themes.ZEPHYR,
    "https://fonts.googleapis.com/css2?family=Fredoka&display=swap",
    "https://fonts.googleapis.com/css2?family=Bayon&display=swap",
    "https://fonts.googleapis.com/css2?family=Oswald:wght@500&display=swap",
    "https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap",
    "https://fonts.googleapis.com/css2?family=Sanchez&display=swap"
    ]

formatting_schema = {
    # UNIVERSAL ELEMENTS
    'shadow': theme_source["shadow"],
    'sectionpadding': 'p-3',
    'sectionmargin': 'ms-4 me-4 mb-4 mt-4',
    'paper_color': theme_source["paper_color"],
    'wallpaper_color': '',
    # FONT
    'text_dark_thick': f'{theme_source["text_dark_thick"]} display-3',
    'format_heading_txt': f'{theme_source["format_heading_txt"]} display-5',
    'helpful_note_value': theme_source["helpful_note_value"],
    'helpful_note_key': '',
    # HTML TABLES
    'format_htmltable_leftcols': f'pe-2 pb-1 pt-1 {theme_source["format_htmltable_leftcols"]}',
    'format_htmltable_rightcols': f'ps-3 pb-1 pt-1 {theme_source["format_htmltable_rightcols"]}',
    'format_htmltable_row': f'{theme_source["format_htmltable_row"]} d-flex mb-3',
    # WINDOW
    'format_window': '',
    # BANNER
    'format_banner': f'{theme_source["format_banner"]} display-1 w-100',
    'format_banner_alt1': theme_source["format_banner_alt1"],
    'format_banner_alt2': theme_source["format_banner_alt2"],
    # LOGIN PAGE
    'format_success_global': f'{theme_source["format_success_global"]} ms-4 me-4 mb-4 mt-4 p-3',
    'format_navbar': f'{theme_source["format_navbar"]} ms-4 me-4 mb-4 mt-4 p-3 hstack gap-3',
    # LOGIN BODY
    'format_loginbody': 'position-absolute top-50 start-50 translate-middle',
    'format_loginbody_elements': 'hstack gap-3',
    # SERVER STATS
    'format_stats_leftcols': 'pe-3',
    'format_stats_rightcols': f'ps-3 {theme_source["format_stats_rightcols"]}',
    'format_stats_livestatus': f'ms-2 {theme_source["format_stats_livestatus"]}',
    # MISC ASSETS
    'format_tabs': f'p-4 {theme_source["format_tabs"]}',
    'buttonclass': f'{theme_source["buttonclass"]} m-1',
    'formaltextinput': 'border border-4 rounded-pill ps-3',
    'textinputboxes': 'border border-1 rounded-3 ms-2 me-2 mb-1 mt-1 w-100',
    'format_datatables': 'table table-hover',
    'format_dropdown': 'rounded-3 ms-2 me-2 mb-1 mt-1 w-auto',
    'format_radio_button': 'me-1',
    'format_radio_label': 'me-3',
    'format_checklist_boxes': 'me-1',
    'format_checklist_label': 'me-3',
    'format_logincopyright': f'{theme_source["format_logincopyright"]} bg-transparent position-absolute bottom-0 start-0 ps-2 m-0 fixed-bottom',
    # GRAPHS
    'dccgraph_config': {
        'displayModeBar': True,
        'scrollZoom': True,
        'doubleClick': 'autosize',
        'displaylogo': False,
        },
    'figure_layout_global': {
        'transition_duration': 500,
        'uirevision': 'some-constant',
        # 'font_family': theme_source['graph_font_family'],
        # 'font_size': theme_source['graph_font_size'],
        # 'font_color': theme_source['graph_font_color'],
        # 'title_font_family': theme_source['graph_title_font_family'],
        # 'title_font_color': theme_source['graph_title_font_color'],
        # 'legend_title_font_color': theme_source['graph_legend_title_font_color']
        },
    'figure_layout_mastertemplate': f'{theme_source["graph_builtin_theme"]}+global'
}

'''FIGURE_LAYOUT SETTINGS'''
pio.templates["global"] = go.layout.Template(layout=formatting_schema['figure_layout_global'])
