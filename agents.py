import os
import re
import subprocess
import time
from swarm import Agent

def convert_latex_to_unicode(text):
    """
    Convert LaTeX-style mathematical expressions to Unicode characters.
    """
    # Dictionary of LaTeX to Unicode conversions
    latex_to_unicode = {
        r'\pi': 'π',
        r'\alpha': 'α',
        r'\beta': 'β',
        r'\gamma': 'γ',
        r'\delta': 'δ',
        r'\epsilon': 'ε',
        r'\zeta': 'ζ',
        r'\eta': 'η',
        r'\theta': 'θ',
        r'\iota': 'ι',
        r'\kappa': 'κ',
        r'\lambda': 'λ',
        r'\mu': 'μ',
        r'\nu': 'ν',
        r'\xi': 'ξ',
        r'\omicron': 'ο',
        r'\rho': 'ρ',
        r'\sigma': 'σ',
        r'\tau': 'τ',
        r'\upsilon': 'υ',
        r'\phi': 'φ',
        r'\chi': 'χ',
        r'\psi': 'ψ',
        r'\omega': 'ω',
        r'\Gamma': 'Γ',
        r'\Delta': 'Δ',
        r'\Theta': 'Θ',
        r'\Lambda': 'Λ',
        r'\Xi': 'Ξ',
        r'\Pi': 'Π',
        r'\Sigma': 'Σ',
        r'\Phi': 'Φ',
        r'\Psi': 'Ψ',
        r'\Omega': 'Ω',
        r'\infty': '∞',
        r'\approx': '≈',
        r'\leq': '≤',
        r'\geq': '≥',
        r'\neq': '≠',
        r'\pm': '±',
        r'\times': '×',
        r'\div': '÷',
        r'\cdot': '·',
        r'\sqrt': '√',
        r'\sum': '∑',
        r'\prod': '∏',
        r'\int': '∫',
        r'\partial': '∂',
        r'\nabla': '∇',
        r'\in': '∈',
        r'\notin': '∉',
        r'\subset': '⊂',
        r'\supset': '⊃',
        r'\cup': '∪',
        r'\cap': '∩',
        r'\emptyset': '∅',
        r'\forall': '∀',
        r'\exists': '∃',
        r'\neg': '¬',
        r'\land': '∧',
        r'\lor': '∨',
        r'\rightarrow': '→',
        r'\leftarrow': '←',
        r'\leftrightarrow': '↔',
        r'\Rightarrow': '⇒',
        r'\Leftarrow': '⇐',
        r'\Leftrightarrow': '⇔',
        r'\ldots': '…',
        r'\cdots': '⋯',
        r'\vdots': '⋮',
        r'\ddots': '⋱',
        # Trigonometric functions
        r'\sin': 'sin',
        r'\cos': 'cos',
        r'\tan': 'tan',
        r'\csc': 'csc',
        r'\sec': 'sec',
        r'\cot': 'cot',
        r'\arcsin': 'arcsin',
        r'\arccos': 'arccos',
        r'\arctan': 'arctan',
        # Logarithmic functions
        r'\log': 'log',
        r'\ln': 'ln',
        # Other common functions
        r'\exp': 'exp',
        r'\lim': 'lim',
        r'\max': 'max',
        r'\min': 'min',
        r'\sup': 'sup',
        r'\inf': 'inf',
        r'\arg': 'arg',
        r'\deg': 'deg',
        r'\dim': 'dim',
        r'\ker': 'ker',
        r'\det': 'det',
        r'\tr': 'tr',
        r'\rank': 'rank',
        r'\null': 'null',
        r'\range': 'range',
        r'\domain': 'domain',
        r'\codomain': 'codomain',
        r'\image': 'image',
        r'\preimage': 'preimage',
        r'\kernel': 'kernel',
        r'\cokernel': 'cokernel',
        r'\im': 'im',
        r'\re': 're',
        r'\mod': 'mod',
        r'\bmod': 'mod',
        r'\pmod': 'mod',
        r'\gcd': 'gcd',
        r'\lcm': 'lcm',
        r'\floor': '⌊',
        r'\ceil': '⌈',
        r'\abs': '|',
        r'\norm': '||',
        r'\angle': '∠',
        r'\measuredangle': '∡',
        r'\sphericalangle': '∢',
        r'\triangle': '△',
        r'\square': '□',
        r'\circle': '○',
        r'\diamond': '◇',
        r'\star': '★',
        r'\bullet': '•',
        r'\circ': '∘',
        r'\bigcirc': '○',
        r'\bigtriangleup': '△',
        r'\bigtriangledown': '▽',
        r'\triangleleft': '◁',
        r'\triangleright': '▷',
        r'\bigstar': '★',
        r'\clubsuit': '♣',
        r'\diamondsuit': '♦',
        r'\heartsuit': '♥',
        r'\spadesuit': '♠',
    }
    
    # First, handle display math blocks \[ ... \]
    def replace_display_math(match):
        content = match.group(1)
        # Convert LaTeX expressions within the display math
        for latex, unicode_char in latex_to_unicode.items():
            content = content.replace(latex, unicode_char)
        # Handle superscripts and subscripts
        content = re.sub(r'\^\\pi', '^π', content)
        content = re.sub(r'\^\\e', '^e', content)
        content = re.sub(r'_\\pi', '_π', content)
        content = re.sub(r'_\\e', '_e', content)
        return content
    
    # Replace display math blocks
    text = re.sub(r'\\\[(.*?)\\\]', replace_display_math, text, flags=re.DOTALL)
    
    # Handle inline math \( ... \)
    def replace_inline_math(match):
        content = match.group(1)
        # Convert LaTeX expressions within the inline math
        for latex, unicode_char in latex_to_unicode.items():
            content = content.replace(latex, unicode_char)
        # Handle superscripts and subscripts
        content = re.sub(r'\^\\pi', '^π', content)
        content = re.sub(r'\^\\e', '^e', content)
        content = re.sub(r'_\\pi', '_π', content)
        content = re.sub(r'_\\e', '_e', content)
        return content
    
    # Replace inline math blocks
    text = re.sub(r'\\\((.*?)\\\)', replace_inline_math, text, flags=re.DOTALL)
    
    # Convert any remaining LaTeX expressions outside of math blocks
    for latex, unicode_char in latex_to_unicode.items():
        text = text.replace(latex, unicode_char)
    
    # Handle remaining superscripts and subscripts
    text = re.sub(r'\^\\pi', '^π', text)
    text = re.sub(r'\^\\e', '^e', text)
    text = re.sub(r'_\\pi', '_π', text)
    text = re.sub(r'_\\e', '_e', text)
    
    return text

