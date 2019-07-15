from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label, HoverTool, CrosshairTool, CategoricalColorMapper, Slider, Select, Plot, LinearAxis, Grid, Arrow, OpenHead, NormalHead, VeeHead
from bokeh.models.widgets import Tabs, Panel, Dropdown, TextInput, Div, DataTable, DateFormatter, TableColumn
from bokeh.models.glyphs import Text
from bokeh.layouts import row, column, widgetbox
from bokeh.io import output_file, show, curdoc
import pandas as pd
import numpy as np

#import os
#os.chdir('C:/Users/z3160256/OneDrive - UNSW/R Data Camp')


### 1. CREATE THE DATASET

# convert iris into a ColumnDataSource >> here I am explicitly assigning the columns from the original data frame
# To Column Data Source columns (as a dictionary)

survivalcurve = pd.read_csv("average_function.csv")
survivalcurve['Survival'] = np.round((1 - survivalcurve['Survival']),3)*100

surv = pd.read_csv("final_survival_functions_latest.csv")
surv = surv.set_index("patient_id")
idx = pd.IndexSlice

survival_source = ColumnDataSource(data={
    'Time'       : survivalcurve.loc[:,'Time'],
    'Survival'       : survivalcurve.loc[:,'Survival']
}) 

patient_source = ColumnDataSource(data={
    'Time'       : surv.columns[29:].values,
    'Survival'       : surv.loc['eCQQYNA7a8U'][29:]
}) 


surv.loc['eCQQYNA7a8U'][29:]

# Save the minimum and maximum values of the time column - should be from 0 to 480
xmin, xmax = min(survivalcurve['Time']), max(survivalcurve['Time'])

# Save the minimum and maximum values of the Y axis - probability of sepsis
ymin, ymax = 0, 100

# 2. Create the figure: plot >> note we added extra commands includimg the range of our X and Y axes, which are the min and max of out X and Y axis variables fertility and life_expectancy

survival_plot = figure(tools=['box_select',
                         'lasso_select',
                          'crosshair'],  
                  x_axis_label="Time (hours)",
                  y_axis_label="Probability of sepsis (%)",
                  x_range = (xmin, xmax),
                  y_range = (ymin, ymax),
                  plot_width = 900,
                  plot_height = 500)

survival_plot.title.text = "Probability of Sepsis over Time"
survival_plot.title.text_color = "DarkSlateGray"
survival_plot.title.text_font = "arial"
survival_plot.title.text_font_style = "bold"
survival_plot.title.text_font_size = "20pt"
survival_plot.title.align = "center"

survival_plot.xaxis.axis_label_text_font_size = "15pt"
survival_plot.xaxis.axis_label_text_font = "arial"
survival_plot.xaxis.axis_label_text_font_style = "normal"
survival_plot.yaxis.axis_label_text_font_size = "15pt"
survival_plot.yaxis.axis_label_text_font = "arial"
survival_plot.yaxis.axis_label_text_font_style = "normal"


# Plot the graph (scatter plot)

ss1 = survival_plot.line(x = 'Time', 
                y = 'Survival', 
                source=survival_source,             
                line_dash="6 2", line_width=3, color='GoldenRod'
                )


#ss2 = survival_plot.circle(x = 'Time', 
#                y = 'Survival',
#                source=survival_source,
#                size=20,
#                fill_color="grey", hover_fill_color="purple",
#                fill_alpha=0.05, hover_alpha=0.4,
#                line_color=None, hover_line_color="white")

survival_plot.add_tools(HoverTool(renderers=[ss1], tooltips=[('probability','@Survival'+"%"),('time (h)','@Time')], mode='vline'),
                       CrosshairTool(line_color='grey'))


survival_plot.ygrid.minor_grid_line_color = 'SlateGrey'
survival_plot.ygrid.minor_grid_line_alpha = 0.05



### ADD A SECOND TABBED PLOT FOR INDIVIDUAL PATIENTS

