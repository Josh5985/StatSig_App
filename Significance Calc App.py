import tkinter as tk
from scipy import stats
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from pptx import Presentation (imports for code that I am working on to make the app a bit more complex and output a power point slide. I am still working through the ways to make this function)
#from pptx.util import Inches

def calculate_significance(): #I am adding this an easy way to start. I need to add the field input verification to this code to ensure it works properly. 
    # Get inputs from the GUI required to calculate. 
    n1 = int(entry_sample_size_a.get())
    n2 = int(entry_sample_size_b.get())
    p1 = float(entry_percentage_a.get()) / 100
    p2 = float(entry_percentage_b.get()) / 100
    
    # Calculate pooled proportion
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    
    # Calculate the z-score
    z = (p1 - p2) / math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    
    # Calculate p-value from z-score (two-tailed test)
    p_value = stats.norm.sf(abs(z)) * 2
    
       # Variables to hold the significance level and status
    confidence_reached = None
    
    # Loop through different significance levels (80%-99%). I ordered descending here as you really want to understand the highest level it is significant at.
    for confidence in [0.99, 0.95, 0.90, 0.85, 0.80]:
        significance_level = 1 - confidence
        if p_value < significance_level:
            output_text.set(f"Significant at {confidence*100}% level (p-value: {p_value:.4f})")
            break
    else:
        output_text.set(f"Not significant (p-value: {p_value:.4f})")

   # Call the function to update the graph
    update_graph(p1, p2, confidence_reached)

def update_graph(p1, p2, confidence_reached):
    # Clear the previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    # Create a new figure
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Data for the bar chart
    labels = ['Percentage A', 'Percentage B']
    values = [p1 * 100, p2 * 100]
    
    # Plot the bars
    ax.bar(labels, values, color=['blue', 'orange'])
    
    # Add a line indicating the significance level, if any
    if confidence_reached:
        ax.axhline(confidence_reached * 100, color='red', linestyle='--', label=f'Significant at {confidence_reached*100}%')
        ax.legend()
    
    # Set the plot labels and title
    ax.set_ylabel('Percentages')
    ax.set_title('Percentage Comparison')
    
    # Embed the plot into Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def reset_fields():
    entry_sample_size_a.delete(0, tk.END)
    entry_percentage_a.delete(0, tk.END)
    entry_sample_size_b.delete(0, tk.END)  # Fixed the reference here
    entry_percentage_b.delete(0, tk.END)  # Fixed the reference here
    output_text.set('')  # Clear output text after reset
    
    # Clear the graph
    for widget in plot_frame.winfo_children():
        widget.destroy()

def reset_fields(): # This enables a reset button to clear fields and get ready for the next computation
    entry_sample_size_a.delete(0, tk.END)
    entry_percentage_a.delete(0, tk.END)
    entry_sample_size_b.delete(0, tk.END)  # Fixed the reference here
    entry_percentage_b.delete(0, tk.END)  # Fixed the reference here
    output_text.set('')  # Clear output text after reset

# Tkinter setup
root = tk.Tk()
root.title("Statistical Significance Calculator")

# Input fields
tk.Label(root, text="Sample Size A:").grid(row=0, column=0)
entry_sample_size_a = tk.Entry(root)
entry_sample_size_a.grid(row=0, column=1)

tk.Label(root, text="Percentage A:").grid(row=1, column=0)
entry_percentage_a = tk.Entry(root)
entry_percentage_a.grid(row=1, column=1)

tk.Label(root, text="Sample Size B:").grid(row=2, column=0)
entry_sample_size_b = tk.Entry(root)
entry_sample_size_b.grid(row=2, column=1)

tk.Label(root, text="Percentage B:").grid(row=3, column=0)
entry_percentage_b = tk.Entry(root)
entry_percentage_b.grid(row=3, column=1)

# Compute button
compute_button = tk.Button(root, text="Compute", command=calculate_significance)
compute_button.grid(row=4, column=0, columnspan=2)

# Reset button
reset_button = tk.Button(root, text="Reset", command=reset_fields)
reset_button.grid(row=4, column=2, padx=5, pady=5)

# Output label
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text)
output_label.grid(row=5, column=0, columnspan=2)

# Frame for the plot
plot_frame = tk.Frame(root)
plot_frame.grid(row=6, column=0, columnspan=3)

root.mainloop()
