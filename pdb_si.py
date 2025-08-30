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
            
            # Check if this might be a function call
            if '(' in line:
                # Get the call expression
                call_part = line.split('(')[0].strip()
                if '=' in call_part:
                    call_expr = call_part.split('=')[-1].strip()
                else:
                    call_expr = call_part
                
                # Try to evaluate as function call
                try:
                    func = eval(call_expr, frame.f_globals, frame.f_locals)
                    if callable(func):
                        return self._handle_callable(func, call_expr)
                except Exception:
                    # eval failed - not a function call
                    print("Not a function call")
                    return 0
            else:
                # No parentheses - definitely not a function call
                print("Not a function call")
                return 0
        
        return 0
    
    def _handle_callable(self, func, call_expr):
        """Handle different types of callable objects."""
        # Get the location from whatever Python gives us
        if hasattr(func, '__code__'):
            callable_obj = func
        elif isinstance(func, classmethod):
            # Classmethod wrapper - get the wrapped function
            callable_obj = func.__func__
        elif hasattr(func, '__init__'):
            # Class constructor
            callable_obj = func.__init__
        elif hasattr(func, '__call__'):
            # Handle any other callable type
            callable_obj = func.__call__
        else:
            print("Not a function call")
            return 0
        
        # Get filename and find actual def line for all callable types
        filename = callable_obj.__code__.co_filename
        lineno = callable_obj.__code__.co_firstlineno
        
        # This is only necessary to deal with decorated functions
        # Start at our function's line and move forward until we find the def line
        with open(filename, 'r') as f:
            lines = f.readlines()
            # Keep checking our specific line - if it's a decorator, move to next line
            while lineno <= len(lines) and lines[lineno - 1].strip().startswith('@'):
                lineno += 1
        
        self._si_mode = True
        self.set_break(filename, lineno + 1, temporary=True)
        self.set_continue()
        return 1

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
