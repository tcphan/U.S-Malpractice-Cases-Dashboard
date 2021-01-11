import pandas as pd
import numpy as np
import plotly as pyo
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
from dash_table.Format import Format, Symbol, Group

#******************************************************************************
#SECTION I: READING AND CLEANING OF INPUT FILES
#******************************************************************************

#file path to NPD input file
npdb_filepath = r"C:\Users\tcphan\OneDrive\Documents\kaggle_projects\NpdbPublicUseData\data\NPDB2004.csv"
#read in input file into dataframe
npdb_df = pd.read_csv(npdb_filepath, low_memory = False)

#remove dollar sign from string
npdb_df["TOTALPMT"] = npdb_df["TOTALPMT"].str.replace("$", "")
#convert total payment column to float data type
npdb_df["TOTALPMT"] = npdb_df["TOTALPMT"].astype(float)
#convert year value to integer format
npdb_df["ORIGYEAR"] = npdb_df["ORIGYEAR"].astype(int)

#******************************************************************************
#SECTION II: STYLE/FORMATTING PARAMETERS
#******************************************************************************

#color RGBs
primary_color = "rgb(50, 93, 136)"
secondary_color = "rgb(142, 140, 132)"
tertiary_color = "rgb(244, 243, 240)"
success_color = "rgb(147, 197, 75)"
info_color = "rgb(41, 171, 224)"
warning_color = "rgb(244, 124, 60)"
danger_color = "rgb(217, 83, 79)"
light_color = "rgb(248, 245, 240)"
dark_color = "rgb(62, 63, 58)"

#******************************************************************************
#SECTION III: DEFINE APP DASHBOARD
#******************************************************************************

#initialize dash application
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SANDSTONE])

