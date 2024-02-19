import tkinter as tk
from tkinter import ttk
import numpy as np
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

global num_variables, num_constraints, constraints_entries, objective_entries, tableau, tableau_list, res_file
res_file = "lpp.pdf"

def simplex_iteration(tableau):
    pivot_column = np.argmin(tableau[-1, :])
    positive_ratios = tableau[:-1, -1] / tableau[:-1, pivot_column]
    pivot_row = np.argmin(positive_ratios)

    pivot_element = tableau[pivot_row, pivot_column]
    tableau[pivot_row, :] /= pivot_element

    for i in range(len(tableau)):
        if i == pivot_row:
            continue
        mult = -1 * tableau[i, pivot_column]
        tableau[i, :] += mult * tableau[pivot_row, :]

def save_tableaux_to_pdf(tableau_list, filename):
    c = canvas.Canvas(filename)
    c.setTitle("Solution to LPP")
    yaxis = 720    
    
    c.setFont('Helvetica-Bold', 16) 
    c.drawString(95,800,"Step-wise Solution to your Linear Programming Problem")
    
    c.setFont('Helvetica', 14) 
    for iteration, tableau in enumerate(tableau_list):
        if iteration == 0:
            c.drawString(85, yaxis+20, f"Initial Tableau:")
        else: 
            c.drawString(85, yaxis+20, f"Tableau after iteration {iteration}:")
        row_height = 20
        for i, row in enumerate(tableau):
            for j, val in enumerate(row):
                c.drawString(85 + j * 50, yaxis - i * row_height, str(val))
        yaxis  -= 1.5 * inch
        
    c.save()
    print(f"Tableaux saved to {filename}")

def make_tableau(table):
    tableau = np.zeros((num_constraints+1,num_variables+num_constraints+2))
    b = 0
    for row in table:
        for index ,element in  enumerate(row):         
            if(index == num_variables):
                tableau[b][-1] = element
                b = b+1
                continue
            if(b==num_constraints):
                tableau[b][index] = -1 * element
                continue
            tableau[b][index] = element
    return tableau

def calculate():  
    table = np.zeros((num_constraints+1, num_variables+1),dtype=float)

    for i in range(num_constraints):
        for j in range(num_variables+1):
            entry_value = float(constraints_entries[i][j].get())
            table[i][j] = entry_value
    
    for i in range(num_variables):
        entry_value = float(objective_entries[i].get())
        table[-1][i] = entry_value
        
    global tableau
    tableau = make_tableau(table) # implementing slack variables is remaining
    print(tableau)
    
    global tableau_list 
    tableau_list = []
    
    # Save all tableaux to PDF
    save_tableaux_to_pdf(tableau_list, res_file)
    
    pdf_button = ttk.Button(root, text="PDF", command= webbrowser.open_new(res_file) , width=15)
    pdf_button.grid(row=6, column=1, pady=10) # pos to be changed 
    
def generate():
    global num_variables,num_constraints
    num_variables = int(variables_var.get())
    num_constraints = int(constraints_var.get())

    # Clear existing components in the input_frame
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Create entry widgets for objective function
    global objective_entries
    objective_entries = []

    ttk.Label(input_frame, text="Objective Function Z = ", font=custom_font).grid(row=1, column=0, padx=5, pady=5)
    for i in range(num_variables):
        obj_entry = ttk.Entry(input_frame, width=5)
        obj_entry.grid(row=1, column= i*2 + 1, padx=5, pady=5)
        objective_entries.append(obj_entry)
        ttk.Label(input_frame, text=f"x{i + 1}").grid(row=1, column= i*2 + 2, padx=5, pady=5)

    # Create entry widgets for constraints
    global constraints_entries
    constraints_entries = []
    for i in range(num_constraints):
        ttk.Label(input_frame, text=f"Constraint {i + 1}:", font=custom_font).grid(row=i + 2, column=0, padx=5, pady=5)

        entries_row = []
        for j in range(num_variables):
            entry = ttk.Entry(input_frame, width=5)
            entry.grid(row=i + 2, column=j * 2 + 1, padx=5, pady=5)
            entries_row.append(entry)
            ttk.Label(input_frame, text=f"x{j + 1}").grid(row=i + 2, column=j * 2 + 2, padx=5, pady=5)
            
        eq_combobox = ttk.Combobox(input_frame, values=eq_options)
        eq_combobox.grid(row=i + 2, column=num_variables * 2 + 1, padx=5, pady=5)
        eq_combobox.current(0)
        
        rhs_entry = ttk.Entry(input_frame, width=5)
        rhs_entry.grid(row=i + 2, column=num_variables * 2 + 2, padx=5, pady=5)
        entries_row.append(rhs_entry)
        constraints_entries.append(entries_row)
    
    calculate_button = ttk.Button(root, text="Calculate", command=calculate, width=15)
    calculate_button.grid(row=6, column=1, pady=10)


# Options for the dropdowns
var_options = [2, 3, 4, 5, 6, 7, 8, 9]
eq_options = ['<=', '>=']

# Create the main window
root = tk.Tk()
custom_font = ("Helvetica", 15)
root.geometry('600x600')
root.title("Linear Programming Problem Solver")

# Create and grid the number of variables label and combobox
ttk.Label(root, text="Select number of variables", font=custom_font).grid(row=0, column=0, pady=5)
variables_var = tk.StringVar()
variables_combobox = ttk.Combobox(root, textvariable=variables_var, values=var_options)
variables_combobox.grid(row=0, column=1, pady=5)
variables_combobox.current(0)

# Create and grid the number of constraints label and combobox
ttk.Label(root, text="Select number of constraints", font=custom_font).grid(row=1, column=0, pady=5)
constraints_var = tk.StringVar()
constraints_combobox = ttk.Combobox(root, textvariable=constraints_var, values=var_options)
constraints_combobox.grid(row=1, column=1, pady=5)
constraints_combobox.current(0)

# Create and grid the Generate button
generate_button = ttk.Button(root, text="Generate", command=generate)
generate_button.grid(row=2, column=1, pady=10)

# Create the input frame
input_frame = ttk.Frame(root)
input_frame.grid(row=3, column=0, columnspan=2)

root.mainloop()