"""
pdb extension adding "si" (step into next call).

Skips function argument lines and steps directly into function bodies.
"""
import sys, pdb as _pdb
import os

class Pdb(_pdb.Pdb):
    def __init__(self, *a, **k):
        skip = set(k.pop("skip", [])).union({__name__, "_pdb", "pdb", "bdb"})
        super().__init__(*a, skip=list(skip), **k)
        # SH TODO - make message suppression threadsafe
        self._si_mode = False  # Deleted breakpoint message suppression

    def do_si(self, arg=None):
        """si: step directly into the next Python call (skip caller arg lines)."""
        frame = self.curframe
        with open(frame.f_code.co_filename, 'r') as f:
            lines = f.readlines()
            line = lines[frame.f_lineno - 1].strip()
            if '(' in line:
                func_name = line.split('(')[0].split()[-1]
                
                # Try to find function in any loaded module
                for module in sys.modules.values():
                    if hasattr(module, func_name):
                        func = getattr(module, func_name)
                        if hasattr(func, '__code__'):
                            filename = func.__code__.co_filename
                            lineno = func.__code__.co_firstlineno
                            self._si_mode = True
                            self.set_break(filename, lineno + 1, temporary=True)
                            self.set_continue()
                            return 1
        return 0

    def message(self, msg):
        """Suppress breakpoint deletion messages from si command"""
        if "Deleted breakpoint" in msg and self._si_mode:
            self._si_mode = False
            return
        super().message(msg)

def set_trace(frame=None):
    if frame is None:
        frame = sys._getframe().f_back
    Pdb().set_trace(frame)

# Monkey-patch the real pdb module if environment variable is set
if 'PDB_EXTENSION' in os.environ:
    # Force reload of pdb module to ensure our patching works
    if 'pdb' in sys.modules:
        del sys.modules['pdb']
    import pdb
    pdb.Pdb = Pdb
    pdb.set_trace = set_trace
