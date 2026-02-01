import os
import signal
import subprocess
import time
import sys
import re

def log(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stdout.write(f"{msg}\n")
    try:
        with open("/tmp/solver.log", "a") as f:
            f.write(f"{msg}\n")
    except:
        pass

def solve():
    log("[*] SOLVER STARTED")
    try:
        # Check environment
        log(f"[*] ENV: {os.environ}")
        
        # 1. Block SIGALRM
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
            log("[*] SIGALRM blocked successfully")
        except AttributeError:
            log("[!] signal.pthread_sigmask not available, trying signal.signal")
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
            log("[!] Empty output from /readflag. Sandbox active?")
            # Try to list files to confirm sandbox
            try:
                log(f"[*] LS /: {os.listdir('/')}")
            except Exception as e:
                log(f"[!] LS failed: {e}")
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
            log(f"[+] FLAG: {flag}")
            print(f"FLAG_IS_HERE: {flag}")
        else:
            log("[!] No equation found")

        process.wait()

    except Exception as e:
        log(f"[!] Error: {e}")

if __name__ == "__main__":
    solve()