#define the layout for the dashboard
app.layout = html.Div(style = {"backgroundColor": tertiary_color},
                      children = [
        
        
                #row 1
                dbc.Row(
                        children = [
                        
                        dbc.Col(width = {"size": "auto", "order": 1, "offset": 6},
                                children = [html.H3("U.S MALPRACTICE CASES BETWEEN", style = {"fontWeight": "bold", "color": primary_color})]),
                                

                       dbc.Col(width = {"size": "auto", "order": 2}, style = {"width": "150px"},
                               children = [dbc.Input(id = "malp_start_year",
                                                     type = "number", 
                                                     min = npdb_df["ORIGYEAR"].min(),
                                                     max = npdb_df["ORIGYEAR"].max(), 
                                                     step = 1,
                                                     style = {"textAlign": "center"},
                                                     value = npdb_df["ORIGYEAR"].min())]),
                               
                       dbc.Col(width = {"size": "auto", "order": 3},
                               children = [html.H3("AND", style = {"fontWeight": "bold", "color": primary_color})]),
                               
                       dbc.Col(width = {"size": "auto", "order": 4}, style = {"width": "150px"},
                               children = [dbc.Input(id = "malp_end_year",
                                                     type = "number", 
                                                     min = npdb_df["ORIGYEAR"].min(),
                                                     max = npdb_df["ORIGYEAR"].max(),
                                                     step = 1,
                                                     style = {"textAlign": "center"},
                                                     value = npdb_df["ORIGYEAR"].max())])
                               
                            
                       ]), #end of row 1
        
                #row 2
                dbc.Row(justify = "end",
                        children = [
                                
                            dbc.Col(width = {"size": 3},
                                    children = [
                                                 html.Div(style = {"position": "fixed",
                                                                   "top": 0,
                                                                   "left": 0,
                                                                   "bottom": 0,
                                                                   "background-color": primary_color,
                                                                   "width": "25rem",
                                                                   "padding": "2rem 1rem"},

                                                          children = [
                                                                      
                                                                      html.H2("MEDICAL MALPRACTICE IN THE UNITED STATES",
                                                                              style = {"fontWeight": "bold", "color": warning_color}),
                                                                      
                                                                      html.Hr(style = {"height": "1px", "backgroundColor": dark_color}),
                                                                      
                                                                      html.H4("PURPOSE:", style = {"fontWeight": "bold", "color": warning_color}),
                                                                      dcc.Markdown("""
                                                                                   * To provide greater insight into the frequency and cost of medical malpractice/adverse events in the United States.
                                                                                   
                                                                                   * To engender transparency and proactive legislations preventing unprofessional practitioners from moving to different state jurisdiction
                                                                                     without full disclosure of prior adverse behaviors and actions.
                                                                                     
                                                                                   * To improve overall patient safety and care quality.
                                                                                   """,
                                                                                   style = {"color": light_color}),
                                                                      
                                                                      html.Br(),
                                                                      
                                                                      html.H4("INSTRUCTIONS:", style = {"fontWeight": "bold", "color": warning_color}),
                                                                      dcc.Markdown("""
                                                                                   Enter the starting and ending year of interest under the ___U.S Malpractice Cases Between___ header
                                                                                   located on the right-hand side of the dashboard to query data and summary statistics for the
                                                                                   specified study period. 
                                                                                   """,
                                                                                   style = {"color": light_color}),
                                                                    
                                                                      html.Br(),
                                                                      
                                                                      html.H4("DATA SOURCE:", style = {"fontWeight": "bold", "color": warning_color}),
                                                                      dcc.Markdown("""
                                                                                   The U.S Department of Health and Human Services's National Practitioner Data Bank (NPDB)
                                                                                   """,
                                                                                   style = {"color": light_color})
                                                                      
                                                                     ])
                                               ]),

                            dbc.Col(width = {"size": 3},
                                    children = [
                                            
                                                html.Div(children = [
                                                                 
                                                                     dash_table.DataTable(id = "tot_allsumm_tbl",
                                                                                          
                                                                                          columns = [{"name": " ", "id": "SUMMSTAT", "type": "text"},
                                                                                                     {"name": "ACROSS ALL U.S STATES", "id": "SUMMVAL", "type": "text"}],
                                                                                          
                                                                                          style_as_list_view = True,
                                                                                                                                                                                  
                                                                                          #style formatting for header
                                                                                          style_header = {"fontWeight": "bold",
                                                                                                          "font-size": "16px",
                                                                                                          "textAlign": "center",
                                                                                                          "height": "50px",
                                                                                                          "backgroundColor": dark_color,
                                                                                                          "color": "white"},
                                                                                                          
                                                                                                          
                                                                                          #style formatting for data cells
                                                                                          style_data = {"height": "40px"},
                                                                                          
                                                                                          #styling for cell data
                                                                                          style_cell = {"whiteSpace": "normal"},
                                                                                          
                                                                                          style_data_conditional = [{"if": {"row_index": "odd"}, "backgroundColor": "rgb(185, 184, 181)"},
                                                                                                                    {"if": {"row_index": "even"}, "backgroundColor": "rgb(255, 255, 255)"}],
                                                                                          
                                                                                          #conditional style formatting for cell data
                                                                                          style_cell_conditional = [{"if": {"column_id": "SUMMSTAT"}, "width": "150px", "textAlign": "left", "font-size": "14px", "fontWeight": "bold"},
                                                                                                                    {"if": {"column_id": "SUMMVAL"}, "textAlign": "center", "font-size": "20px"}],
                                                                                                                    
                                                                                                          
                                                                                        )
                                                                 
                                                                    ]),
                                                                     
                                                
                                                dcc.Graph(id = "algtyp_barchart"),
                                                
                                                dcc.Graph(id = "outc_barchart")
                                            
                                            
                                               ]),
                        
                            dbc.Col(width = {"size": 6},
                                    children = [
                                            
                                                #div container for row 2, column 1
                                                html.Div(children = [
                                                                 
                                                                    #choropleth map of malpractice claims across US
                                                                    dcc.Graph(id = "malp_geo_map"),
                                                
                                                                    #data table contain summary statistics on malpractice claims across US
                                                                    dash_table.DataTable(id = "malp_geo_tbl", 
                                                         
                                                                                         columns = [{"name": "Year", "id": "ORIGYEAR"},
                                                                                                    {"name": "State", "id": "WORKSTAT"}, 
                                                                                                    {"name": "# of Practitioners", "id": "PRACTNUM", "type": "numeric", "format": Format(nully = "None", group = Group.yes)}, 
                                                                                                    {"name": "# of Records", "id": "SEQNO", "type": "numeric", "format": Format(nully = "None", group = Group.yes)}, 
                                                                                                    {"name": "Median Payment", "id": "TOTALPMT", "type": "numeric", "format": Format(nully = "None", symbol = Symbol.yes, symbol_prefix = "$", group = Group.yes)}, 
                                                                                                    {"name": "Median Length", "id": "AALENGTH", "type": "numeric", "format": Format(nully = "None", group = Group.yes)}],
                                                                                         
                                                                                         #style formatting for table
                                                                                         style_table = {"height": "270px", "overflowY": "auto"},
                                                                                        
                                                                                         style_as_list_view = True,
                                                                                         
                                                                                         fixed_rows = {"headers": True}, #keeps header fixed when scrolling vertically through table
                                                                                         
                                                                                         sort_action = "native", #allow for sorting of columns in table
                                                                                         
                                                                                         sort_mode = "multi", #allow for sorting by multiple columns in table
                                                                                         
                                                                                         #style formatting for header
                                                                                         style_header = {"fontWeight": "bold", 
                                                                                                         "font-size": "12px", 
                                                                                                         "color": "white",
                                                                                                         "backgroundColor": dark_color},                                          
                                                                                         
                                                                                         #conditional formatting for headers
                                                                                         style_header_conditional = [{"if": {"column_id": "ORIGYEAR"}, "textAlign": "center"},
                                                                                                                     {"if": {"column_id": "WORKSTAT"}, "textAlign": "center"}],
                                                                                                                     
                                                                                         #conditional formatting for specific data cell                            
                                                                                         style_data_conditional = [{"if": {"column_id": "ORIGYEAR"}, "textAlign": "center", "width": "50px", "fontWeight": "bold"},
                                                                                                                   {"if": {"column_id": "WORKSTAT"}, "textAlign": "center", "width": "50px", "fontWeight": "bold"},
                                                                                                                   {"if": {"column_id": "PRACTNUM"}, "width": "100px"},
                                                                                                                   {"if": {"column_id": "SEQNO"}, "width": "100px"}, 
                                                                                                                   {"if": {"column_id": "TOTALPMT"}, "width": "100px"},
                                                                                                                   {"if": {"column_id": "AALENGTH"}, "width": "100px"},
                                                                                                                   {"if": {"row_index": "even"}, "backgroundColor": "rgb(255, 255, 255)"},
                                                                                                                   {"if": {"row_index": "odd"}, "backgroundColor": "rgb(185, 184, 181)"}],
                                                    
                                                                                         #tooltip for table headers
                                                                                         tooltip = {"ORIGYEAR": {"value": "Year that malpractice/adverse action case record was reported", "use_with": "header"},
                                                                                                    "WORKSTAT": {"value": "Practitioners' work state", "use_with": "header"},
                                                                                                    "PRACTNUM": {"value": "Total number of unique practitioners with an associated malpractice claim", "use_with": "header"},
                                                                                                    "SEQNO": {"value": "Total number of malpractice claims", "use_with": "header"},                                                       
                                                                                                    "TOTALPMT": {"value": "Median amount paid by malpractice insurer for practitioner's claim", "use_with": "header"},
                                                                                                    "AALENGTH": {"value": "Median length of adverse action penalty in years", "use_with": "header"}},
                                                                                                    
                                                                                        tooltip_delay = 0, #amount of delay before showing the tooltip description (measured in milliseconds)
                                                                                        tooltip_duration = 3000, #duration time for displaying the tooltip description (measured in milliseconds)
                                                                                        
                                                                                        #css style format for tooltip
                                                                                        css = [{"selector": ".dash-table-tooltip","rule": "font-size: 10px; background-color: " + light_color}]
                                                                                                 
                                                                                        )
                    
                                                                    ])
                                                ]), 
                                                
                                ]) 
        
                    ]) #end of app.layout