patient_plot = figure(tools=['box_select',
                         'lasso_select',
                          'crosshair'],  
                  x_axis_label="Time (hours)",
                  y_axis_label="Probability of sepsis (%)",
                  x_range = (xmin, xmax),
                  y_range = (ymin, ymax),
                  plot_width = 900,
                  plot_height = 500)

patient_plot.title.text = "Probability of Sepsis over Time"
patient_plot.title.text_color = "DarkSlateGray"
patient_plot.title.text_font = "arial"
patient_plot.title.text_font_style = "bold"
patient_plot.title.text_font_size = "20pt"
patient_plot.title.align = "center"

patient_plot.xaxis.axis_label_text_font_size = "15pt"
patient_plot.xaxis.axis_label_text_font = "arial"
patient_plot.xaxis.axis_label_text_font_style = "normal"
patient_plot.yaxis.axis_label_text_font_size = "15pt"
patient_plot.yaxis.axis_label_text_font = "arial"
patient_plot.yaxis.axis_label_text_font_style = "normal"

pp1 = patient_plot.line(x = 'Time', 
                y = 'Survival', 
                source=patient_source,             
                line_dash="6 2", line_width=2, color='MediumSeaGreen'
                )

pp2 = patient_plot.line(x = surv.columns[25:].values, 
                y = 50, line_width=1, color='Red')

pp3 = patient_plot.add_layout(Arrow(end=NormalHead(fill_color="orange", line_color="Red"), line_color="Red", line_width=4,
                   x_start=50, y_start=30, x_end=100, y_end=50))

patient_plot.add_tools(HoverTool(renderers=[pp1], tooltips=[('probability','@Survival'+"%"),('time (h)',  '@Time')], mode='vline'),
                       CrosshairTool(line_color='grey'))



# add a textbox where the arrow is

citation = Label(x=60, y=95, x_units='screen', y_units='screen',
                 text="Danger zone: Take note when patient's curve crosses this line", render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0, text_font_size="10pt")
patient_plot.add_layout(citation)

#show(survival_plot)

patient_plot.ygrid.minor_grid_line_color = 'SlateGrey'
patient_plot.ygrid.minor_grid_line_alpha = 0.05



def update_plot(attr, old, new):
    age_range = ageslider.value
    charlson_value = charlsonslider.value
    resp_value = respslider.value
    hr_value = hrslider.value
    map_value = mapslider.value
    spo2_value = spo2slider.value
    bmi_value = bmislider.value
    if gendermenu.value=='Male': 
        filt = (surv['gender'] == "Male") 
    elif gendermenu.value=='Female': 
        filt = (surv['gender'] == "Female")
    else: 
        filt = (surv['gender'].isin(["Male","Female"]))
    new_data = {
        'Time': surv.columns[25:].values,
        'Survival':surv[(surv['age']>=age_range) & (surv['bmi']<=bmi_value) & (surv['spo2_mean']>=spo2_value) & (surv['charlson_index']>=charlson_value) & (surv['map_mean']>=map_value) & (surv['heart_rate_mean']>=hr_value) & (surv['respiratory_rate_shift']>=resp_value) & (filt)][surv.columns[25:]].mean()
    }
    survival_source.data = new_data
    
# Make a slider object: slider
ageslider = Slider(start=20,end=90,step=5,value=40,title='Age')
ageslider.on_change('value', update_plot)

charlsonslider = Slider(start=0,end=8,step=1,value=0,title='Charlson Index Score (number of comorbid conditions)')
charlsonslider.on_change('value', update_plot)

respslider = Slider(start=-20,end=20,step=0.5,value=15,title='How much breathing rate (breaths per min) has changed in the previous 6h')
respslider.on_change('value', update_plot)

hrslider = Slider(start=20,end=120,step=0.5,value=15,title='Average heart rate in the previous 6h (beats per min)')
hrslider.on_change('value', update_plot)

