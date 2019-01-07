import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
import xlrd
from xlrd import xldate_as_tuple
from datetime import datetime
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def read_excel(filename, sheetname):
    rbook = xlrd.open_workbook(filename)
    sheet = rbook.sheet_by_name(sheetname)
    rows = sheet.nrows
    cols = sheet.ncols
    all_content = []
    for i in range(rows):
        row_content = []
        for j in range(cols):
            ctype = sheet.cell(i, j).ctype  # 表格的数据类型
            cell = sheet.cell_value(i, j)
            if ctype == 3:
                # 转成datetime对象
                date = datetime(*xldate_as_tuple(cell, 0))
                cell = date.strftime('%Y/%d/%m')
            row_content.append(cell)
        all_content.append(row_content)
        #print ('[' + ','.join("'" + str(element) + "'" for element in row_content) + ']')
    return all_content

filename = r'ProjectPrototype.xlsx'
sheetname = 'clean_chegg_scholarship'
table=read_excel(filename, sheetname)



# In[20]:
nptable=np.array(table)
nptable=nptable[:,0:3]
index=nptable[0]
data=nptable[1:]
scholarship_df=pd.DataFrame(data,columns=index)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Label('Please enter key words followed by commas for the type of scholarship you want: '),
    html.Div(dcc.Input(
            id='scholarship-key-word',
            type='text'
         )),
    html.Label('Please put in the minimum amount for the schloarship you want to search (0-99999)： '),
        
    html.Div(dcc.Input(
            id='scholarship-amount',
            type='text',
            style=dict(display='inline')
        )),
            
    html.Button('Search', id='button'),
   
    html.Div(dcc.RadioItems(
        options=[
        {'label': 'Key Words', 'value': 'Key Words'},
        {'label': 'Amount', 'value': 'Amount'}
        ], 
        value='Key Words', 
        labelStyle={'display': 'inline-block'},
        id='scholarship-radio')),


    html.H4(children='Scholarships',
            id='scholarship-table'),

    dt.DataTable(
            rows=[{}], # initialise the rows
            row_selectable=False,
            filterable=False,
            sortable=True,
            selected_row_indices=[],
            id='scholarship-data-table'
            ),
])


@app.callback(
    dash.dependencies.Output('scholarship-data-table', 'rows'),
    [dash.dependencies.Input('button', 'n_clicks'),
    dash.dependencies.Input('scholarship-radio','value')],
    [dash.dependencies.State('scholarship-key-word', 'value'),
    dash.dependencies.State('scholarship-amount','value')])
def update_output(n_clicks, radio, keyword, amount):
    if n_clicks !=0 and keyword is not None and amount is not None: 
        # search by keywords
        key_result=[nptable[0]]
        keywords=keyword.split(",")
        index=1;
        for i in scholarship_df['title']:
            for k in keywords:
                if (k.strip().lower() in i.lower() and k != ""):
                    key_result.append(nptable[index])
            index+=1
        # search by amount
        amount_result=[nptable[0]]
        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        index=1;
        for i in scholarship_df['amount']:
            if(isfloat(i)):
                if (float(i)>=float(amount)):
                    amount_result.append(nptable[index])
            index+=1
            
        if(radio=='Key Words'):
            return key_result
        else:
            return amount_result

    else: 
        return None

if __name__ == '__main__':
    app.run_server(debug=True)