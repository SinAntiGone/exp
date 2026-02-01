import os
import signal
import subprocess
import time
import sys
import re

def log(msg):
    # Try all output channels
    try:
        sys.stderr.write(f"{msg}\n")
        sys.stderr.flush()
    except: pass
    
    try:
        sys.stdout.write(f"{msg}\n")
        sys.stdout.flush()
    except: pass

    try:
        with open("/dev/tty", "w") as f:
            f.write(f"{msg}\n")
    except: pass

def solve():
    log("[*] SOLVER STARTED - V2")
    try:
        # 1. Block SIGALRM
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
            log("[*] SIGALRM blocked successfully")
        except AttributeError:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)

        # 2. Start /readflag
        log("[*] Starting /readflag")
        process = subprocess.Popen(
            ["/readflag"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )

        # 3. Read Challenge
        output = ""
        while True:
            char = process.stdout.read(1)
            if not char:
                break
            output += char
            if "=" in output and "?" in output:
                break
        
        log(f"[*] Output: {output}")

        if not output:
            log("[!] Empty output")
            return

        # 4. Parse and Solve
        match = re.search(r'(\d+(?:\s*[\+\-\*\/]\s*\d+)+)\s*=\s*\?', output)
        if match:
            expression = match.group(1)
            log(f"[*] Solving: {expression}")
            result = int(eval(expression))
            log(f"[*] Result: {result}")
            
            process.stdin.write(f"{result}\n")
            process.stdin.flush()
            
            flag = process.stdout.read()
            # BOMBASTIC OUTPUT
            for i in range(10):
                log(f"\n\n[+] FLAG: {flag}\n\n")
                time.sleep(0.1)
        else:
            log("[!] No equation found")

        process.wait()

    except Exception as e:
        log(f"[!] Error: {e}")

if __name__ == "__main__":
    solve()