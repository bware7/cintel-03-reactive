import plotly.express as px
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_plotly
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import reactive

# Load the Palmer Penguins dataset
penguins = load_penguins()

# Set the page options with the title "Penguin Data Exploration"
ui.page_opts(title="Penguin Data Exploration - Bin Ware", fillable=True)

# Reactive filtered data with NaN and empty DataFrame handling
@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    if selected_species:
        filtered_df = penguins[penguins["species"].isin(selected_species)]
        # Check for empty DataFrame and handle NaN
        if filtered_df.empty:
            return None  # Return None if the DataFrame is empty
        return filtered_df.dropna()  # Drop rows with NaN values if necessary
    return penguins.dropna()  # Return the complete DataFrame without NaN if no selection is made

# Sidebar for user interaction
with ui.sidebar(position="right", bg="#f8f8f8", open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Select column to visualize",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected="bill_length_mm"
    )
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 10, min=1, max=30)
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 5, 50, 15, step=5)
    ui.input_checkbox_group(
        "selected_species_list",
        "Select Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True
    )
    ui.hr()
    ui.h5("GitHub Code Repository")
    ui.a("View on GitHub", href="https://github.com/bware7/cintel-03-reactive", target="_blank")

# Main content layout
with ui.layout_columns():
    # Plotly Histogram using filtered data
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotly_histogram():
            data = filtered_data()
            if data is not None:
                return px.histogram(
                    data, 
                    x=input.selected_attribute(),
                    nbins=input.plotly_bin_count(),
                    color="species"
                )
            else:
                return "No data available for the selected filters"

    # Data Table using filtered data
    with ui.card(full_screen=True):
        ui.card_header("Data Table")
        @render.data_frame
        def data_table():
            data = filtered_data()
            if data is not None:
                return data
            else:
                return "No data available for the selected filters"

    # Data Grid using filtered data
    with ui.card(full_screen=True):
        ui.card_header("Data Grid")
        @render.data_frame
        def data_grid():
            data = filtered_data()
            if data is not None:
                return data
            else:
                return "No data available for the selected filters"

# Additional visualizations
with ui.layout_columns():
    # Plotly Scatterplot using filtered data
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Body Mass vs. Bill Depth")
        @render_plotly
        def plotly_scatterplot():
            data = filtered_data()
            if data is not None:
                return px.scatter(
                    data_frame=data,
                    x="body_mass_g",
                    y="bill_depth_mm",
                    color="species",
                    labels={"bill_depth_mm": "Bill Depth (mm)", "body_mass_g": "Body Mass (g)"}
                )
            else:
                return "No data available for the selected filters"

    # Seaborn Histogram using filtered data
    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram: Body Mass")
        @render.plot
        def seaborn_histogram():
            data = filtered_data()
            if data is not None:
                fig, ax = plt.subplots()
                sns.histplot(
                    data=data, 
                    x="body_mass_g", 
                    hue="species", 
                    bins=input.seaborn_bin_count(), 
                    ax=ax
                )
                ax.set_xlabel("Mass (g)")
                ax.set_ylabel("Count")
                ax.set_title("Body Mass Distribution (Seaborn)")
                return fig
            else:
                return plt.figure()  # Return an empty figure if no data

    # Summary Statistics Table using filtered data
    with ui.card(full_screen=True):
        ui.card_header("Summary Statistics")
        @render.data_frame
        def summary_table():
            data = filtered_data()
            if data is not None:
                summary = data.describe()
                return summary.reset_index()
            else:
                return "No data available for the selected filters"