#******************************************************************************
#SECTION IV: DEFINE APP CALLBACKS
#******************************************************************************

#callback for malpractice summary table by US states
@app.callback(Output(component_id = "malp_geo_tbl", component_property = "data"),
              [Input(component_id = "malp_start_year", component_property = "value"),
               Input(component_id = "malp_end_year", component_property = "value")])
def filter_malp_geo_tbl(malp_start_yr, malp_end_yr):
    
    if (malp_start_yr is None) or (malp_end_yr is None):
        raise PreventUpdate
    else:
    
       #filter npdb dataset to records between the starting and ending year specified by user
       filter_malp_df = npdb_df[npdb_df["ORIGYEAR"].between(malp_start_yr, malp_end_yr)] 

       #summary statistics by year and practitioner's state location of work 
       malp_by_geo_df = filter_malp_df.groupby(["ORIGYEAR", "WORKSTAT"]).aggregate({"PRACTNUM": "nunique", #count of practitioners
                                                                                   "SEQNO": "nunique", #count of malpractice records
                                                                                   "TOTALPMT": "median", #median malpractice payment amount 
                                                                                   "AALENGTH": "median" #median adverse action length
                                                                                   }).reset_index()

       #round results to two decimal places
       malp_by_geo_df["TOTALPMT"] = round(malp_by_geo_df["TOTALPMT"], 2)
       malp_by_geo_df["AALENGTH"] = round(malp_by_geo_df["AALENGTH"], 2)

       return malp_by_geo_df.to_dict("records")
        

