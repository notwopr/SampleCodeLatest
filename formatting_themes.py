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

theme_directory = {
    'cooper': {
        # UNIVERSAL ELEMENTS
        'shadow': 'shadow-lg',
        'paper_color': 'paper',
        # FONT
        'text_dark_thick': 'fw-bold charcoal_txt',
        'format_heading_txt': 'fw-bold font_heading',
        'helpful_note_value': 'fadedpurple_txt',
        # HTML TABLES
        'format_htmltable_leftcols': 'bg-transparent',
        'format_htmltable_rightcols': 'bg-transparent',
        'format_htmltable_row': 'border border-light shadow-lg rounded-1 bg-white',
        # BANNER
        'format_banner': 'fw-bold font_banner text-end',
        'format_banner_alt1': 'darkgrey_txt',
        'format_banner_alt2': 'alt2_txt',
        # LOGIN PAGE
        'format_success_global': 'paper shadow-lg',
        'format_navbar': 'paper shadow-lg',
        # 'format_top': f'{format_success_global}',
        # 'format_main': f'{format_success_global}',
        # 'format_footer': f'{format_success_global}',
        # LOGIN BODY
        # SERVER STATS
        'format_stats_rightcols': 'text-info',
        'format_stats_livestatus': 'badge bg-success',
        # GRAPHING
        'graph_builtin_theme': 'plotly_dark',
        'graph_font_family': '',
        'graph_font_size': 10,
        'graph_font_color': "blue",
        'graph_title_font_family': "Times New Roman",
        'graph_title_font_color': "red",
        'graph_legend_title_font_color': "green",
        # MISC ASSETS
        'format_tabs': 'bg-white',
        'buttonclass': 'btn btn-outline-dark',
        'format_logincopyright': 'fw-bold offwhite_txt font_logincopyright fs-3',
    },
    'duke': {},
    'reed': {},
    'grayson': {},
    'chase': {},
    'chance': {},
    'bryce': {},
    'mason': {},
    'brant': {}
}
chosentheme = 'cooper'
theme_source = theme_directory[chosentheme]
