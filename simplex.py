import numpy as np
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

ratios = []
pivotcols , pivotrows = [],[]


def simplex_iteration(tableau):
    pivot_column = np.argmin(tableau[-1, :])
    pivotcols.append(pivot_column+1)

    positive_ratios = tableau[:-1, -1] / tableau[:-1, pivot_column]
    for ratio in positive_ratios:
        ratios.append(ratio)
    pivot_row = np.argmin(positive_ratios)
    pivotrows.append(pivot_row+1)

    pivot_element = tableau[pivot_row, pivot_column]
    tableau[pivot_row, :] /= pivot_element

    for i in range(len(tableau)):
        if i == pivot_row:
            continue
        mult = -1 * tableau[i, pivot_column]
        tableau[i, :] += mult * tableau[pivot_row, :]
        
def save_tableaux_to_pdf(tableau_list, filename):
    basicvar = ["Z"]
    for i in range(num_constraints):
        basicvar.append(f"s{i+1}")
    flag = False
    c = canvas.Canvas(filename)
    c.setTitle("Solution to LPP")
    yaxis = 720    
    count = 0
    c.setFont('Helvetica-Bold', 16) 
    c.drawString(95,800,"Step-wise Solution to your Linear Programming Problem")
    
    c.setFont('Helvetica', 14) 
    for iteration, tableau in enumerate(tableau_list):
        if flag:
            basicvar = list(map(lambda x: x.replace(f's{pivotrows[iteration-1]}', f'x{pivotcols[iteration-1]}'), basicvar))
        
    
        count2 = 1
        c.drawString(65, yaxis+20, f"Iteration     BasicVar                    Coefficients                           RHS                Ratio")
        cursor = 200
        row_height = 20
        for j in range(num_variables):
            c.drawString(cursor, yaxis , f"x{j+1}")
            cursor = 200 + 50
            
        for j in range(num_constraints):
            cursor = cursor + 50
            c.drawString(cursor,yaxis,f"s{j+1}")
        
        yaxis -= 1 * row_height
        
        for j, element in enumerate(tableau[-1]):
            c.drawString(200 + j * 50, yaxis , str(element))
             
        c.drawString(85 , yaxis , str(iteration))
        if iteration != 0:
            c.drawString(75 , yaxis-20, f"s{pivotrows[iteration-1]} leaves")
            c.drawString(75 , yaxis-40, f"x{pivotcols[iteration-1]} enters")
        
        yaxis -= 1 * row_height
        for i, row in enumerate(tableau):
            if(i != num_constraints):
                for j, val in enumerate(row):
                    c.drawString(200 + j * 50, yaxis - i * row_height, str(val))
                    
                if count < len(ratios):  # Check if count is within the range of ratios list
                    c.drawString(200 + num_constraints+num_variables+6.5 * 50, yaxis - i * row_height, str(ratios[count]))
                    count += 1
                
                if count2 < len(basicvar):  # Check if count is within the range of ratios list
                    c.drawString(160 , yaxis - i * row_height, basicvar[count2])
                    count2 += 1
            i -= 1
        yaxis  -= 1.5 * inch
        flag = True

    c.save()
    print(f"Tableaux saved to {filename}")

def make_tableau(table):
    tableau = np.zeros((num_constraints+1,num_variables+num_constraints+1))
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
    for i in range(0, num_constraints):
        tableau[i][num_variables + i] = 1
    return tableau
    
tableau_list = []
res_file = "lpp.pdf"

num_variables = 2
num_constraints = 3
table = np.array([
    [1, 1.5, 750],
    [2, 3, 1500],   
    [2, 1, 1000],
    [50, 40, 0]
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