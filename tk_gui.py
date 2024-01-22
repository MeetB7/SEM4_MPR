import tkinter as tk
from tkinter import ttk

# Options for the dropdowns
var_options = [2, 3, 4, 5, 6, 7, 8, 9]
eq_options = [ '<=' , '>=']

def generate():
    num_variables = int(variables_var.get())
    num_constraints = int(constraints_var.get())

    # Clear existing components in the input_frame
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Create entry widgets for objective function
    ttk.Label(input_frame, text="Objective Function: Z =", font=custom_font).grid(row=0, column=0, padx=5, pady=5, columnspan=num_variables * 2 + 2)

    for i in range(num_variables):
        ttk.Entry(input_frame, width=5).grid(row=1, column=i * 2 + 1, padx=5, pady=5)
        ttk.Label(input_frame, text=f"x{i + 1}").grid(row=1, column=i * 2 + 2, padx=5, pady=5)

    # Create entry widgets for constraints
    for i in range(num_constraints):
        ttk.Label(input_frame, text=f"Constraint {i + 1}:", font=custom_font).grid(row=i + 2, column=0, padx=5, pady=5)

        for j in range(num_variables):
            ttk.Entry(input_frame, width=5).grid(row=i + 2, column=j * 2 + 1, padx=5, pady=5)
            ttk.Label(input_frame, text=f"x{j + 1}").grid(row=i + 2, column=j * 2 + 2, padx=5, pady=5)

        ttk.Combobox(input_frame, values=eq_options).grid(row=i + 2, column=num_variables * 2 + 1, padx=5, pady=5)
        ttk.Entry(input_frame, width=5).grid(row=i + 2, column=num_variables * 2 + 2, padx=5, pady=5)

# Create the main window
root = tk.Tk()
custom_font = ("Helvetica", 15)
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
