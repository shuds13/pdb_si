# pdb_si.py — pdb fork adding "si" (step into next call)
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
        # Find function name from current line
        frame = self.curframe
        with open(frame.f_code.co_filename, 'r') as f:
            lines = f.readlines()
            line = lines[frame.f_lineno - 1].strip()
            if '(' in line:
                func_name = line.split('(')[0].split()[-1]
                # Find function line and set breakpoint
                for i, l in enumerate(lines, 1):
                    if l.strip().startswith(f'def {func_name}('):
                        self._si_mode = True  # Mark that we're in si mode
                        self.set_break(frame.f_code.co_filename, i + 1, temporary=True)
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