def generate_code(file_name,code,project,readme=None):
    """
    Creates a file with the specified name and writes the provided code to it within the given project directory
    under 'agent_workspace'. Optionally, if a README content is provided, it writes it to a README file in the same
    directory. Returns the absolute path to the generated code file.

    Args:
        file_name (str): The name of the file to create (e.g., 'main.py').
        code (str): The code content to write into the file.
        project (str): The project directory name under 'agent_workspace'. Defaults to 'project_name'.
        readme (str, optional): Content for a README file. If provided, a README file will be created.

    Returns:
        str: The absolute path to the generated code file.
    
    Remember to use 127.0.0.1 and NOT localhost as the server url for the flask server.
    """
    print("generate_code tool is called")
    os.makedirs("agent_workspace/"+project,exist_ok=True)
    file=open("agent_workspace/"+project+"/"+file_name,"w")
    print(file_name)
    file.write(code)
    print(code)
    if readme:
        readme_file=open("agent_workspace/"+project+"/"+readme,"w")
        readme_file.write(readme)
        readme_file.close()
    file_path = os.path.abspath(file_name)
    print(file_path)
    file.close()
    return file_path

def execute_code(file_path):
    """
    Execute the code in the given file and return the output.
    """
    print("execute_code tool is called")
    output=os.popen(f"python {file_path}").read()
    print(output)
    return output

def format_math_output(text):
    """
    Format mathematical output by converting LaTeX expressions to Unicode.
    """
    return convert_latex_to_unicode(text)

