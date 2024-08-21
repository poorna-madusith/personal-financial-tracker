import json #import json for save trasnaction in json formt
import tkinter as tk#import tkinter to create gui for the program
from tkinter import messagebox, simpledialog#from tkinter import messagebox and simpledialog to handle gui operations
from tkinter import ttk

class FinancialTracker:
    def __init__(self):
        #initialize transactions dictionary
        self.transactions = {}
        #load existing transactions from the JSONfile
        self.load_transactions()

    def load_transactions(self):#create laod trasnactions function to load trasnactions from the json file
        try:
            with open("transactions.json","r") as file:#open transactions file in r mode
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = {}

    def save_trasactions(self):#create save transactions for the save transaction inside the json file
        with open("transactions.json","w") as file:#open trasnactions.json file in write mode and save the transaction details inside the json file
            json.dump(self.transactions,file, indent=4)

    def transactiontype_input(self):#create a function to handle the transaction type  inputs
        while True:
            user_input = simpledialog.askstring("input","Enter the type of transaction")#get user input usong tkinter simpldialog
            if user_input is None:#chiek user input is none
                return
            else:
                user_input = user_input.lower()#if not make user input to lowercase
            if user_input in ["income","expense"]:#check whether user input in mentioned list
                return user_input
            else:#if not show error message usiing tkinter messagebox
                messagebox.showerror("Error","Please enter income or expense")

    def instructions(self):#cretae a fucntion to show intrctions to the user to use the program
        messagebox.showinfo("Instructions","1. To add Transactions click add button and enter the transaction detais\n2. to veiw your transaction history click veiw transactions button\n3. to update transactiosnc lick update transaction button and enter category and index of the trasnaction you want to update and then enter the new transaction details\n4. to delete a trasnaction enter the category and index number of the transaction then ur transaction will be deleted\n5. to search trasnaction based on criteria enter the criteria and then program will shw=ow the all details\n6. to see summary of your all trabsactions select the summary button\n7. if you want to add more than one transaction at the same time select the read transactions from a file button. first you have to create a text file and enter the trasnaction details in this format one under other category,type,amount,date. then enter the file name with txt extenstion.then all details will be added and saved\n7. if you click select exit button your all transactions will be saved and you can exit from the financial tracker")


    def search_transactions(self):#creta a function to search transactions
        search_criteria = simpledialog.askstring("input","Enter the search ctiteria (category,type,amount,date): ")#ask the criteria using tkinter simpledialog
        #check search criteria is none or nor if none return and if not make search criteira input to lowercase
        if search_criteria is None:
            return
        else:
            search_criteria = search_criteria.lower()
    
    
        if search_criteria in ["category","type","amount","date"]:#check search criteria inside the mentioned list
            search_value = simpledialog.askstring("input","Enter the value you want to search: ")#ask the search value using tkinter simpledialog
            #check search value is none or nor if none return and if not make search value input to lowercase
            if search_value is None:
                return
            else:
                search_value = search_value.lower()
            output = "search results\n"#make a varialble name output and assingned it into search results string
            for category,trans in self.transactions.items():#go theourh wach category and trasactions
                for t in trans:
                    if search_criteria == "category" and category == search_value:#check the search criteria is category and matches the search value
                        output += f"Category: {category}, Type: {t["type"]}, Amount:{t["amount"]}, Date: {t["date"]}\n"
                    elif str(t.get(search_criteria)) == search_value:#check if search criteria matches any transaction attribute and matches the search value
                        output += f"Category: {category}, Type: {t["type"]}, Amount:{t["amount"]}, Date: {t["date"]}\n"
        
            if output == "search results\n":#check if any results are found
                output = "No transactions found maching in the search criteria"
            messagebox.showinfo("search results",output)#display the search results using tkinter messagebox
        else:#if search criteria not in metioned list display error message using message boc
            messagebox.showerror("Error","There is no such a criteria.only exist category,type,amount and date")
    
    

    def read_bulk_transactions_fromfile(self):#cretae a function read transactions from a text file
        filename = simpledialog.askstring("input","Enter file name (e.g:- filename.txt): ")#ask the file name from user using simple dialog
        if filename is None:
            return
        try:
            with open(filename,"r") as file:#open the user mentioned text file in read mode and read it 
                for line in file:
                    category,type,amount,date = line.strip().split(',')
                    amount = float(amount)
                    if category in self.transactions:#if category already exist add deatils in to that category
                        self.transactions[category].append({"type": type, "amount": amount, "date": date})
                    else:#if not create a new category and add the details
                        self.transactions[category] = [{"type": type, "amount": amount, "date": date}]
                messagebox.showinfo("succsess","succsessfully read from the file")
        except FileNotFoundError:#if filenotfounderror comes display a error message using messagebox
            messagebox.showerror("error","there is no such a file")
        except ValueError:#if there any value error inside the text file display an error message
            messagebox.showerror("error","Error reading transactions form the file\nplease enter transactions inside the file this format\ncategory,type,amount,date")

    def add_transactions(self):#create a function to add a transaction
        category = simpledialog.askstring("input","Enter the category of transaction: ")#ask the category
        if category is None:
            return
        else:
            category = category.lower()
    
        type = self.transactiontype_input()#call transactiontype_function to get the trasnaction type input
        if type is None:
            return

        amount = simpledialog.askfloat("input","Enter the amount of your transaction")#ask amount from the user
        if amount is None:
            return
    
        date = simpledialog.askstring("input","Enter the date")#ask date from user
        if date is None:
            return
        #cretate a dictioanry to to store the transaction details
        trans = {"type": type, "amount": amount, "date": date}

        if category in self.transactions:#check category is already exsist
            self.transactions[category].append(trans)#if yes add details in to that category
        else:
            self.transactions[category] = [trans]#if not cretae a new  category and add the details

        messagebox.showinfo("Succsess","Transaction added succsessfully")#displaya message using tkinter messagebox

    def veiw_transactions(self):#create a fucntion to veiw the transactions
        #create a new windows for display transactions
        window = tk.Tk()
        window.title("Transactions History")

        #create tree veiw widget
        tree = ttk.Treeview(window)
        tree["columns"] = ("Type", "Amount", "Date")

        #define column headings
        tree.heading("#0", text = "Category")
        tree.heading("Type", text = "Type")
        tree.heading("Amount", text = "Amount")
        tree.heading("Date", text = "Date")

        #populate tree veiw with data
        for category, tra in self.transactions.items():
            for trans in tra:
                tree.insert("",'end',text = category, values=(trans["type"], trans["amount"], trans["date"]))

        #display tree veiw
        tree.pack(expand = True,fill="both")

    def update_transacions(self):#create a function to update a transaction
        category = simpledialog.askstring("input","Enter the category you want to update")#ask category from user
        if category is None:#check category is none
            return#if yes return from the function
        else:
            category = category.lower()#if not make the category input to lower
    
        if category in self.transactions:#check category in trasnactions dictionary
            output = ""#assign output variable to emplty string
            for index,tra in enumerate(self.transactions[category]):#go throuth the trasnactions dictionary and index each transaction using enumarate
                output += f"{index+1}. Type:{tra['type']}, Amount: {tra['amount']}, Date: {tra['date']}\n"

            choice = simpledialog.askinteger("input",f"Please select the index of the transaction you want to update: \n{output}")#ask the index of the trasnaction user want to update
            if choice is None:#if choice is none return from the fucntion
                return

        
            if choice and 0 < choice <= len(self.transactions[category]):#check the index is valid
                type = self.transactiontype_input()#callctype function to ask the typr of trasnaction
                if type is None:
                    return

                amount = simpledialog.askfloat("input","Enter the amount of your transaction: ")#ask amount from the user
                if amount is None:#if amount is none return from the function
                    return
    
                date = simpledialog.askstring("input","Enter the date")#ask the date from user
                if date is None:#if date is none return from the function
                    return
            
                self.transactions[category][choice-1] = {"type": type, "amount": amount, "date": date}#update the trasnaction with new details
                messagebox.showinfo("Succsess","Trasnactions updated succsessfully")#display a message to user using tkinter messagebox
            else:
                messagebox.showerror("Error","Invalid index")#if index is not valid displaya message to user
        else:
            messagebox.showerror("Error",f"There is no such a category named{category}")#if cateogry not in trasnaction display error message


    def delete_trasnaction(self):#crreate a function to delete a trasnaction
        category = simpledialog.askstring("input","Enter the category you want to delete: ")#ask the category from user using tkinter simpledialog
        if category is None:#if category is none return from the function
            return
        else:#if not turn category input into lowercase
            category = category.lower()
        if category in self.transactions:#check category in transactions dictionary
            output = ""#if yes assign output variable into empty string
            for index,tra in enumerate(self.transactions[category]):#based on the category user enterd go through the dictionary and display all the transaction details with index before each transaction
                output += f"{index+1}. Type:{tra['type']}, Amount: {tra['amount']}, Date: {tra['date']}\n"

            choice = simpledialog.askinteger("input",f"Please select the index of the transaction you want to delete: \n{output}")#ask the index number user want to delete using tkinter simpledialog
            if choice is None:#if choice is none return from the function
                return

            if choice and 0 < choice <= len(self.transactions[category]):#check if index is valid
                del self.transactions[category][choice-1]#if yes delete the indexed transaction
                messagebox.showinfo("Success","Trasnaction deleted succsessfully")#displaya message using tkinter messagebox
            else:
                messagebox.showerror("Error","Invalid index")#if index is invalid display an error message
        else:
            messagebox.showerror("Error",f"There is no category named {category}")#if category not in transactions display error message using tkinter messagebox

    def display_summary(self):#create a function to display summary of transactions
        total_income = 0#assign total income to zero
        total_expense = 0#assign total expense to zero
        output = "Summary of trasnactions\n"#assingn output in to summary of transactions string

        for category,trans in self.transactions.items():#go throuth the transactions dictionary
            total = sum(tra['amount'] for tra in trans)#get the sum of all transactions amounts
            total_income += sum(tra['amount'] for tra in trans if tra['type'] == "income")#get the total amount of each transactions where type equals to income
            total_expense += sum(tra['amount'] for tra in trans if tra['type'] == "expense")#get the total amount of each transactions where type equals to expense

            output += f"{category}: total amount{total}\n"#add cateogry and total amounts of each catgory to output vairable

        output += f"\nTotal income: {total_income}\n"#add total income to output
        output += f"Total expense: {total_expense}\n"#add total expense to output
        output += f"Net balance: {total_income- total_expense}\n"#add net balance by substractiong total expense from total income and add it to ouput

        messagebox.showinfo("Summary",output)#dispplay output using tkinter messagebox

