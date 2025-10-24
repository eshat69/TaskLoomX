# importing necessary libraries
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime

# helper: suggest category based on task content (module-level so methods can call it)
def suggest_category(task):
    task_lower = task.lower()
    if any(word in task_lower for word in ["work", "office", "job", "task", "duty", "assignment", "project", "meeting", "report", "deadline", "client"  ,
                                             "presentation", "schedule", "plan", "strategy", "target", "goal", "performance", "feedback",
                                             "update", "progress", "documentation", "note", "follow-up", "tasklist", "agenda", "brief", "outline",
                                             "draft", "submission", "approval", "revision", "deliverable", "milestone", "workflow",
                                             "timeline", "summary", "objective", "planning", "priority"
                                             ]):
        return "Work"
    elif any(word in task_lower for word in ["dataset", "model", "training", "testing", "evaluation", "accuracy", 
                                             "precision", "recall",
                                             "algorithm", "simulation", "reproducibility", "AI", "ML", "LLM", "prompt engineering",
                                             "deep learning", "neural network", "code review", "experiment setup"]):
        return "Technical / AI Research"
    elif any(word in task_lower for word in ["supervisor", "conference", "presentation", "defense", "project proposal", "research group",
                                             "publication", "peer review", "submission", "revision", "collaboration", "coauthor", "lab",
                                             "experiment log", "grant application", "literature review", "academic writing"]):
        return "Academic Process"
    elif any(word in task_lower for word in ["doctor", "hospital", "clinic", "appointment", "checkup", "prescription", "medicine", "tablet",
                                             "symptom", "diagnosis", "therapy", "vaccination", "dentist", "eye", "test", "medical report"]):
        return "Health"
    elif any(word in task_lower for word in ["exercise", "workout", "gym", "yoga", "meditation", "jogging", "running", "cycling", "stretching",
                                             "cardio", "training", "diet", "protein", "nutrition", "weight loss", "health goal", "fitness plan"]):
        return "Fitness & Exercise"
    elif any(word in task_lower for word in ["mental", "meditation", "stress", "relaxation", "therapy", "self-care", "mindfulness", "rest",
                                             "sleep", "balance", "happiness", "calm", "positivity", "well-being", "journaling", "gratitude"]):
        return "Mental & Emotional Wellness"
    elif any(word in task_lower for word in ["movie", "music", "party", "trip", "travel", "holiday", "vacation", "shopping", "gift", "outing", "game",
                                            "festival", "photography", "hangout", "celebration", "event"]):
        return "Lifestyle & Leisure"
    elif any(word in task_lower for word in ["money", "finance", "budget", "expense", "income", "saving", "investment", "balance", "account",
                                             "bill", "invoice", "tax", "credit", "debit", "bill", "pay", "payment", "invoice", "due", "rent", 
                                             "tax", "fee", "credit", "debit", "subscription",
                                             "utility", "recharge", "mobile bill", "internet bill",
                                             "statement", "transaction", "wallet", "banking", "deposit", "withdraw","salary", "stipend", "wage",
                                             "earning", "bonus", "commission", "payroll", "allowance", "income source", "plan", "goal", "savings plan", 
                                             "insurance", "policy", "retirement", "portfolio", "stock", "share",
                                             "mutual fund", "crypto", "loan", "EMI", "debt", "interest", "finance tracking"]):
        return "Finance"
    elif any(word in task_lower for word in ["family", "friend", "mom", "dad", "brother", "sister", "relative", "partner", "love", "date", "spouse",
                                            "marriage", "anniversary", "relationship", "call", "visit", "talk", "dinner", "lunch", "breakfast", 
                                            "hangout", "get-together", "reunion", "chat","support", "help", "advice", "counseling", "empathy",
                                            "understanding", "compassion", "gift", "shopping","celebration", "event", "outing"]):
        return "Social & Relationships"
    elif any(word in task_lower for word in ["hobby", "goal", "journaling", "learning", "play","reading", "course", "study", "motivation", "reflection",
                                            "self-improvement", "relaxation", "creativity", "exploration", "adventure", "travel", "vacation", "trip", "outing",
                                            "fun", "entertainment", "music", "art", "craft", "photography", "writing", "blogging", "vlogging", "gaming", 
                                            "movie", "theater", "theatre",]):
        return "Personal"
    return "General"

