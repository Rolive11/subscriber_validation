import os
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io
from datetime import datetime
import vs_part3
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define BASE_DIR
BASE_DIR = os.getcwd()  # Current working directory

app = dash.Dash(__name__)

# Add Tailwind CSS via CDN
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout with rearranged elements and modified styling
app.layout = html.Div(
    className="container mx-auto p-4",
    children=[
        html.H1("RSI Subscriber Validation Dashboard", className="text-2xl font-bold mb-4 text-center"),
        html.Div(id="validate-debug", className="text-sm text-gray-600 text-center mb-4"),
        html.Div(
            className="grid grid-cols-1 gap-4 mb-4",
            children=[
                html.Div(
                    children=[
                        html.Label("Company Name", className="block text-sm font-medium text-green-900"),
                        dcc.Input(id="company-name", type="text", placeholder="Enter company name", className="mt-1 block w-full border border-gray-300 rounded-md p-2")
                    ]
                ),
                html.Div(
                    children=[
                        html.Label("Company ID", className="block text-sm font-medium text-green-900"),
                        dcc.Input(id="company-id", type="text", placeholder="Enter company ID", className="mt-1 block w-full border border-gray-300 rounded-md p-2")
                    ]
                ),
                html.Div(
                    children=[
                        html.Label("User Email", className="block text-sm font-medium text-green-900"),
                        dcc.Input(id="user-email", type="email", placeholder="Enter user email", className="mt-1 block w-full border border-gray-300 rounded-md p-2")
                    ]
                )
            ]
        ),
        html.Div(
            className="mb-4 mt-6 p-6 bg-gray-50 rounded-md",
            children=[
                html.Label("Upload Subscriber CSV", className="block text-sm font-medium text-gray-700 mb-2"),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and Drop or ", html.A("Select a CSV File", className="text-blue-500 underline")]),
                    className="border-2 border-dashed border-gray-300 p-4 text-center rounded-md",
                    accept=".csv",
                    multiple=False
                ),
                html.Div(id="upload-feedback", className="text-sm text-gray-600 mt-2")
            ]
        ),
        html.Div(id="upload-error", className="mb-4 text-red-600 flex items-center space-x-2 justify-center"),
        html.Div(
            className="flex space-x-4 mb-4",
            children=[
                html.Button("Validate", id="validate-button", className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed", disabled=False),
                html.Button("Clear", id="clear-button", className="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600")
            ]
        ),
        html.Div(
            id="validation-result",
            className="mt-4",
            children=[
                html.H2("Validation Results", className="text-xl font-semibold mb-2"),
                html.Div(id="validation-summary", children="")
            ]
        ),
        dash_table.DataTable(
            id="error-table",
            columns=[
                {"name": "Row", "id": "Row"},
                {"name": "Column", "id": "Column"},
                {"name": "Error", "id": "Error"},
                {"name": "Value", "id": "Value"}
            ],
            data=[],
            style_table={"overflowY": "auto", "maxHeight": "400px"},
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"backgroundColor": "#f1f5f9", "fontWeight": "bold"}
        ),
        dcc.Store(id="upload-store"),
        dcc.Download(id="download-report")
    ]
)

# Clientside callbacks
app.clientside_callback(
    """
    function(store_data, company_name, company_id, user_email) {
        return false;
    }
    """,
    Output("validate-button", "disabled"),
    [Input("upload-store", "data"), Input("company-name", "value"), Input("company-id", "value"), Input("user-email", "value")]
)

app.clientside_callback(
    """
    function(store_data, company_name, company_id, user_email) {
        return "Validate Button State: Always Enabled";
    }
    """,
    Output("validate-debug", "children"),
    [Input("upload-store", "data"), Input("company-name", "value"), Input("company-id", "value"), Input("user-email", "value")]
)

# Updated process_upload callback
@app.callback(
    [
        Output("upload-store", "data"),
        Output("upload-error", "children"),
        Output("upload-feedback", "children"),
        Output("validation-result", "children"),
        Output("error-table", "data", allow_duplicate=True),
        Output("error-table", "style_data_conditional", allow_duplicate=True),
        Output("download-report", "data", allow_duplicate=True),
    ],
    Input("upload-data", "contents"),
    [State("upload-data", "filename"), State("company-name", "value"), State("company-id", "value"), State("user-email", "value")],
    prevent_initial_call=True
)
def process_upload(contents, filename, company_name, company_id, user_email):
    if contents is None:
        return (None, "", "No file uploaded", html.Div([html.H2("Validation Results", className="text-xl font-semibold mb-2"), html.Div(id="validation-summary", children="")]), [], [], None)

    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if not filename.lower().endswith(".csv"):
            return (
                {"filename": filename, "valid": False, "error": "File must be a CSV"},
                html.Div([html.I(className="fas fa-exclamation-triangle mr-2 text-red-600"), "File must be a CSV"]),
                "",
                html.Div([html.H2("Validation Results", className="text-xl font-semibold mb-2"), html.Div(id="validation-summary", children="")]),
                [],
                [],
                None
            )

        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), dtype=str)
        expected_columns = ["customer", "lat", "lon", "address", "city", "state", "zip", "download", "upload", "voip_lines_quantity", "business_customer", "technology"]
        actual_columns = [col.strip() for col in df.columns]
        header_errors = []
        header_table_data = []
        uppercase_headers = []

        def get_column_letter(index):
            return chr(65 + index)

        # Check for case-sensitivity
        for col in actual_columns:
            for expected in expected_columns:
                if col.lower() == expected.lower() and col != expected:
                    uppercase_headers.append((col, expected))
                    header_errors.append(f"Header '{col}' is uppercase, expected '{expected}'")
                    header_table_data.append({"Actual Header": col, "Expected Header": expected, "Issue": "Uppercase"})
                    break

        # Check for incorrect, extra, or missing headers
        incorrect_headers = []
        for col in actual_columns:
            if col not in expected_columns and not any(col.lower() == expected.lower() for expected in expected_columns):
                incorrect_headers.append(col)
                expected = expected_columns[actual_columns.index(col)] if actual_columns.index(col) < len(expected_columns) else "N/A"
                header_errors.append(f"Header '{col}' is incorrect, expected '{expected}'")
                header_table_data.append({"Actual Header": col, "Expected Header": expected, "Issue": "Incorrect spelling"})

        extra_columns = [(i, col) for i, col in enumerate(actual_columns) if col not in expected_columns and not any(col.lower() == expected.lower() for expected in expected_columns) and actual_columns[:i].count(col) > 0]
        for i, col in extra_columns:
            header_errors.append(f"Extra column '{col}' in column {get_column_letter(i)}")
            header_table_data.append({"Actual Header": col, "Expected Header": "N/A", "Issue": f"Extra column in column {get_column_letter(i)}"})

        matched_columns = [col.lower() for col in actual_columns if any(col.lower() == expected.lower() for expected in expected_columns)]
        missing_columns = [col for col in expected_columns if col.lower() not in matched_columns]
        for col in missing_columns:
            header_errors.append(f"Missing column: {col}")
            header_table_data.append({"Actual Header": "N/A", "Expected Header": col, "Issue": "Missing column"})