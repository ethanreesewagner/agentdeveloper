import config  # This sets the OPENAI_API_KEY environment variable
import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from agents import code_agent

def format_agent_response(response_text):
    from agents import convert_latex_to_unicode
    return convert_latex_to_unicode(response_text)

class InputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Agent Input GUI")
        self.root.geometry("800x600")
        self.input_data = {}
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Agent Input Interface", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Text Input Section
        ttk.Label(main_frame, text="Input:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(main_frame, width=70, height=8, wrap=tk.WORD, font=("Arial", 20))
        self.text_input.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Run Button
        run_button = ttk.Button(main_frame, text="Run", command=self.run_agent, style="Accent.TButton")
        run_button.grid(row=3, column=0, pady=(0, 20))
        
        # Agent Response Section
        ttk.Label(main_frame, text="Response:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        self.response_text = scrolledtext.ScrolledText(main_frame, width=70, height=12, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 20))
        self.response_text.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def run_agent(self):
        """Run the agent with the input text"""
        try:
            # Get input text
            text_content = self.text_input.get("1.0", tk.END).strip()
            
            # Validate input
            if not text_content:
                messagebox.showwarning("Input Required", "Please enter some text.")
                return
            
            # Build the prompt for the agent (with all options enabled)
            prompt = self.build_agent_prompt(text_content)
            
            # Update status
            self.status_var.set("Running agent...")
            self.root.update()
            
            # Run agent in a separate thread to avoid blocking the GUI
            threading.Thread(target=self.execute_agent, args=(prompt,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error preparing input: {str(e)}")
            self.status_var.set("Error occurred")
    
    def build_agent_prompt(self, text_content):
        """Build a comprehensive prompt for the agent with all options enabled"""
        prompt = f"User Request:\n{text_content}\n\n"
        prompt += "Options (all enabled by default):\n"
        prompt += "- generate_code: True\n"
        prompt += "- run_flask: True\n"
        prompt += "- launch_tkinter: True\n"
        prompt += "- project_type: python\n\n"
        prompt += "Please process this request and provide appropriate code, explanations, or actions."
        
        return prompt
    
    def execute_agent(self, prompt):
        """Execute the agent with the given prompt"""
        try:
            # Clear previous response
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", "Agent is processing your request...\n")
            self.response_text.config(state=tk.DISABLED)
            self.root.update()
            
            # Run the agent with streaming
            from swarm import Swarm
            client = Swarm()
            
            message = {"role": "user", "content": prompt}
            
            # Use streaming to get real-time updates
            response_stream = client.run_and_stream(
                agent=code_agent,
                messages=[message],
                execute_tools=True,
            )
            
            # Clear the "processing" message
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete("1.0", tk.END)
            self.response_text.config(state=tk.DISABLED)
            
            # Process the streaming response
            full_response = ""
            for chunk in response_stream:
                if hasattr(chunk, 'content') and chunk.content:
                    # Update the response text with each chunk
                    self.response_text.config(state=tk.NORMAL)
                    self.response_text.insert(tk.END, chunk.content)
                    self.response_text.see(tk.END)  # Auto-scroll to bottom
                    self.response_text.config(state=tk.DISABLED)
                    self.root.update()  # Force GUI update
                    full_response += chunk.content
                elif hasattr(chunk, 'messages') and chunk.messages:
                    # Handle tool calls or other message types
                    for msg in chunk.messages:
                        if msg.get('content'):
                            self.response_text.config(state=tk.NORMAL)
                            self.response_text.insert(tk.END, msg['content'])
                            self.response_text.see(tk.END)
                            self.response_text.config(state=tk.DISABLED)
                            self.root.update()
                            full_response += msg['content']
            
            # If no streaming content was received, try to get the final response
            if not full_response.strip():
                # Fallback to non-streaming approach
                response = client.run(
                    agent=code_agent,
                    messages=[message],
                    execute_tools=True,
                )
                
                if response.messages and len(response.messages) > 1:
                    agent_response = response.messages[-1].get("content", "No response from agent")
                else:
                    agent_response = "Agent processed the request but didn't provide a text response."
                
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

def main():
    root = tk.Tk()
    app = InputGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()