# defining the main application class
class TodoList:
    def __init__(self, master):
        # setting up the main window
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("400x500")
        self.master.configure(bg="#BD5F12")

        # setting up styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#BD5F12")
        style.configure("TButton", padding=10, font=('Times New Roman', 10))
        style.configure("TLabel", background="#BD5F12", font=('Times New Roman', 10))
        style.configure("TEntry", padding=10, font=('Times New Roman', 10))
        style.configure("Treeview", font=('Times New Roman', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Times New Roman', 10, 'bold'))
        style.map('TButton', background=[('active', '#FFA500')])

        # setting up the main frame
        self.frame = ttk.Frame(self.master, padding=10, style="TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # setting up widgets
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.frame, textvariable=self.task_var, width=30, style="TEntry")
        self.task_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Add Task button
        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Task list display
        #self.task_tree = ttk.Treeview(self.frame, columns=("Task", "Priority", "Created At", "Status"), show="headings", style="Treeview")
        self.task_tree = ttk.Treeview(
        self.frame,
        columns=("Task", "Priority", "Created At", "Status", "Category"),
        show="headings",
        style="Treeview"
    )
        self.task_tree.heading("Category", text="Category")
        self.task_tree.heading("Task", text="Task")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Created At", text="Created At")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Color coding based on priority
        self.task_tree.tag_configure("High", background="#FF8783") 
        self.task_tree.tag_configure("Mid", background="#F7E26D")   
        self.task_tree.tag_configure("Low", background="#63C763") 

        # Color coding based on category
        self.task_tree.tag_configure("Work", foreground="#1E90FF")
        self.task_tree.tag_configure("Health", foreground="#228B22")
        self.task_tree.tag_configure("Finance", foreground="#8B0000")
        self.task_tree.tag_configure("Personal", foreground="#DA70D6")

    # initial placeholder row removed (was using undefined variables)
        # Adding scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Control buttons for delete, edit, save, and sort
        self.delete_button = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.edit_button = ttk.Button(self.frame, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.save_button = ttk.Button(self.frame, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.sort_button = ttk.Button(self.frame, text="Sort by Priority", command=self.sort_by_priority)
        self.sort_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.toggle_button = ttk.Button(self.frame, text="Toggle Status", command=self.toggle_status)
        self.toggle_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # configuring grid weights
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)        

        self.load_tasks()

# defining methods for task operations   
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            priority = simpledialog.askstring("Priority", "Enter priority (High,Mid,Low):", parent=self.master)
            category = suggest_category(task)
            if priority and priority.lower() in ["high", "mid", "low"]:
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # ensure priority tag matches configured tags (capitalized)
                pr = priority.capitalize()
                self.task_tree.insert("", tk.END, values=(task, pr, created_at, "Pending 🔴", category), tags=(pr,))
                self.task_var.set("")
            else:
                messagebox.showwarning("Invalid Input", "Please enter High, Mid, or Low.")
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

# method to delete a selected task
    def delete_task(self):
        selected_items = self.task_tree.selection()
        if selected_items:
            for item in selected_items:
                self.task_tree.delete(item)
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

# method to suggest category based on task content
    def suggest_category(task):
        task_lower = task.lower()
        if any(word in task_lower for word in ["email", "meeting", "report", "project", "deadline", "client"]):
            return "Work"
        elif any(word in task_lower for word in ["doctor", "exercise", "meditation", "health", "appointment"]):
            return "Health"
        elif any(word in task_lower for word in ["pay", "bill", "budget", "bank", "invoice", "salary"]):
            return "Finance"
        elif any(word in task_lower for word in ["call", "family", "friend", "party", "gift", "shopping"]):
            return "Personal"
        return "General"

# method to edit a selected task
    def edit_task(self):
        selected_items = self.task_tree.selection()
        if selected_items:
            item = selected_items[0]
            current_values = self.task_tree.item(item, "values")
            if len(current_values) == 5:
                current_task, current_priority, current_created, current_status, current_category = current_values
            else:
                messagebox.showerror("Error", "Task format is invalid.")
                return

            new_task = simpledialog.askstring("Edit Task", "Update the task:", initialvalue=current_task)
            new_priority = simpledialog.askstring("Edit Priority", "Update priority (High, Mid, Low):", initialvalue=current_priority)
            new_category = suggest_category(new_task) if new_task else current_category

            if new_task and new_priority and new_priority.lower() in ["high", "mid", "low"]:
                self.task_tree.item(item, values=(new_task, new_priority.capitalize(), current_created, current_status, new_category))
            else:
                messagebox.showwarning("Invalid Input", "Please enter valid task and priority.")
        else:
            messagebox.showwarning("Warning", "Please select a task to edit.")

# method to toggle task status between Pending and Done
    def toggle_status(self):
        selected_items = self.task_tree.selection()
        if selected_items:
            for item in selected_items:
                values = self.task_tree.item(item, "values")
                if len(values) == 5:
                    task, priority, created_at, status, category = values
                    new_status = "Done ✅" if "Pending" in status else "Pending 🔵"
                    self.task_tree.item(item, values=(task, priority, created_at, new_status, category))
                else:
                    messagebox.showerror("Error", "Task format is invalid.")
        else:
            messagebox.showwarning("Warning", "Please select a task to toggle status.")
            
# method to save tasks to a JSON file
    def save_tasks(self):
        tasks = [self.task_tree.item(child)["values"] for child in self.task_tree.get_children()]
        with open("tasks.json", "w") as f:
            json.dump({"tasks": tasks}, f, indent=2)
        messagebox.showinfo("Success", "Tasks saved successfully.")

# method to load tasks from a JSON file
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as f:
                    data = json.load(f)
                    tasks = data.get("tasks", [])
                    for task in tasks:
                        # normalize stored task formats into 5-field rows: Task, Priority, Created At, Status, Category
                        if isinstance(task, list):
                            row = task[:]  # copy
                        elif isinstance(task, str):
                            row = [task, "Mid"]
                        else:
                            continue
                        # pad or truncate to 5 fields
                        while len(row) < 5:
                            row.append("")
                        row = row[:5]
                        pr = row[1].capitalize() if row[1] else "Mid"
                        self.task_tree.insert("", tk.END, values=(row[0], pr, row[2], row[3], row[4]), tags=(pr,))
            except (json.JSONDecodeError, KeyError):
                messagebox.showerror("Error", "Failed to load tasks. File may be corrupted.")
        else:
            messagebox.showinfo("Info", "No saved tasks found.")

# method to sort tasks by priority
    def sort_by_priority(self):
        priority_order = {"High": 1, "Mid": 2, "Low": 3}
        rows = []
        for i in self.task_tree.get_children():
            vals = list(self.task_tree.item(i)["values"])
            while len(vals) < 5:
                vals.append("")
            task, pr, created_at, status, category = vals
            pr_key = priority_order.get(pr, 99)
            rows.append((pr_key, task, pr, created_at, status, category))
        rows.sort()
        # clear and reinsert in sorted order
        for i in self.task_tree.get_children():
            self.task_tree.delete(i)
        for _, task, pr, created_at, status, category in rows:
            self.task_tree.insert("", tk.END, values=(task, pr, created_at, status, category), tags=(pr,))

# running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoList(root)
    root.mainloop()