"""
Title: API Endpoint Home
Date Started: Jan 22, 2022
Version: 1.00
Version Start: Jan 22, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Main API endpoints.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
import dash
from dashappobject import app
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import datetime as dt
#   LOCAL APPLICATION IMPORTS
from webapp.servernotes import gen_serverstat
from webapp.router_directory import retrieve_bot_content, bpdict
from webapp.html_dash import gen_htmltable, gen_trlist_from_dict_footer
from file_functions import readpkl
from webapp.dashinputs import dash_inputbuilder
from formatting import formatting_schema
from file_hierarchy import DirPaths
from machinesettings import _machine
from webapp.colors import ColorGenerator

format_loginbody = formatting_schema['format_loginbody']
format_loginbody_elements = formatting_schema['format_loginbody_elements']
format_footer = formatting_schema['format_success_global']
format_main = formatting_schema['format_success_global']
format_top = formatting_schema['format_success_global']
format_navbar = formatting_schema['format_navbar']
format_banner = formatting_schema['format_banner']
format_heading_txt = formatting_schema['format_heading_txt']
formaltextinput = formatting_schema['formaltextinput']
format_logincopyright = formatting_schema['format_logincopyright']
format_stats_livestatus = formatting_schema['format_stats_livestatus']

coname = 'climb.'


def gen_banner():
    banner_base = ColorGenerator().gen_random_hex()
    banner_alt = ColorGenerator().gen_random_hex()
    coname_banner = [
        html.Span(coname[:1], style={"color": banner_base}),
        html.Span(coname[1:2], style={"color": banner_alt}),
        html.Span(coname[2:3], style={"color": banner_base}),
        html.Span(coname[3:4], style={"color": banner_alt}),
        html.Span(coname[4:5], style={"color": banner_base}),
        html.Span(coname[5:], style={"color": banner_alt})
        ]
    return coname_banner


# navbar assets
logout = dash_inputbuilder({
        'id': 'logout-button',
        'buttontext': 'logout',
        'inputtype': 'button_submit'
    })
tomain = dash_inputbuilder({
        'id': 'tomain-button',
        'buttontext': 'home',
        'inputtype': 'button_submit'
    })

success = html.Div([
    html.Div([
        html.Div(logout, id='logout'),
        html.Div(tomain, id='tomain'),
        html.Div(id='banner', className=format_banner)
        ], id='navbar', className=format_navbar),
    html.Div(id='top-content', className=format_top),
    html.Div(id='main-content', className=format_main),
    html.Div(id='bottom-content', className=format_footer)
], id='success_page', hidden='hidden')

login = html.Div([
    html.Div([
        html.H2('welcome', id='h2'),
        dash_inputbuilder({
            'id': 'pwd-box',
            'placeholdertext': 'password',
            'inputtype': 'password',
            'className': formaltextinput
        }),
        dash_inputbuilder({
            'id': 'login-button',
            'buttontext': 'enter',
            'inputtype': 'button_submit'
        }),
        html.Div(id='pw-check')
    ], className=format_loginbody_elements)
], id='login_page', hidden=None, className=format_loginbody)


# webapp layout
app.title = coname
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([login, success], id='pagecontent'),
    html.Small(f'?? 2022 {coname}', className=format_logincopyright, hidden=None, id='login_copyright'),
    dcc.Interval(
            id='serverinfo-refreshinterval',
            interval=60*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Interval(id='update-in-timer', interval=500),
    dcc.Store(id='last-update-time')
    ])


# login/logout
@app.callback(
    Output('url', 'pathname'),
    Output('login_page', 'hidden'),
    Output('success_page', 'hidden'),
    Output('pw-check', 'children'),
    Output('pwd-box', 'value'),
    Output('login_copyright', 'hidden'),
    Output('banner', 'children'),
    Input('login-button', 'n_clicks'),
    Input('pwd-box', 'value'),
    Input('logout-button', 'n_clicks'),
    Input('tomain-button', 'n_clicks')
    )
def successful(login_clicks, pw, logout_clicks, main_clicks):
    if _machine.machinename == 'awsbeanstalk':
        if callback_context.triggered[0]['prop_id'] == 'login-button.n_clicks':
            if pw == readpkl('auth', Path(DirPaths().auth)):
                return '/', 'hidden', None, None, '', 'hidden', gen_banner()
            elif pw:
                return '/', None, 'hidden', 'INVALID ENTRY', pw, None, gen_banner()
            else:
                return dash.no_update
        elif callback_context.triggered[0]['prop_id'] == 'logout-button.n_clicks':
            return '/', None, 'hidden', None, '', None, gen_banner()
        elif callback_context.triggered[0]['prop_id'] == 'tomain-button.n_clicks':
            return '/', 'hidden', None, None, '', 'hidden', gen_banner()
        elif pw == '':
            return '/', None, 'hidden', None, pw, None, gen_banner()
        else:
            return '/', None, 'hidden', None, pw, None, gen_banner()
    else:
        return '/', 'hidden', None, None, '', 'hidden', gen_banner()


# Update top content
@app.callback(Output('top-content', 'children'),
              Input('url', 'pathname'))
def gen_top_content(pathname):
    if pathname[1:] in bpdict.keys():
        if pathname[1:] == 'strat_ranker' or pathname[1:] == 'strattester':
            header = f"{bpdict[pathname[1:]].botid} [DEPRECATED]"
        else:
            header = bpdict[pathname[1:]].botname
        intro = bpdict[pathname[1:]].botdesc
    elif pathname == '/':
        header = 'welcome'
        intro = 'Below are links to the different investing tools available on this platform.  Have a nice day.'
    else:
        header = 'PAGE NOT FOUND!'
        intro = 'Please correct the URL.  If the URL is correct, please contact an administrator for help.'
    return [
        html.Div(header.title(), id='heading', className=format_heading_txt),
        html.P(intro, id='intro'),
        html.Small("WARNING: Depending on the inputs you set, these tools may require considerable computing power, which at present we do not have.  As a result, you may experience slow processing times.  If you would like to run an expensive task, please contact us to arrange for a demonstration.", className="text-danger")
        ]


# Update main content
@app.callback(Output('main-content', 'children'),
              Input('url', 'pathname'))
def gen_main_content(pathname):
    if pathname[1:] in bpdict.keys():
        return retrieve_bot_content(pathname[1:], 'layout')
    elif pathname == '/':
        return html.P([
                html.Span([
                    dcc.Link(
                            b.botname,
                            b.botpath
                        ),
                    html.Br()
                ]) for b in bpdict.values()
            ])
    else:
        return 'PAGE NOT FOUND!'


# Update countdown timer
js_counter = """
function counting_down(n, last, interval) {

    t =  Math.trunc((interval - (Date.now() - last*1000))/1000);

    return `refreshes in: ${t} secs`
}
"""


# Update the bottom content
@app.callback(
                Output('bottom-content', 'children'),
                Output('last-update-time', 'data'),
                Input('url', 'pathname'),
                Input('serverinfo-refreshinterval', 'n_intervals'))
def gen_bottom_content(pathname, refresh_interval):
    return [
        html.Strong(html.Small('Database Info')), html.Small(id='refreshtimer_count', className=format_stats_livestatus),
        html.Br(),
        gen_htmltable(gen_trlist_from_dict_footer(gen_serverstat())),
        html.Small(f'?? 2022 {coname}'),
    ], dt.datetime.now().timestamp()


app.clientside_callback(
    js_counter,
    Output('refreshtimer_count', 'children'),
    Input('update-in-timer', 'n_intervals'),
    State('last-update-time', 'data'),
    State('serverinfo-refreshinterval', 'interval')
)

application = app.server

if __name__ == '__main__':
    if _machine.machinename == 'awsbeanstalk':
        application.run(debug=False)
    else:
        app.run_server(debug=True)