#callback for summary table across all US states
@app.callback(Output(component_id = "tot_allsumm_tbl", component_property = "data"),
              [Input(component_id = "malp_start_year", component_property = "value"),
               Input(component_id = "malp_end_year", component_property = "value")])
def calc_tot_allsumm_tbl(malp_start_yr, malp_end_yr):
    
    if (malp_start_yr is None) or (malp_end_yr is None):
        raise PreventUpdate
    else:
        
        #filter npdb dataset to records between the starting and ending year specified by user
        filter_malp_df = npdb_df[npdb_df["ORIGYEAR"].between(malp_start_yr, malp_end_yr)]
        
        #calculate the total number of malpractice records across the US
        tot_seqno_all = "{:,}".format(filter_malp_df["SEQNO"].nunique())
        tot_pract_all = "{:,}".format(filter_malp_df["PRACTNUM"].nunique())
        tot_pmt_all = "${:,}".format(int(filter_malp_df["TOTALPMT"].sum()))
        tot_aalen_all = "{:,}".format(filter_malp_df["AALENGTH"].median())

        #format summary statistics into dataframe
        tot_allsumm_df = pd.DataFrame({"SUMMSTAT": ["# OF MALPRACTICE CLAIMS:",
                                                    "# OF LIABLE PRACTITIONERS:", 
                                                    "TOTAL MALPRACTICE PAYMENT:",
                                                    "MEDIAN ADVERSE EVENT LENGTH:"],
                                       "SUMMVAL":  [tot_seqno_all,
                                                    tot_pract_all,
                                                    tot_pmt_all,
                                                    tot_aalen_all]})
        
        return tot_allsumm_df.to_dict("records")

#callback for allegation type bar chart
@app.callback(Output(component_id = "algtyp_barchart", component_property = "figure"),
              [Input(component_id = "malp_start_year", component_property = "value"),
               Input(component_id = "malp_end_year", component_property = "value")])