def run_flask_server(file_path, port=5000):
    """
    Run a Flask server from the given Python file as a background process.
    Returns the process ID and the server URL.
    """
    print("run_flask_server tool is called")
    # Run the Flask app as a background process
    # Assumes the Flask app uses `if __name__ == '__main__': app.run(port=port)`
    process = subprocess.Popen([
        'python3', file_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    url = f"http://127.0.0.1:{port}"
    print(f"Flask server started with PID {process.pid} at {url}")
    return {"pid": process.pid, "url": url}

def run_tkinter(file_path):
    """
    Run a Tkinter GUI Python program as a background process.
    Returns the process ID.
    """
    print("run_tkinter tool is called")
    print(f"Attempting to run Tkinter app: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return {"error": f"File not found: {file_path}"}
    
    # On macOS, try to run with specific environment variables to handle display issues
    env = os.environ.copy()
    
    # Set environment variables that might help with macOS GUI permissions
    env['PYTHONPATH'] = os.getcwd()
    env['DISPLAY'] = ':0'  # For X11 compatibility
    
    try:
        # Run Tkinter without redirecting stdout/stderr to allow GUI to open
        process = subprocess.Popen([
            'python3', file_path
        ], env=env)
        
        print(f"Tkinter program started with PID {process.pid}")
        print("Note: On macOS, you may need to grant accessibility permissions to Terminal/your IDE")
        print("Go to System Preferences > Security & Privacy > Privacy > Accessibility")
        print("and add Terminal (or your IDE) to the list of allowed apps.")
        
        return {"pid": process.pid, "status": "started", "note": "Check accessibility permissions if GUI doesn't appear"}
        
    except Exception as e:
        print(f"ERROR starting Tkinter app: {e}")
        return {"error": str(e)}

def run_flask_with_tkinter(flask_file_path, tkinter_file_path, port=5000):
    """
    Run a Flask server and a Tkinter GUI, with the Tkinter app able to communicate with the Flask server.
    Flask server starts first, then Tkinter app starts after a delay to ensure Flask is ready.
    Returns the process IDs and the Flask server URL.
    """
    print("run_flask_with_tkinter tool is called")
    
    # Check if files exist
    if not os.path.exists(flask_file_path):
        print(f"ERROR: Flask file not found: {flask_file_path}")
        return {"error": f"Flask file not found: {flask_file_path}"}
    
    if not os.path.exists(tkinter_file_path):
        print(f"ERROR: Tkinter file not found: {tkinter_file_path}")
        return {"error": f"Tkinter file not found: {tkinter_file_path}"}
    
    # Start Flask server
    flask_proc = subprocess.Popen([
        'python3', flask_file_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    url = f"http://127.0.0.1:{port}"
    print(f"Flask server started with PID {flask_proc.pid} at {url}")
    
    # Wait for Flask server to start up before launching Tkinter
    print("Waiting for Flask server to start up...")
    time.sleep(3)  # Wait 3 seconds for Flask to initialize
    
    # Set up environment for Tkinter
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    env['DISPLAY'] = ':0'
    
    try:
        # Run Tkinter without redirecting stdout/stderr to allow GUI to open
        tkinter_proc = subprocess.Popen([
            'python3', tkinter_file_path
        ], env=env)
        
        print(f"Tkinter program started with PID {tkinter_proc.pid}")
        print("Note: On macOS, you may need to grant accessibility permissions to Terminal/your IDE")
        print("Go to System Preferences > Security & Privacy > Privacy > Accessibility")
        print("and add Terminal (or your IDE) to the list of allowed apps.")
        
        return {
            "flask_pid": flask_proc.pid, 
            "tkinter_pid": tkinter_proc.pid, 
            "flask_url": url,
            "status": "both started",
            "note": "Check accessibility permissions if Tkinter GUI doesn't appear"
        }
        
    except Exception as e:
        print(f"ERROR starting Tkinter app: {e}")
        return {"error": str(e), "flask_pid": flask_proc.pid, "flask_url": url}

def read_code_file(file_path):
    """
    Read and return the contents of a code file from agent_workspace.
    Args:
        file_path (str): Path to the file relative to agent_workspace.
    Returns:
        str: Contents of the file.
    """
    abs_path = os.path.join('agent_workspace', file_path)
    print(f"read_code_file tool is called for {abs_path}")
    if not os.path.exists(abs_path):
        return f"File not found: {file_path}"
    with open(abs_path, 'r') as f:
        return f.read()

def list_projects():
    """
    List all existing projects in agent_workspace.
    Returns:
        list: List of project directory names.
    """
    print("list_projects tool is called")
    if not os.path.exists('agent_workspace'):
        return []
    
    projects = []
    for item in os.listdir('agent_workspace'):
        item_path = os.path.join('agent_workspace', item)
        if os.path.isdir(item_path):
            projects.append(item)
    
    print(f"Found projects: {projects}")
    return projects

code_agent = Agent(
    name="Code Agent",
    instructions="""You are a helpful agent that generates python code and executes it. 

CRITICAL INSTRUCTION FOR MATHEMATICAL OUTPUT:
When you provide mathematical expressions in your responses, you MUST use the format_math_output function to convert LaTeX-style expressions to proper Unicode characters. 

Examples of what you should do:
- Instead of writing: "The result is \\(e^\\pi \\approx 23.1407\\)"
- Write: "The result is " + format_math_output("\\(e^\\pi \\approx 23.1407\\)")

- Instead of writing: "\\[\\sum_{n=1}^{10} (2n + 3)\\]"
- Write: "\\[\\sum_{n=1}^{10} (2n + 3)\\]" and then use format_math_output on it

This makes the output much more readable by converting expressions like \\(e^\\pi\\) to e^π.

ALWAYS use format_math_output() for any mathematical expressions in your responses.
You can also use the run_flask_server function to launch a Flask server from a Python file.
You can also use the generate_code function to generate a Python file and then use the run_flask_server function to launch a Flask server from the generated file.
You can also use the execute_code function to execute a Python file and return the output.
You can also use the format_math_output function to convert LaTeX-style expressions to proper Unicode characters.
In a flask server, you can write HTML,CSS,JavaScript,Python code, and use the run_flask_server function to execute the code and return the output.
You can also use the run_tkinter function to launch a Tkinter GUI Python program from a file.
You can also use the run_flask_with_tkinter function to launch both a Flask server and a Tkinter GUI, with the Tkinter app able to communicate with the Flask server. IMPORTANT: When using run_flask_with_tkinter, the Flask server starts first, then the Tkinter app starts after a delay to ensure the Flask server is ready to accept connections.
You can also use the read_code_file function to read the contents of an existing code file in agent_workspace, so you can inspect, modify, or extend existing code as needed.
You can also use the list_projects function to get a list of all existing projects in agent_workspace, so you can see what projects are available to work with.
""",
    functions=[generate_code, execute_code, format_math_output, run_flask_server, run_tkinter, run_flask_with_tkinter, read_code_file, list_projects]
)