"""
Demo 03: Remote Method Invocation (RMI) with Pyro4 (Python Remote Objects)
==========================================================================

Demonstrates object-oriented remote method calls with Pyro4:
    - Exposing Python classes over the network using @Pyro4.expose
    - Registering remote objects with a Pyro Daemon and Name Server
    - Calling methods on remote objects transparently from a client
    - Chaining remote objects across multiple services

Run instructions:
    If Pyro4 is installed:
        pyro4-ns                          # Start Name Server in terminal 1
        python3 03_pyro4_remote_objects.py # Runs server & client
    Otherwise, running with `python3` executes a self-contained simulation.
"""

import time
import os

try:
    import Pyro4
    PYRO_AVAILABLE = True
except ImportError:
    PYRO_AVAILABLE = False


# ===================================================================
# 1. Defining the Remote Service Class
# ===================================================================

class ComputeService:
    """
    A service offering scientific calculation methods.
    When using Pyro4, decorated with @Pyro4.expose to allow remote access.
    """
    def __init__(self):
        self.call_count = 0

    def calculate_square(self, x):
        self.call_count += 1
        print(f"  [Server PID {os.getpid()}] calculate_square({x}) invoked! (Total calls: {self.call_count})")
        return x * x

    def get_service_stats(self):
        return {"pid": os.getpid(), "calls_served": self.call_count}


# ===================================================================
# Fallback Simulation: Transparent Proxy Pattern
# ===================================================================

class SimulatedRemoteProxy:
    """Simulates a Pyro4 Remote Proxy interacting with a remote server object."""

    def __init__(self, target_service, uri="PYRO:ComputeService@localhost:9090"):
        self._target = target_service
        self._uri = uri

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        if callable(attr):
            def remote_call(*args, **kwargs):
                print(f"  [Client Proxy] Serializing call: {name}{args} over {self._uri}...")
                time.sleep(0.2)  # simulate network round-trip latency
                result = attr(*args, **kwargs)
                print(f"  [Client Proxy] Deserialized return value: {result}")
                return result
            return remote_call
        return attr


# ===================================================================
# Demo Functions
# ===================================================================

def demo_remote_method_invocation():
    """
    Demonstrates calling methods on an object running in another process or machine.
    """
    print("=" * 60)
    print("Pyro4: Remote Method Invocation (RMI)")
    print("=" * 60)

    if PYRO_AVAILABLE:
        print("Genuine Pyro4 installed. Setting up daemon...")
        daemon = Pyro4.Daemon()
        uri = daemon.register(Pyro4.expose(ComputeService))
        print(f"Server ready. Object URI: {uri}")
        # In a real setup, client connects using:
        # proxy = Pyro4.Proxy(uri)
        # res = proxy.calculate_square(12)
    else:
        print("[Simulated Mode — Pyro4 not installed]")
        print("To install: pip install Pyro4")
        print("Architecture: [Client Proxy] =====(Network / TCP)=====> [Pyro Daemon -> Object]")
        print()

        # Create simulated remote service instance
        server_instance = ComputeService()
        client_proxy = SimulatedRemoteProxy(server_instance)

        print("[Client] Calling calculate_square(12) on remote proxy:")
        val1 = client_proxy.calculate_square(12)
        print(f"[Client] Result from remote object: {val1}\n")

        print("[Client] Calling calculate_square(25) on remote proxy:")
        val2 = client_proxy.calculate_square(25)
        print(f"[Client] Result from remote object: {val2}\n")

        stats = client_proxy.get_service_stats()
        print(f"[Client] Remote service statistics: {stats}\n")


def demo_pyro_chaining():
    """
    Demonstrates Chaining Objects with Pyro4:
    Client calls Service A, which internally forwards or chains requests
    to Service B and Service C before returning the final result.
    """
    print("=" * 60)
    print("Chaining Remote Objects with Pyro4")
    print("=" * 60)
    print("Flow: [Client] ---> [Service A: Parser] ---> [Service B: Model] ---> [Service C: Storage]")
    print()
    print("Code Pattern:")
    print("  # Inside Service A:")
    print("  class Aggregator:")
    print("      def process(self, data):")
    print("          model = Pyro4.Proxy('PYRONAME:ai.model')")
    print("          refined = model.predict(data)")
    print("          storage = Pyro4.Proxy('PYRONAME:db.storage')")
    print("          return storage.save(refined)")
    print()
    print("This pattern enables microservice-style distributed workflows in pure Python.\n")


# ===================================================================
# Main: uncomment one function at a time to demonstrate progressively
# ===================================================================

def main():
    demo_remote_method_invocation()
    # demo_pyro_chaining()


if __name__ == "__main__":
    main()