def plot_algtyp_barchart(malp_start_yr, malp_end_yr):
    
    if (malp_start_yr is None) or (malp_end_yr is None):
        raise PreventUpdate
    else:

        #mapping of allegation group raw values to abbreviated code values 
        algtyp_rwab_mapping = {1: "DR", 
                               10: "AR",
                               20: "SR",
                               30: "MR",
                               40: "IVB",
                               50: "OR",
                               60: "TR",
                               70: "MR",
                               80: "EPR",
                               90: "OM",
                               100: "BHR"}  
        
        #mapping of allegation group raw values to full description
        algtyp_rwds_mapping = {1: "Diagnosis Related", 
                               10: "Anesthesia Related",
                               20: "Surgery Related",
                               30: "Medication Related",
                               40: "IV & Blood Products Related",
                               50: "Obstetrics Related",
                               60: "Treatment Related",
                               70: "Monitoring Related",
                               80: "Equipment/Product Related",
                               90: "Other Miscellaneous",
                               100: "Behavioral Health Related"}

        #filter npdb dataset to records between the starting and ending year specified by user
        filter_malp_df = npdb_df[npdb_df["ORIGYEAR"].between(malp_start_yr, malp_end_yr)]
        
        #map allegation group code to abbreviate code description
        filter_malp_df["ALGNNATR_ABBR"] = filter_malp_df["ALGNNATR"].map(algtyp_rwab_mapping)
        #map allegation group code to description
        filter_malp_df["ALGNNATR_DESC"] = filter_malp_df["ALGNNATR"].map(algtyp_rwds_mapping)
        
        #calculate numbers for bar chart
        algtyp_df = filter_malp_df.groupby(["ALGNNATR_ABBR", "ALGNNATR_DESC"])["SEQNO"].nunique().reset_index()

        #plot bar chart
        algtyp_fig = px.bar(data_frame = algtyp_df, x = "ALGNNATR_ABBR", y = "SEQNO", color_discrete_sequence = ["rgb(87, 167, 113)"])
        algtyp_fig.update_layout(yaxis = {"title": "", "gridcolor": dark_color},
                                 xaxis = {"title": "", "showline": True, "linecolor": dark_color},
                                 title= {"text": "<b># OF MALPRACTICE CLAIMS BY ALLEGATION TYPE:</b>",
                                         "font": dict(size=10),
                                         "xanchor": "left"},
                                 font = {"size": 8},
                                 margin = dict(l=0, b=0),
                                 width = 480,
                                 height = 250,
                                 paper_bgcolor = tertiary_color,
                                 plot_bgcolor = tertiary_color,
                                 hoverlabel = {"bgcolor": "rgb(99, 198, 132)", "font": dict(size=8)})
        algtyp_fig.update_traces(customdata = np.stack((algtyp_df["ALGNNATR_DESC"], algtyp_df["SEQNO"]), axis = -1),
                                 hovertemplate = "<b>Allegation Type:</b> %{customdata[0]}<br>" + 
                                                 "<b># of Claims:</b> %{customdata[1]:,}")
        
        return algtyp_fig
    
#callback for outcome severity type bar chart
@app.callback(Output(component_id = "outc_barchart", component_property = "figure"),
              [Input(component_id = "malp_start_year", component_property = "value"),
               Input(component_id = "malp_end_year", component_property = "value")])
def plot_outc_bartchart(malp_start_yr, malp_end_yr):
    
    if (malp_start_yr is None) or (malp_end_yr is None):
        raise PreventUpdate
    else:
        
        #mapping of outcome raw value to abbreviate code
        outc_rwab_mapping = {1: "EM",
                             2: "INS",
                             3: "MIT",
                             4: "MAT",
                             5: "MIP",
                             6: "SP",
                             7: "MAP",
                             8: "QBL",
                             9: "DE",
                             10: "CBD"}
            
        #mapping of outcome raw value to full code description
        outc_rwds_mapping = {1: "Emotional",
                             2: "Insignificant",
                             3: "Minor Temporary",
                             4: "Major Temporary",
                             5: "Minor Permanent",
                             6: "Significant Permanent",
                             7: "Major Permanent",
                             8: "Quadriplegic/Brain Damage/Lifelong Care",
                             9: "Death",
                             10: "Cannot Be Determined"}
            
        #filter npdb dataset to records between the starting and ending year specified by user
        filter_malp_df = npdb_df[npdb_df["ORIGYEAR"].between(malp_start_yr, malp_end_yr)]
            
        #map outcome raw value to abbreviated code value
        filter_malp_df["OUTCOME_ABBR"] = filter_malp_df["OUTCOME"].map(outc_rwab_mapping)
        #map outcome raw value to full code description
        filter_malp_df["OUTCOME_DESC"] = filter_malp_df["OUTCOME"].map(outc_rwds_mapping)
   
        #calculate numbers for outcome bar chart
        outc_df = filter_malp_df.groupby(["OUTCOME_ABBR", "OUTCOME_DESC"])["SEQNO"].nunique().reset_index()

        #plot bar chart
        outc_fig = px.bar(data_frame = outc_df, x = "OUTCOME_ABBR", y = "SEQNO", color_discrete_sequence = ["rgb(160, 56, 43)"])
        outc_fig.update_layout(yaxis = {"title": "", "gridcolor": dark_color},
                               xaxis = {"title": "", "showline": True, "linecolor": dark_color},
                               title = {"text": "<b># OF MALPRACTICE CLAIMS BY SEVERITY OF INJURY:</b>",
                                        "font": dict(size = 10),
                                        "xanchor": "left"},
                               font = {"size": 8},
                               margin = dict(l=0, b=0),
                               width = 480,
                               height = 250,
                               paper_bgcolor = tertiary_color,
                               plot_bgcolor = tertiary_color,
                               hoverlabel = {"bgcolor": "rgb(223, 98, 83)", "font": dict(size=8)})
        
        outc_fig.update_traces(customdata = np.stack((outc_df["OUTCOME_DESC"], outc_df["SEQNO"]), axis = -1),
                               hovertemplate = "<b>Outcome Type:</b> %{customdata[0]}<br>" + 
                                               "<b># of Claims:</b> %{customdata[1]:,}")
        
        return outc_fig


