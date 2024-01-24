import tkinter as tk


root = tk.Tk()

root.geometry('700x700')
root.configure(bg='#f4f4f6',)

l1 = tk.Label(root, text="Number of Variables:", font=('Poppins 16'),fg='#09090b',bg='#f4f4f6',)
l1.pack()


l2 = tk.Label(root, text="Number of Constraints:", font=('Poppins 16'),fg='#09090b',bg='#f4f4f6',)
l2.pack()

root.mainloop()
