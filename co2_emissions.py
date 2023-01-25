import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly.graph_objects as go

@st.cache
def get_co2_data():
    co2_data = pd.read_csv("https://github.com/owid/co2-data/raw/master/owid-co2-data.csv")
    # Slicing the data from 1950 and onwards
    co2_data = co2_data[co2_data['year']>=1950]
    # Converting CO2 column to exact numbers
    co2_data['co2'] = co2_data['co2'].apply(lambda x: x*1000000)
    return co2_data

@st.cache
def get_temperature_data():
    temperature = pd.read_csv("https://raw.githubusercontent.com/Raf888-sr/climate-change/main/land%20and%20ocean%20temp.csv")
    temperature.drop(temperature.iloc[:4].index,inplace=True)
    temperature = temperature.reset_index(drop=True)
    temperature.rename(columns={"Global Land and Ocean Temperature Anomalies":"Year"," January-December":"Temperature"},inplace=True)
    temperature['Temperature'] = pd.to_numeric(temperature['Temperature'])
    temperature['Year'] = pd.to_numeric(temperature['Year'])
    return temperature

# Loading Data
co2_data = get_co2_data()
temperature = get_temperature_data()

min_year = co2_data['year'].min()
max_year = co2_data['year'].max()


st.title("Climate Change")

# Sidebar Widgets
st.sidebar.image("https://gbsn.org/wp-content/uploads/2020/07/AUB-logo.png")
st.sidebar.title("Navigation")

# Sidebar for range of years available
selected_range = st.sidebar.slider("Years",min_value=min_year,max_value=max_year,
value=[min_year,max_year])

# List of Countries and Regions
sorted_countries = sorted(co2_data['country'].unique())
selected_country = st.sidebar.multiselect('Select country or group',sorted_countries,default=['United States','Europe','China','Russia','India'])

st.sidebar.markdown("Sources:")
st.sidebar.markdown("""
    >* [OWID](https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions)
    >* [NOAA](https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature)""")
st.sidebar.markdown("Useful Links:")
st.sidebar.markdown("""
                    >* [GatesNotes](https://www.gatesnotes.com/Climate-and-energy)
                    >* [What Can You do To Stop Climate Change? And Should You?](https://sites.google.com/view/sources-climate-how/)""")
st.sidebar.markdown("Done By: Rafic Srouji")





co2_year_selected = co2_data[(co2_data['year']>=selected_range[0]) & (co2_data['year']<=selected_range[1])]

trace1 = go.Scatter(x=temperature['Year'][:2],
                y=temperature['Temperature'][:2],
                mode='lines',
                line=dict(width=3,color="#d20931"))
frames = [dict(data= [dict(type='scatter',
                           x=temperature['Year'][:k+1],
                           y=temperature['Temperature'][:k+1]),
                     ],
               traces= [0],
              )for k  in  range(1, len(temperature)-1)]

layout = go.Layout(width=1200,
                   height=800,
                   showlegend=False,
                   hovermode='x unified',
                   updatemenus=[
                        dict(
                            type='buttons', showactive=False,
                            pad=dict(t=0, r=10),
                            buttons=[dict(label='Play',
                            method='animate',
                            args=[None,
                                  dict(frame=dict(duration=45,
                                                  redraw=False),
                                                  transition=dict(duration=0),
                                                  fromcurrent=True,
                                                  mode='immediate')]
                            )]
                        )])
layout.update(xaxis =dict(range=['1850', '2030'], autorange=False,title="year"),
              yaxis =dict(range=[temperature['Temperature'].min()-0.5, temperature['Temperature'].max()+0.5], autorange=False,title="Global Temperature Change in (C)"),
             title="Global Average Temperature Change<br><sup>Global average land-sea temperature anomaly relative to the 20th century average temperature.</sup>");
fig = go.Figure(data=[trace1], frames=frames, layout=layout)
fig.add_hline(y=0, line_width=3, line_color="violet",opacity=0.5)
fig.update_layout(template='simple_white',font_size=15)
st.plotly_chart(fig,use_container_width=True)




st.write("""
Carbon dioxide and other greenhouse gases emitted by humans are a major contributor to climate change and one of the world's most important problems.
Throughout Earth's history, there has always been a relationship between global temperatures and greenhouse gas concentrations, particularly CO2.
""")
st.write("""The chart represents the average temperature relative to the 20th century average (1901-2000).
We see that over the last few decades, global temperatures have risen sharply — to approximately 0.99℃  in 2016 higher than 20th century temperature average.""")
st.markdown("---------------")