#callback for malpractice choropleth map by US states
@app.callback(Output(component_id = "malp_geo_map", component_property = "figure"),
              [Input(component_id = "malp_start_year", component_property = "value"),
               Input(component_id = "malp_end_year", component_property = "value")])
def plot_malp_choropleth(malp_start_yr, malp_end_yr):
    
    if (malp_start_yr is None) or (malp_end_yr is None):
        raise PreventUpdate
    else:
        #
        #filter npdb dataset to records between the starting and ending year specified by user
        filter_malp_df = npdb_df[npdb_df["ORIGYEAR"].between(malp_start_yr, malp_end_yr)] 

        #summary statistics by year and practitioner's state location of work 
        malp_by_geo_df = filter_malp_df.groupby(["WORKSTAT"]).aggregate({"PRACTNUM": "nunique", #count of practitioners
                                                                         "SEQNO": "nunique", #count of malpractice records
                                                                         "TOTALPMT": "median", #median malpractice payment amount 
                                                                         "AALENGTH": "median" #median adverse action length
                                                                                    }).reset_index()

        #plot choropleth of malpractice cases by US state
        malp_chorodata = [go.Choropleth(locationmode = "USA-states",
                             locations = malp_by_geo_df["WORKSTAT"],
                             z = malp_by_geo_df["SEQNO"],
                             colorscale = "Redor",
                             colorbar = dict(title = dict(text = "<b># of Records</b>", side = "right"),
                                             x = 0.95,
                                             separatethousands = True,
                                             showticklabels = True,
                                             thickness = 10,
                                             tickfont = dict(size = 8))
                                       )]
                                                                         
        malp_chorolayout = go.Layout(geo = dict(bgcolor = tertiary_color,
                                                lakecolor = tertiary_color,
                                                landcolor = tertiary_color),
                                     geo_scope = "usa",
                                     paper_bgcolor = tertiary_color,
                                     plot_bgcolor = tertiary_color,
                                     margin = dict(l=10, r=10, b=10, t=10),
                                     hoverlabel = {"font": {"size": 10}} #set the font size for text in hoverlabel )          
                                     )
        
        malp_chorofig = go.Figure(data = malp_chorodata, layout = malp_chorolayout)
        
        malp_chorofig.update_traces(customdata = np.stack((malp_by_geo_df["WORKSTAT"],\
                                                           malp_by_geo_df["PRACTNUM"].fillna("None"),\
                                                           malp_by_geo_df["SEQNO"].fillna("None"),\
                                                           malp_by_geo_df["TOTALPMT"].fillna("None"),\
                                                           malp_by_geo_df["AALENGTH"].fillna("None")), axis = -1),
                                    hovertemplate = "<b>%{customdata[0]}</b><br>" +
                                                    "# of Practitioners: %{customdata[1]: ,}<br>" +
                                                    "# of Records: %{customdata[2]: ,}<br>" +
                                                    "Median Payment: $%{customdata[3]: ,}<br>" +
                                                    "Median Length: %{customdata[4]: ,}" +
                                                    "<extra></extra>",
                                    marker_line_width = 0 #removes border bolding from states in choropleth map
                                    )

        return malp_chorofig


       
if __name__ == '__main__':
    app.run_server(debug = False)
