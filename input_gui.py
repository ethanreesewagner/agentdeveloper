#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import sys
import threading

# Add the current directory to path to import agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents import code_agent

class InputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Agent Input GUI")
        self.root.geometry("800x700")
        
        # Store input data
        self.input_data = {}
        
        # Create main frame with scrollbar
        main_canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
        self.main_frame = ttk.Frame(main_canvas)
        
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Agent Input Interface", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        # Text Input Section
        ttk.Label(self.main_frame, text="Text Input:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(self.main_frame, width=60, height=6, wrap=tk.WORD)
        self.text_input.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # File Selection Section
        ttk.Label(self.main_frame, text="File Selection:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        file_frame = ttk.Frame(self.main_frame)
        file_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(0, weight=1)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.grid(row=0, column=1)
        
        # Options Section
        ttk.Label(self.main_frame, text="Options:", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        options_frame = ttk.Frame(self.main_frame)
        options_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Checkboxes
        self.option1_var = tk.BooleanVar()
        self.option2_var = tk.BooleanVar()
        self.option3_var = tk.BooleanVar()
        
        ttk.Checkbutton(options_frame, text="Generate Code", variable=self.option1_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Run Flask Server", variable=self.option2_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Checkbutton(options_frame, text="Launch Tkinter GUI", variable=self.option3_var).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Dropdown
        ttk.Label(options_frame, text="Project Type:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.project_type_var = tk.StringVar(value="python")
        project_combo = ttk.Combobox(options_frame, textvariable=self.project_type_var, 
                                   values=["python", "flask", "tkinter", "web", "data_analysis"])
        project_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Agent Response Section
        ttk.Label(self.main_frame, text="Agent Response:", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky=tk.W, pady=(20, 5))
        
        self.response_text = scrolledtext.ScrolledText(self.main_frame, width=60, height=8, wrap=tk.WORD, state=tk.DISABLED)
        self.response_text.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Action Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        submit_button = ttk.Button(button_frame, text="Submit to Agent", command=self.submit_to_agent)
        submit_button.grid(row=0, column=0, padx=(0, 10))
        
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_input)
        clear_button.grid(row=0, column=1, padx=(0, 10))
        
        save_button = ttk.Button(button_frame, text="Save Config", command=self.save_config)
        save_button.grid(row=0, column=2, padx=(0, 10))
        
        load_button = ttk.Button(button_frame, text="Load Config", command=self.load_config)
        load_button.grid(row=0, column=3, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure scrolling
        self.main_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        
    def browse_file(self):
        """Open file dialog for file selection"""
        filename = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("Python files", "*.py"),
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.file_path_var.set(filename)
            self.status_var.set(f"File selected: {os.path.basename(filename)}")
    
    def submit_to_agent(self):
        """Submit input to the agent and display response"""
        try:
            # Collect input data
            text_content = self.text_input.get("1.0", tk.END).strip()
            file_path = self.file_path_var.get().strip()
            
            options = {
                "generate_code": self.option1_var.get(),
                "run_flask": self.option2_var.get(),
                "launch_tkinter": self.option3_var.get(),
                "project_type": self.project_type_var.get()
            }
            
            # Validate input
            if not text_content and not file_path:
                messagebox.showwarning("Input Required", "Please provide text input or select a file.")
                return
            
            # Build the prompt for the agent
            prompt = self.build_agent_prompt(text_content, file_path, options)
            
            # Update status
            self.status_var.set("Sending to agent...")
            self.root.update()
            
            # Run agent in a separate thread to avoid blocking the GUI
            threading.Thread(target=self.run_agent, args=(prompt,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error preparing input: {str(e)}")
            self.status_var.set("Error occurred")
    
    def build_agent_prompt(self, text_content, file_path, options):
        """Build a comprehensive prompt for the agent"""
        prompt = "User Request:\n"
        
        if text_content:
            prompt += f"{text_content}\n\n"
        
        if file_path:
            prompt += f"File to work with: {file_path}\n\n"
        
        prompt += "Options:\n"
        for key, value in options.items():
            prompt += f"- {key}: {value}\n"
        
        prompt += "\nPlease process this request and provide appropriate code, explanations, or actions."
        
        return prompt
    
    def run_agent(self, prompt):
        """Run the agent with the given prompt"""
        try:
            # Clear previous response
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", "Agent is processing your request...\n")
            self.response_text.config(state=tk.DISABLED)
            self.root.update()
            
            # Run the agent
            from swarm import Swarm
            client = Swarm()
            
            message = {"role": "user", "content": prompt}
            response = client.run(
                agent=code_agent,
                messages=[message],
                execute_tools=True,
            )
            
            # Get the agent's response
            if response.messages and len(response.messages) > 1:
                agent_response = response.messages[-1].get("content", "No response from agent")
            else:
                agent_response = "Agent processed the request but didn't provide a text response."
            
            # Update the response text
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", agent_response)
            self.response_text.config(state=tk.DISABLED)
            
            # Update status
            self.status_var.set("Agent response received")
            
        except Exception as e:
            error_msg = f"Error running agent: {str(e)}"
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", f"ERROR: {error_msg}")
            self.response_text.config(state=tk.DISABLED)
            self.status_var.set("Error occurred")
    
    def submit_input(self):
        """Collect all input data and process it (legacy function)"""
        try:
            # Collect text input
            text_content = self.text_input.get("1.0", tk.END).strip()
            
            # Collect file path
            file_path = self.file_path_var.get().strip()
            
            # Collect options
            options = {
                "generate_code": self.option1_var.get(),
                "run_flask": self.option2_var.get(),
                "launch_tkinter": self.option3_var.get(),
                "project_type": self.project_type_var.get()
            }
            
            # Validate input
            if not text_content and not file_path:
                messagebox.showwarning("Input Required", "Please provide text input or select a file.")
                return
            
            # Store input data
            self.input_data = {
                "text_input": text_content,
                "file_path": file_path,
                "options": options,
                "timestamp": "now"
            }
            
            # Display collected data
            self.show_input_summary()
            
            self.status_var.set("Input submitted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing input: {str(e)}")
            self.status_var.set("Error occurred")
    
    def show_input_summary(self):
        """Show a summary of the collected input data"""
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Input Summary")
        summary_window.geometry("500x400")
        
        # Create scrolled text widget
        text_widget = scrolledtext.ScrolledText(summary_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Format and display the data
        summary_text = "INPUT SUMMARY:\n" + "="*50 + "\n\n"
        
        if self.input_data["text_input"]:
            summary_text += f"TEXT INPUT:\n{self.input_data['text_input']}\n\n"
        
        if self.input_data["file_path"]:
            summary_text += f"FILE PATH:\n{self.input_data['file_path']}\n\n"
        
        summary_text += f"OPTIONS:\n"
        for key, value in self.input_data["options"].items():
            summary_text += f"  {key}: {value}\n"
        
        text_widget.insert("1.0", summary_text)
        text_widget.config(state=tk.DISABLED)
    
    def clear_input(self):
        """Clear all input fields"""
        self.text_input.delete("1.0", tk.END)
        self.file_path_var.set("")
        self.option1_var.set(False)
        self.option2_var.set(False)
        self.option3_var.set(False)
        self.project_type_var.set("python")
        self.input_data = {}
        
        # Clear response
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.config(state=tk.DISABLED)
        
        self.status_var.set("All inputs cleared")
    
    def save_config(self):
        """Save current configuration to a JSON file"""
        try:
            config_data = {
                "text_input": self.text_input.get("1.0", tk.END).strip(),
                "file_path": self.file_path_var.get(),
                "options": {
                    "generate_code": self.option1_var.get(),
                    "run_flask": self.option2_var.get(),
                    "launch_tkinter": self.option3_var.get(),
                    "project_type": self.project_type_var.get()
                }
            }
            
            filename = filedialog.asksaveasfilename(
                title="Save Configuration",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(config_data, f, indent=2)
                self.status_var.set(f"Configuration saved to {os.path.basename(filename)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving configuration: {str(e)}")
    
    def load_config(self):
        """Load configuration from a JSON file"""
        try:
            filename = filedialog.askopenfilename(
                title="Load Configuration",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r') as f:
                    config_data = json.load(f)
                
                # Restore text input
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", config_data.get("text_input", ""))
                
                # Restore file path
                self.file_path_var.set(config_data.get("file_path", ""))
                
                # Restore options
                options = config_data.get("options", {})
                self.option1_var.set(options.get("generate_code", False))
                self.option2_var.set(options.get("run_flask", False))
                self.option3_var.set(options.get("launch_tkinter", False))
                self.project_type_var.set(options.get("project_type", "python"))
                
                self.status_var.set(f"Configuration loaded from {os.path.basename(filename)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading configuration: {str(e)}")

def main():
    root = tk.Tk()
    app = InputGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 