# Interactive Map Showing CO2 emissions per capita from 1950 to 2020
st.markdown("""
#### Global CO2 Emissions Per Capita
""")
st.write("The graph below shows the CO2 emmissions per capita for the entire world. Select the range of years with the slider from sidebar to reveal the change between the two selected years.")

co2_year_selected = co2_data[(co2_data['year']>=selected_range[0]) & (co2_data['year']<=selected_range[1])]

fig = px.choropleth(co2_year_selected,
                    locations="iso_code",
                    color="co2_per_capita",
                    hover_name="country",
                    animation_frame="year",
                    projection="equirectangular",
                    range_color=(0,25),
                    color_continuous_scale = px.colors.sequential.Reds)
fig.update_layout(
        margin=dict(l=1,r=1,t=1,b=1),
        template = 'simple_white')

st.plotly_chart(fig,use_container_width=True)
st.markdown("---------------")


# Interactive Animated Bar Plot Showing Variation of CO2 emissions from 1950 to 2020

st.markdown("""
### Total CO2 emissions For Each Country
""")
st.write("Select the range of years with the slider from sidebar and countries from the drop down menu to observe the variation in CO2 emissions each year for every country selected.")

co2_selected = co2_data[(co2_data['year']>=selected_range[0]) & (co2_data['year']<=selected_range[1]) & (co2_data['country'].isin(selected_country))]
fig2 = px.bar(co2_selected,x="country",y="co2",color="country",animation_frame="year",animation_group="country",
             range_y=[0,co2_selected['co2'].max()],
             labels = dict(co2="CO2 emission in (tonnes)"))

fig2.update_layout(template = 'simple_white',font_size=15,width=1500,height=600)
st.plotly_chart(fig2,use_container_width=True)
st.markdown("---------------")


# Interactive Line Plot for Top Countries With Most CO2 emissions from 1950 to 2020
st.markdown("""
### Annual CO2 emmissions Per country
""")

st.write("""To stabilize (or even reduce) concentrations of CO2 in the atmosphere, the world needs to reach net-zero emissions. This requires large and fast reductions in emissions.

Are we making progress towards this? How far are we from this target?

At a time when global emissions need to be falling, they are in fact still rising, as the chart here shows. China is the world's biggest CO2 emissions surpassing most
developed countries such as United States and whole of Europe.""")

df = co2_year_selected[co2_year_selected['country'].isin(selected_country)]


pv = df.pivot_table(index="country",columns="year",values="co2",aggfunc='sum').reset_index()

x_axis = list(range(pv.shape[1]))
y_axis = list(pv.iloc[0,1:])

initial_data =[]
num_cols = pv.shape[1] - 1
for i in range(len(pv)):
    y_axis = np.array(pv.iloc[i,1])
    initial_data.append(go.Scatter(x = np.array([selected_range[0]]),y = y_axis, mode = "lines", name = pv['country'][i]))


# frames
frames = []

for f in range(selected_range[0],selected_range[1]):
    x_axis = np.arange(selected_range[0],f+1)
    curr_data =[]
    for j in range(len(pv)):
        current_country = pv['country'][j]
        y_axis = np.array(pv.iloc[j,1:(f%selected_range[0])+1])
        curr_data.append(go.Scatter(x = x_axis,
                                    y = y_axis,
                                    mode = 'lines',
                                    name = current_country))
        current_frame = go.Frame(data = curr_data)
        frames.append(current_frame)

layout = go.Layout(width=800,
                   height=800,
                   showlegend=True,
                   hovermode='x unified',
                   updatemenus=[
                        dict(
                            type='buttons', showactive=False,
                            pad=dict(t=0, r=10),
                            buttons=[dict(label='Play',
                            method='animate',
                            args=[None,
                                  dict(frame=dict(duration=0,
                                                  redraw=False),
                                                  transition=dict(duration=0),
                                                  fromcurrent=True,
                                                  mode='immediate')]
                            ),dict(label="Pause",
                                   method = "animate",
                                   args=[[None],
                                         dict(frame=dict(duration=0,
                                                         redraw=False),
                                                         transition=dict(duration=0),
                                                         mode='immediate')])]
                        )])
layout.update(xaxis =dict(range=[selected_range[0],selected_range[1]+10], autorange=False,title="year"),
              yaxis =dict(range=[0,co2_selected['co2'].max()], autorange=False,title="CO2 emissions in tonnes"),
             title="Annual CO2 emissions from fossil fuels");
fig3 = go.Figure(data=initial_data, frames=frames, layout=layout)
fig3.update_layout(template='plotly_white',font = dict(size=15))
st.plotly_chart(fig3)

st.markdown("----")
# YouTube Video
st.markdown("""
### Can You Fix Climate Change?""")
st.video("https://youtu.be/yiw6_JakZFc")
st.markdown("---------")
