import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# File Handler
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Code Parser
def split_into_lines(code):
    return code.split('\n')

# Rule Checker
def check_line_length(line, max_length=100):
    return len(line) <= max_length

def check_indentation(line, indent_size=4):
    if not line.strip():  # Ignore empty lines
        return True
    indent = len(line) - len(line.lstrip())
    return indent % indent_size == 0 or '\t' in line[:indent]

def check_trailing_whitespace(line):
    return not line.rstrip().endswith(' ')

def apply_rules(lines, indent_size):
    issues = []
    for i, line in enumerate(lines, 1):
        if not check_line_length(line):
            issues.append(f"Line {i}: Too long (exceeds 80 characters)")
        if not check_indentation(line, indent_size):
            issues.append(f"Line {i}: Incorrect indentation")
        if not check_trailing_whitespace(line):
            issues.append(f"Line {i}: Trailing whitespace")
    return issues

# Report Generator
def generate_report(file_path, issues):
    if not issues:
        return f"No issues found in {file_path}"
    
    report = f"Code Review Report for {file_path}\n"
    report += "=" * 40 + "\n"
    for issue in issues:
        report += f"- {issue}\n"
    return report

# Main function
def review_code(file_path, indent_size):
    code = read_file(file_path)
    lines = split_into_lines(code)
    issues = apply_rules(lines, indent_size)
    report = generate_report(file_path, issues)
    return report

# GUI
class CodeReviewerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Code Reviewer")
        master.geometry("600x450")

        self.label = tk.Label(master, text="Select a file to review:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.indent_label = tk.Label(master, text="Indentation size:")
        self.indent_label.pack()
        self.indent_var = tk.StringVar(value="4")
        self.indent_entry = tk.Entry(master, textvariable=self.indent_var, width=5)
        self.indent_entry.pack()

        self.review_button = tk.Button(master, text="Review Code", command=self.review_code, state=tk.DISABLED)
        self.review_button.pack(pady=5)

        self.result_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20)
        self.result_area.pack(pady=10, padx=10)

        self.file_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if self.file_path:
            self.review_button['state'] = tk.NORMAL
            self.label.config(text=f"Selected file: {os.path.basename(self.file_path)}")

    def review_code(self):
        if self.file_path:
            try:
                indent_size = int(self.indent_var.get())
                report = review_code(self.file_path, indent_size)
                self.result_area.delete(1.0, tk.END)
                self.result_area.insert(tk.END, report)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for indentation size.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = CodeReviewerGUI(root)
    root.mainloop()