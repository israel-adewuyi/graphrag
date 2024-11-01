import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_bar_chart(numbers: list, filename: str) -> None:
    """
    Creates a bar chart from a list of numbers and saves it to a file.
    
    Args:
        numbers: List of numbers to plot
        filename: Name of the file to save the plot to (without extension)
        
    Example:
        plot_bar_chart([1, 2, 3, 4, 5], "my_plot")
    """
    # Create figure
    fig = make_subplots()
    
    # Add bar trace
    fig.add_trace(
        go.Bar(
            x=list(range(len(numbers))),  # X-axis is the index
            y=numbers,                     # Y-axis is the values
            marker_color='rgb(55, 83, 109)',
            name='Values'
        )
    )
    
    # Update layout with better styling
    fig.update_layout(
        title={
            'text': f'Number of token distribution for {filename} transcript',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Index',
        yaxis_title='Value',
        bargap=0.2,
        showlegend=False,
        template='plotly_white'
    )
    
    # Save the plot to HTML (interactive)
    fig.write_html(f"{filename}.html")
    
    # Also save as PNG for static version
    fig.write_image(f"artifacts/{filename}.png")
    
    print(f"Plot saved as {filename}.html and {filename}.png")