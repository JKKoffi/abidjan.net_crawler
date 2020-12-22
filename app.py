import dash
import dash_core_components as dcc
import dash_html_components as html

import numpy as np
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from datetime import date
from datetime import datetime
import os

from crawler import *

app = dash.Dash('Crawler')



app.layout = html.Div([
	#title
	html.Div(children = [
		html.H2("Abidjan.net Crawler")
	], className='banner'),
	

	 html.Br(),

	html.Div(children = [

		html.Div(children = "Options", style={'textAlign':'center','color':'wite'}),
		html.Br(),
		dcc.RadioItems(
			id = 'id_choice',
			options = [
				 {'label':'By ID','value':'0'},
				 {'label':'By Date','value':'1'},
				 {'label':'By file','value':'2'} 
			],
			labelStyle={'display': 'inline-block'}
		),

		#  html.Br(),

		html.Div([
			dcc.Input(
				id = "id_By_ID",
				type = 'number',
				placeholder = 'Enter an integer',style={'display': 'none', 'textAlign': 'center'}
			),

			html.Br(),

			
			dcc.DatePickerSingle(
				id='id_date',
				min_date_allowed=date(1997, 8, 5),
				max_date_allowed= datetime.now(),
				initial_visible_month=date(2017, 8, 5),
				date=date(2017, 8, 25),
				clearable=True,
				 with_portal=True,
				style={
					'width': '20%',
					'height': '50px',
					'lineHeight': '60px','borderWidth': '1px','textAlign': 'center','display': 'none'

						# 'margin': '10px'#,'borderRadius': '5px'
				}
			),

			html.Br(),

			dcc.Upload(
				id='id_file',
				children=html.Div([
					'Drag and Drop or ',
					html.A('Select Files')
				]),
				style={
					'width': '20%',
					'height': '50px',
					'lineHeight': '60px','borderWidth': '1px','textAlign': 'center',
					'borderStyle': 'dashed','display': 'none'
					# 'margin': '10px','borderRadius': '5px'
				},
				# Allow multiple files to be uploaded
				multiple=False
			),

			html.Br(),


			html.Button('Start Crawler',id='id_start', style = {'display':'none',  'width': '20%','height': '50px'}),
					
					

		]
		
		)
		# html.Br()


	]),


	# html.Div(id = 'id_progress')
	html.Hr(),

	html.Div(children = [	
		dash_table.DataTable(
			id='id_table',# rows=[{}],
			 editable=True,
			 row_deletable=True
			 ),

		# html.Br()

		# html.Div(id = "id_summary")
		html.Div()
	])


],style = {'textAlign':'center','color':'pink'})



"""
callback functions
"""
#deactivate components
# @app.callback([	Output('id_By_ID', 'disabled'),	Output('id_Date', 'disabled'),Output('id_file', 'disabled')],
#              [Input('id_choice', 'value')])
# def set_choice_enabled_state(on_off):
# 	if on_off =='0':return False,True,True
# 	elif on_off=='1': return True,False,True
# 	elif on_off=='2': return True,True,False
		
#deactivate components
@app.callback([	Output('id_By_ID', 'style'),	Output('id_date', 'style'),Output('id_file', 'style'),Output('id_start', 'style')],
             [Input('id_choice', 'value')])
def update_style_components(on_off):
	if on_off =='0':return {'display': 'block'},{'display': 'none'},{'display': 'none'},{'display': 'block'}
	elif on_off=='1': return {'display': 'none'}, {'display': 'block'},{'display': 'none'},{'display': 'block'}
	elif on_off=='2': return {'display': 'none'},{'display': 'none'},{'display': 'block'},{'display': 'block'}


@app.callback([Output('id_table',component_property='data')],
					 
						 Input('id_choice', 'value'),
						 Input('id_By_ID', 'value'),
						 Input('id_date', 'date'),
						 Input('id_file', 'contents'),
						Input('id_start', 'n_clicks'),
						 
						#  State('id_start', 'value'),
						#   State('id_file', 'filename')
					 )
def update_table_data(choice,id, date_value,filename,n_clicks ):
	if choice=='0':
		print(choice)
		if id!=None:
			if n_clicks>0:
				df_links = search_links_id(id)
				print(df_links.shape[0])
				df_merged = crawl_data(df_links)
				df_merged = search_fileds(df_merged)

				columns = [{'name': col, 'id': col} for col in df_merged.columns]
				data = df_merged.to_dict(orient='records')
				return data
	if choice=='1':
		if date_value is not None:
			if n_clicks>0:
		
				date_object = date.fromisoformat(date_value)
				date_string = date_object.strftime("%d %m %Y")

				df_links = search_links_date(date_string)
				df_merged = crawl_data(df_links)
				df_merged = search_fileds(df_merged)

				columns = [{'name': col, 'id': col} for col in df_merged.columns]
				data = df_merged.to_dict(orient='records')
				return data
	if choice=='2':
		if n_clicks>0:
		
			try:
				# content_type, content_string = contents.split(',')
				# decoded = base64.b64decode(content_string)

				df_merged = pd.read_csv(filename, encoding='utf-16le' )
				
				df_merged = search_fileds(df_merged)

				columns = [{'name': col, 'id': col} for col in df_merged.columns]
				data = df_merged.to_dict(orient='records')
				return data
			except:
				pass


    			
				

if __name__ == '__main__':
    app.run_server(debug=True)