mapslider = Slider(start=26,end=165,step=0.5,value=80,title='Average mean arterial blood pressure in the previous 6h (beats per min)')
mapslider.on_change('value', update_plot)

spo2slider = Slider(start=1,end=100,step=0.5,value=80,title='Average peripheral capillary oxygen saturation in the previous 6h (%)')
spo2slider.on_change('value', update_plot)

bmislider = Slider(start=18,end=45,step=0.5,value=25,title='BMI')
bmislider.on_change('value', update_plot)

gendermenu = Select(options=['Male','Female','all'],
             value='Male', title='Gender')
gendermenu.on_change('value', update_plot)

divbox = Div(text="""Below, enter details of the patient to view an estimate of how likely they will get sepsis in the coming hours""",
width=400, height=50)


# Create a layout that combines the menu, the slider, and the irisplot
layout_new=row(survival_plot,widgetbox(divbox, gendermenu, ageslider, bmislider, charlsonslider, respslider, 
                                       hrslider, mapslider, spo2slider))



### Now customise the individual patient section

n_ids = len(surv)
patient_ids = list(surv.index)

def update_patient_plot(attr, old, new):
    updated_data = {
        'Time': surv.columns[25:].values,
        'Survival':surv.loc[patientselectmenu.value][25:]
    }
    patient_source.data = updated_data
    
    
keycols = ['gender','age','bmi','charlson_index','respiratory_rate_shift','heart_rate_mean','map_mean','spo2_mean'] 

    
def update_patient_table(attr, old, new):
    updated_data = {
        'feature':features,  
        'value':[np.round(i,2) if isinstance(i, np.float64) else i for i in list(surv.loc[patientselectmenu.value,keycols])]
    }
    patienttablesource.data = updated_data

#[np.round(i,2) if type(i) == float else i for i in list(surv.loc[patientselectmenu.value,keycols])]


patientselectmenu = Select(title="Choose Patient (by ID):", value=patient_ids[0], options=patient_ids)
patientselectmenu.on_change('value', update_patient_plot, update_patient_table)


# Add data table to summarize each patient

features = ['Sex','Age','BMI','Charlson CCI score',
            'Breathing rate change (cf. 6h ago)',
            '6hr avg heart rate over (bpm)',
            '6hr avg mean arterial blood pressure',
            '6hr avg peripheral capillary O2 saturation','']

keycols = ['gender','age','bmi','charlson_index','respiratory_rate_shift','heart_rate_mean','map_mean','spo2_mean']

#patient_data_source = ColumnDataSource(data={
#    'Feature of patient': features,
#    'Current value'       : surv.loc['eCQQYNA7a8U',keycols]
#}) 

#columns = [
#        TableColumn(field="dates", title="Date", formatter=DateFormatter()),
#        TableColumn(field="downloads", title="Downloads"),
#    ]
#data_table = DataTable(source=patient_data_source, width=400, height=280)


patienttabledata = dict(
        feature = features,
        value=[np.round(i,2) if isinstance(i, np.float64) else i for i in list(surv.loc['eCQQYNA7a8U',keycols])],
    )


patienttablesource = ColumnDataSource(patienttabledata)

columns = [
        TableColumn(field="feature", title="Feature"),
        TableColumn(field="value", title="Value"),
    ]

patient_data_table = DataTable(source=patienttablesource, columns=columns, width=400, height=280, index_position=None)


# Patient layout
layout_patient=row(patient_plot,widgetbox(patientselectmenu, patient_data_table))


## ADD TABBED LAYOUT
first_tab=Panel(child=layout_new, title='Sepsis probability based on vital signs') # title is the NAME of each tab
second_tab=Panel(child=layout_patient, title='Sepsis probability of individual patients')
tabs = Tabs(tabs=[first_tab,second_tab]) 

show(tabs)


curdoc().add_root(tabs)
