from redring.scanners.dummy import DummyScanner
from redring.core.registry import ScannerRegistry


print("=== Registered Scanners ===")
print(ScannerRegistry.list())


print("\n=== Getting Dummy Scanner ===")
scanner_cls = ScannerRegistry.get("dummy.test")

if scanner_cls is None:
    raise RuntimeError("Dummy scanner was not registered!")


print(scanner_cls)


print("\n=== Creating Scanner ===")
scanner = scanner_cls()

print(scanner)


print("\n=== Running Scan ===")
result = scanner.scan()

print(result)