"""
Title: HTML
Date Started: Jan 22, 2022
Version: 1.00
Version Start: Jan 22, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  HTML coding matters.
"""


# generate server notes
def html_servernotes(server_stats):
    return ''.join([f'{s}<br>' for s in server_stats])


# generate one html string for a list
def html_listcontents(contents):
    return ''.join([f'<p>{i}</p>' for i in contents])


# generate one html string for multiple assets
def html_multireports(listofreports):
    return ''.join([f'<div>{j}</div><br><br>' for j in listofreports])


# generate one html string for multiple tables
def html_multitable(listoftables):
    return ''.join([f'<p>{table}</p>' for table in listoftables])


# generates HTML body content
def html_body(heading, intro, mainscheme, notes):
    bodyscheme = f"""
    <div>
        <h1>{heading}</h1>
        <p>{intro}</p>
    </div>
    <div>
        {mainscheme}
    </div>
    <div>
        {notes}
    </div>
    """
    return bodyscheme


# generates HTML code for HTML pandas df to table
def format_htmltable(table_id):
    return f"""
        <script type="text/javascript" src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/jszip-2.5.0/dt-1.11.4/b-2.2.2/b-colvis-2.2.2/b-html5-2.2.2/b-print-2.2.2/cr-1.5.5/fc-4.0.1/fh-3.2.1/datatables.min.css"/>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.36/pdfmake.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.36/vfs_fonts.js"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/v/dt/jszip-2.5.0/dt-1.11.4/b-2.2.2/b-colvis-2.2.2/b-html5-2.2.2/b-print-2.2.2/cr-1.5.5/fc-4.0.1/fh-3.2.1/datatables.min.js"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.11.4/js/dataTables.bootstrap5.min.js"></script>
        <script type="text/javascript" class="init">
            $(document).ready( function () {{$('#{table_id}').DataTable(
                {{
                    dom: 'B<"clear">lfrtip',
                    buttons: ['csv', 'copy', 'excel', 'pdf', 'print', 'colvis'],
                    fixedHeader: true,
                    paging: false,
                    fixedColumns: {{left: 2}}
                }}
            );}});
        </script>
    """


# generates HTML response for API
def gen_html(title, headercode, body):
    html_content = f"""
        <!DOCTYPE html>
            <head>
                <title>{title}</title>
                {headercode}
            </head>
            <body>
                {body}
                <span>© 2022 Aimpoint Labs.</span>
            </body>
        </html>
    """
    return html_content


def html_dropdown(contents):
    return ''.join([f'<option value="{i}">{i}</option>' for i in contents])


def html_inputformbuilder(criteria):
    htmlcode = ''''''
    for c in criteria:
        labelsnip = f'''<label for={c['name']}>{c['prompt']}</label>'''
        if c['inputtype'] == 'range' or c['inputtype'] == 'number':
            inputsnip = f'''<input type={c['inputtype']} size={c['size']} inputmode="numeric" name={c['name']} min={c['min']} max={c['max']} formenctype='multipart/form-data'>'''
        elif c['inputtype'] == 'text':
            inputsnip = f'''<input type='text' name={c['name']} pattern={c['pattern']} formenctype='multipart/form-data'>'''
        elif c['inputtype'] == 'float':
            inputsnip = f'''<input type='number' step='any' name={c['name']} formenctype='multipart/form-data'>'''
        elif c['inputtype'] == 'dropdown':
            inputsnip = f'''<select name={c['name']} id={c['name']}>
                  {html_dropdown(c['contents'])}
                </select>
                '''
        elif c['inputtype'] == 'filter':
            inputsnip = f'''<select name={c['name']} id={c['name']}>
                  <option value="<"><</option>
                  <option value="<="><=</option>
                  <option value=">">></option>
                  <option value=">=">>=</option>
                </select>
                '''
        elif c['inputtype'] == 'yesno':
            inputsnip = f'''<select name={c['name']} id={c['name']}>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
                '''
        elif c['inputtype'] == 'date':
            inputsnip = f'''<input type={c['inputtype']} name={c['name']} min={c['min']} max={c['max']} formenctype='multipart/form-data'>'''
        elif c['inputtype'] == 'datelist':
            inputsnip = f'''<input type='text' name={c['name']} formenctype='multipart/form-data'>'''
        htmlcode += f'''<div>{labelsnip}{inputsnip}</div>'''
    return htmlcode


def html_entirepage(title, headercode, intro, mainscheme, server_stats):
    return gen_html(
        title,
        headercode,
        html_body(title, intro, mainscheme, html_servernotes(server_stats))
        )


# bis = botinputscheme
def html_botinputscheme(botpath, botrs, inputslist):
    return f'''
            <form action="{botpath}{botrs}" method='post'>
                {html_inputformbuilder(inputslist)}
                <input type="submit" value="Submit">
                <input type="reset">
            </form>
            '''
