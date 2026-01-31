import signal
import subprocess
import sys
import re

def main():
    print("Starting solver...", flush=True)
    # Block SIGALRM to bypass the 1ms timeout in readflag
    signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])

    try:
        # Run the target binary
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
        
        print(f"Raw output:\n{buffer}", flush=True)

        # Extract the math expression
        # Example: "(((((123)+(456))...input your answer:"
        match = re.search(r'(\((\((\(123\)+(456))\)).*?\))', buffer, re.DOTALL)
        if match:
            expression = match.group(1)
            print(f"Evaluating: {expression}", flush=True)
            answer = eval(expression)
            print(f"Calculated Answer: {answer}", flush=True)

            # Send the answer
            p.stdin.write(f"{answer}\n")
            p.stdin.flush()

            # Read the rest of the output (the flag)
            result = p.stdout.read()
            print(f"Final Output:\n{result}", flush=True)
        else:
            print("Could not find math expression", flush=True)

    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    main()
