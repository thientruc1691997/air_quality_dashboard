import plotly.express as px
import pandas as pd
import numpy as np
from dash import html


def create_pollutant_barchart(df):
    desired_pollutants = ['BEN', 'CO', 'EBE', 'NMHC', 'NO_2', 'O_3', 'PM10', 'SO_2', 'TCH', 'TOL', 'CH4', 'NO', 'NOx', 'PM25']
    
    pollutant_descriptions = {
        "SO_2": "High levels of sulphur dioxide can produce irritation in the skin and <br>membranes, and worsen asthma or heart diseases in sensitive groups.",
        "CO": "Carbon monoxide poisoning involves headaches, dizziness and confusion in <br>short exposures can result in loss of consciousness, arrhythmias, seizures or even death in the long term.",
        "NO": "This is a highly corrosive gas generated among others by motor vehicles and fuel burning processes.",
        "NO_2": "Long-term exposure is a cause of chronic lung diseases, and are harmful for the vegetation.",
        "PM25": "The size of these particles allow them to penetrate into <br>the gas exchange<br> regions of the lungs (alveolus) and even enter the arteries.<br> Long-term exposure is proven to be related to low birth weight and high blood pressure in newborn babies.",
        "PM10": "Even though they cannot penetrate the alveolus, they can <br>still penetrate through the lungs and affect other organs. Long term exposure<br> can result in lung cancer and cardiovascular complications.",
        "PM10": "Even though they cannot penetrate the alveolus, they can <br> still penetrate through the lungs and affect other organs. Long term exposure<br> can result in lung cancer and cardiovascular complications.",
        "NOx": "Affect the human respiratory system worsening asthma or other diseases,<br> and are responsible for the yellowish-brown color of photochemical smog.",
        "O_3": "High levels can produce asthma, bronchitis or other chronic pulmonary<br> diseases in sensitive groups or outdoor workers.",
        "TOL": "Long-term exposure to this substance (present in tobacco smoke as well)<br> can result in kidney complications or permanent brain damage.",
        "BEN": "Benzene is a eye and skin irritant, and long exposures may result in <br>several types of cancer, leukaemia and anaemias. Benzene is considered a group<br> 1 carcinogenic to humans by the IARC.",
        "EBE": "Long term exposure can cause hearing or kidney problems and the IARC<br> has concluded that long-term exposure can produce cancer.",
        "TCH": "This group of substances can be responsible for different blood, <br>immune system, liver, spleen, kidneys or lung diseases.",
        "CH4": "This gas is an asphyxiant, which displaces the oxygen animals<br>need to breathe. Displaced oxygen can result in dizziness, weakness, nausea<br> and loss of coordination.",
        "NMHC": "Long exposure to some of these substances can result in damage<br> to the liver, kidney, and central nervous system. Some of them are suspected to cause cancer in humans."
}


    # Filter data for 2017 and 2018
    df_2018 = df[df['year'] == 2018]
    df_2017 = df[df['year'] == 2017]
    
    # Convert units for specific pollutants (mg/m3 to μg/m3)
    convert_cols = ['CO', 'CH4', 'NMHC', 'TCH']
    for col in convert_cols:
        if col in df_2018.columns:
            df_2018[col] = df_2018[col] * 1000
        if col in df_2017.columns:
            df_2017[col] = df_2017[col] * 1000
    
    # Calculate averages and filter out NaN values
    avg_2018 = df_2018[desired_pollutants].mean().reset_index()
    avg_2018.columns = ['pollutant', 'value_2018']
    avg_2017 = df_2017[desired_pollutants].mean().reset_index()
    avg_2017.columns = ['pollutant', 'value_2017']
    
    # Merge and calculate metrics
    merged = pd.merge(avg_2018, avg_2017, on='pollutant').dropna()
    merged['change_pct'] = ((merged['value_2018'] - merged['value_2017']) / merged['value_2017'] * 100).round(1)
    merged['log_value'] = np.log1p(merged['value_2018']).round(2)
    merged['actual_value'] = merged['value_2018'].round(2)
    
    # Sort by log value for consistent ordering
    merged = merged.sort_values('log_value')
    
    # Tạo hover text với định dạng HTML
    merged['hover_text'] = merged.apply(
        lambda row: (
            f"<b>{row['pollutant']}</b><br>"
            f"Log Value: {row['log_value']}<br>"
            f"Actual Concentration: {row['actual_value']} μg/m³<br>"
            f"% Change: <span style='color:{'green' if row['change_pct'] < 0 else 'red'}'>{row['change_pct']}%</span><br>"
            f"<span style='"
            f"display: inline-block;"  # Enable width control
            f"width: 5px;"  # Fixed width
            f"max-height: 5px;"
            f"word-wrap: break-word;"
            f"white-space: normal;"  # Enable wrapping
            f"font-size: 12px;"
            f"'>"
            f"❓ {pollutant_descriptions.get(row['pollutant'], 'No description available')}"
            f"</span>"
        ),
        axis=1
    )

    
    # Create figure with custom hover
    fig = px.bar(
        merged,
        x='log_value',
        y='pollutant',
        orientation='h',
        labels={'log_value': 'log(1 + Concentration)', 'pollutant': ''},
        height=500,
        hover_name= 'hover_text',  # Use our custom hover text
        hover_data={'hover_text': False, 'log_value': False, 'actual_value': False},
        custom_data=['hover_text'] # Hide from hover box
    )
    first_pollutant = merged['pollutant'].iloc[13]
    
    # Add table annotations 
    annotations = []
    annotations.append(dict(
        x=1.1,
        y=first_pollutant,
        yshift=25,
        xref='paper',
        yref='y',
        text="<b>% 2017</b>",
        showarrow=False,
        font=dict(size=12),
        align='right'
    ))
        
     # Các giá trị % Change - TÔ XANH nếu giảm mạnh (càng âm càng tốt)
    for _, row in merged.iterrows():
        if row['change_pct'] < -25:  # Giảm >25% => Tốt, tô xanh đậm
            text = f"<span style='color:Cerulean; font-weight:bold'>↓ {row['change_pct']}%</span>"
        elif row['change_pct'] < 0:  # Giảm nhẹ (<25%) => Tô xanh nhạt
            text = f"<span style='color:sky'>{row['change_pct']}%</span>"
        else:  # Tăng (giá trị dương) => Tô đỏ
            text = f"<span style='color:red'>{row['change_pct']}%</span>"
    
        annotations.append(dict(
            x=1.1,
            y=row['pollutant'],
            xref='paper',
            yref='y',
            text=text,
            showarrow=False,
            font=dict(size=11, family="Tahoma"),
            align='left'
        ))
    
    # Update layout with hover settings
    fig.update_layout(
        annotations=annotations,
        margin=dict(l=50, r=170, t=40, b=40),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1034A6', family='Tahoma'),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        yaxis=dict(
            showgrid=False,  # Add this to remove y-axis grid lines
            showline=True,  # Keep y-axis line visible
            linecolor='#1034A6',  # Set y-axis line color
            tickfont=dict(size=12,color='#1034A6'),
            tickmode='array',
            tickvals=list(range(len(merged)))
        ),
        xaxis=dict(
            showgrid=False,  # Add this to remove x-axis grid lines
            showline=True,  # Keep x-axis line visible
            linecolor='#1034A6',  # Set x-axis line color
            range=[0, merged['log_value'].max()]
        )
    )
    
    # Customize hover template
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='#1034A6'),
            opacity=0.3,
            color='#1034A6'  # White bars
        ),
        hovertemplate="%{customdata[0]}",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            namelength=-1  # Ngăn cắt ngắn text
        )
    )

    return fig

def create_main_map(df, stations_df):
    # Merge with station data to get coordinates
    merged_df = pd.merge(
        df[['station']].drop_duplicates(),  # Just get unique station IDs
        stations_df,
        left_on='station',
        right_on='id'
    )
    
    # Create basic map with station locations
    fig = px.scatter_mapbox(
        merged_df,
        lat='lat',
        lon='lon',
        hover_name='name',  # Show station name on hover
        hover_data={'lat': False, 'lon': False},  # Hide lat/lon from hover
        size_max=15,
        zoom=10,
        mapbox_style='carto-positron'
    )

    # Customize marker appearance
    fig.update_traces(
        marker=dict(
            size=10,  
            opacity=0.8
        ),
        hovertemplate="<b>%{hovertext}</b><extra></extra>"  
    )
    
    # Adjust map layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',
        margin={"r":10,"t":20,"l":10,"b":20},
        hoverlabel=dict(
            bgcolor="rgba(255, 255, 255, 0.9)",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig