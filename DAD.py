import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Data Analytics Dashboard"),
    html.P("Upload a CSV file to analyze and visualize the data."),

    # File Upload Component
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV'),
        multiple=False
    ),

    # Data Preview
    html.Div(id='data-preview'),

    # Basic Data Information
    html.Div(id='data-info'),

    # Data Visualization
    html.Div([
        html.Div([
            html.H4("Correlation Heatmap"),
            dcc.Graph(id='correlation-heatmap')
        ], className='six columns'),
        html.Div([
            html.H4("Distribution of Numeric Features"),
            dcc.Graph(id='numeric-feature-distribution'),
            dcc.Dropdown(id='feature-dropdown', multi=False)
        ], className='six columns')
    ], className='row'),

    # Filter Data Section
    html.Div([
        html.H4("Filter Data"),
        dcc.Dropdown(id='filter-column', multi=False),
        dcc.Dropdown(id='filter-value', multi=False),
        html.Div(id='filtered-data')
    ])
])


# Callback to handle file upload and data preview
@app.callback(
    [Output('data-preview', 'children'),
     Output('data-info', 'children'),
     Output('filter-column', 'options'),
     Output('feature-dropdown', 'options')],
    [Input('upload-data', 'contents')]
)
def upload_file(contents):
    if contents is None:
        return [], [], [], []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Data preview
    preview = html.Div([
        html.H5("Data Preview"),
        html.Table([html.Tr([html.Th(col) for col in df.columns])] +
                   [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), 10))])
    ])

    # Data info
    data_info = html.Div([
        html.H5("Dataset Information"),
        html.Pre(df.describe().to_string())
    ])

    # Filter columns options
    filter_columns = [{'label': col, 'value': col} for col in df.columns]

    # Numeric feature dropdown options for distribution
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    feature_dropdown_options = [{'label': col, 'value': col} for col in numeric_cols]

    return preview, data_info, filter_columns, feature_dropdown_options


# Callback for plotting correlation heatmap
@app.callback(
    Output('correlation-heatmap', 'figure'),
    [Input('upload-data', 'contents')]
)
def update_heatmap(contents):
    if contents is None:
        return {}

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Correlation heatmap
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        return {
            'data': [{
                'x': corr.columns,
                'y': corr.index,
                'z': corr.values,
                'type': 'heatmap'
            }],
            'layout': {
                'title': 'Correlation Heatmap',
                'xaxis': {'title': 'Features'},
                'yaxis': {'title': 'Features'}
            }
        }
    return {}


# Callback for plotting numeric feature distribution
@app.callback(
    Output('numeric-feature-distribution', 'figure'),
    [Input('upload-data', 'contents'),
     Input('feature-dropdown', 'value')]
)
def update_distribution(contents, selected_column):
    if contents is None or selected_column is None:
        return {}

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    
    fig = plt.figure(figsize=(6, 4))
    sns.histplot(df[selected_column], bins=30, kde=True)
    return {
        'data': [{
            'x': df[selected_column],
            'type': 'histogram'
        }],
        'layout': {
            'title': f'Distribution of {selected_column}',
            'xaxis': {'title': selected_column},
            'yaxis': {'title': 'Frequency'}
        }
    }


# Callback for filtering data
@app.callback(
    Output('filtered-data', 'children'),
    [Input('upload-data', 'contents'),
     Input('filter-column', 'value'),
     Input('filter-value', 'value')]
)
def filter_data(contents, filter_column, filter_value):
    if contents is None or filter_column is None or filter_value is None:
        return "Select a filter option."

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    filtered_df = df[df[filter_column] == filter_value]
    return html.Div([
        html.H5("Filtered Data"),
        html.Table([html.Tr([html.Th(col) for col in filtered_df.columns])] +
                   [html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns]) for i in range(min(len(filtered_df), 10))])
    ])


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
