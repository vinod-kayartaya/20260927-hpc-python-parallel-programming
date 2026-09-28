"""
Demo 04: Remote Procedure Calls (RPyC) and Communicating Sequential Processes (PyCSP)
=====================================================================================

Demonstrates two distinct distributed paradigms:
    - RPyC (Remote Python Call): Transparent, symmetric RPC library allowing remote Python access
    - PyCSP (Communicating Sequential Processes): Concurrency via synchronous / buffered channels
      (Tony Hoare's CSP model, similar to Go channels)

Uncomment one function at a time in main() to demonstrate progressively.
"""

import time
import os
import queue
import threading

# ===================================================================
# 1. RPyC: Remote Python Call
# ===================================================================

class TimeService:
    """A service that exposes methods over RPyC."""
    def exposed_get_server_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def exposed_remote_eval(self, expression):
        # Exposes safe mathematical evaluation on the remote host
        return eval(expression, {"__builtins__": {}}, {"abs": abs, "pow": pow})


def demo_rpyc():
    """
    Demonstrates RPyC:
    RPyC (Remote Python Call) transparently mirrors objects between processes.
    Methods prefixed with 'exposed_' are callable by remote clients.
    """
    print("=" * 60)
    print("RPyC: Transparent Remote Procedure Call")
    print("=" * 60)

    print("Architecture: Client connects to RPyC Server via TCP socket.")
    print("Methods starting with 'exposed_' can be called remotely.\n")

    # Simulation of RPyC client interaction
    service = TimeService()
    print("[Client] Invoking exposed_get_server_time() on remote service...")
    server_time = service.exposed_get_server_time()
    print(f"  -> Server Time: {server_time}")

    expr = "pow(2, 16)"
    print(f"\n[Client] Invoking exposed_remote_eval('{expr}') on remote service...")
    eval_res = service.exposed_remote_eval(expr)
    print(f"  -> Evaluated on Server: {eval_res}\n")


# ===================================================================
# 2. Communicating Sequential Processes (PyCSP)
# ===================================================================

class Channel:
    """
    Simulates a CSP (Communicating Sequential Processes) Channel.
    In CSP, processes communicate ONLY by passing messages over channels.
    No shared memory. No locks.
    """
    def __init__(self, buffer_size=0):
        self._q = queue.Queue(maxsize=buffer_size)

    def write(self, val):
        self._q.put(val)

    def read(self):
        return self._q.get()


def csp_producer(channel, count):
    """A sequential process that generates values into a channel."""
    for i in range(count):
        val = f"sensor-reading-{i*10}"
        print(f"  [Producer PID {os.getpid()}] writing to channel -> '{val}'")
        channel.write(val)
        time.sleep(0.1)
    channel.write(None)  # poison pill / end of stream


def csp_consumer(channel):
    """A sequential process that consumes values from a channel."""
    while True:
        msg = channel.read()
        if msg is None:
            print("  [Consumer] Received stop signal from channel.")
            break
        print(f"  [Consumer] Read from channel -> '{msg}'")


def demo_csp():
    """
    Demonstrates Communicating Sequential Processes (CSP):
    Processes are independent sequential threads; they coordinate exclusively
    by reading and writing to channels.
    """
    print("=" * 60)
    print("PyCSP: Communicating Sequential Processes (Channel-based)")
    print("=" * 60)
    print("Core Concept: 'Do not communicate by sharing memory; instead, share memory by communicating.'")
    print()

    chan = Channel(buffer_size=2)

    t_prod = threading.Thread(target=csp_producer, args=(chan, 4))
    t_cons = threading.Thread(target=csp_consumer, args=(chan,))

    t_cons.start()
    t_prod.start()

    t_prod.join()
    t_cons.join()
    print("\nCSP demonstration completed.\n")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_rpyc()
    # demo_csp()


if __name__ == "__main__":
    main()
