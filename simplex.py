import numpy as np
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

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

tableau_list = []
res_file = "lpp.pdf"

num_variables = 2
num_constraints = 2
table = np.array([
    [1, 1, 12],
    [2, 1, 16],   
    [40, 30, 0]
], dtype=float)

tableau = make_tableau(table)
# tableau = np.array([
#     [1, 1, 1, 0, 0, 12],
#     [2, 1, 0, 1, 0, 16],
#     [-40, -30, 0, 0, 1, 0]
# ], dtype=float)

tableau_list.append(tableau.copy())  # Save a copy of the initial tableau

# Perform the first Simplex iteration
simplex_iteration(tableau)
tableau_list.append(tableau.copy())  # Save a copy after the first iteration

# Perform the second Simplex iteration
simplex_iteration(tableau)
tableau_list.append(tableau.copy())  # Save a copy after the second iteration

# Save all tableaux to PDF
save_tableaux_to_pdf(tableau_list, res_file)

webbrowser.open_new(res_file)