def main_menu():#create a function for main menu 
    tracker = FinancialTracker()

    #create the mainmenu window using tkinter
    window = tk.Tk()
    window.geometry("400x500")
    window.configure(bg="lightblue")
    window.title("Personal Financial Tracker")

    #create and pack the welcome label
    label1 = tk.Label(window,text="WELCOME!!!\nTO YOUR\nPERSONAL FINANCIAL TRACKER", font=("Comic Sans Ms",16),bg="lightblue")
    label1.pack()

    #create and pack the buttons for varius functionaliteis
    add_button = tk.Button(window,text="Add Transactions",command=tracker.add_transactions,fg="white",bg="black")
    add_button.pack(pady=10)

    veiw_button = tk.Button(window,text="Veiw Transactions",command=tracker.veiw_transactions,fg="white",bg="black")
    veiw_button.pack(pady=10)

    update_button = tk.Button(window,text="Update Transaction",command=tracker.update_transacions,fg="white",bg="black")
    update_button.pack(pady=10)

    delete_button = tk.Button(window,text="Delete Transaction",command=tracker.delete_trasnaction,fg="white",bg="black")
    delete_button.pack(pady=10)

    search_button = tk.Button(window,text="Search Transactions",command=tracker.search_transactions,fg="white",bg="black")
    search_button.pack(pady=10)

    summary_button = tk.Button(window,text="Display Summary",command=tracker.display_summary,fg="white",bg="black")
    summary_button.pack(pady=10)

    read_button = tk.Button(window,text="Read Transactions From A File",command=tracker.read_bulk_transactions_fromfile,fg="white",bg="black")
    read_button.pack(pady=10)

    exit_button = tk.Button(window,text="Exit",command=lambda:[tracker.save_trasactions(),window.destroy()],fg="white",bg="black")
    exit_button.pack(pady=10)

    about_button = tk.Button(window,text="About",command=tracker.instructions,fg="white",bg="black")
    about_button.pack(side = "bottom",padx=10, pady=10, anchor="se")

    #run the main loop of the tikinter window
    window.mainloop()

main_menu()#call main_menu function to strat the program

