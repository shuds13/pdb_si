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
            current_line_no = frame.f_lineno - 1
            line = lines[current_line_no].strip()
            
            # Check if current line has function call
            call_expr = self._extract_function_call(line)
            if call_expr:
                try:
                    func = eval(call_expr, frame.f_globals, frame.f_locals)
                    if callable(func):
                        return self._handle_callable(func, call_expr)
                except Exception:
                    print("Not a function call")
                    return 0
            
            print("Not a function call")
            return 0
    
    def _extract_function_call(self, line):
        """Extract function name from a line containing a function call."""
        if '(' not in line:
            return None
        call_part = line.split('(')[0].strip()
        if '=' in call_part:
            return call_part.split('=')[-1].strip()
        return call_part
    
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
        
        # Skip decorators and multi-line function signatures
        with open(filename, 'r') as f:
            lines = f.readlines()
            # Skip decorators
            while lineno <= len(lines) and lines[lineno - 1].strip().startswith('@'):
                lineno += 1
            # Skip past multi-line function signature to first executable line
            if lineno <= len(lines) and lines[lineno - 1].strip().startswith('def '):
                lineno += 1
                # Skip lines that are part of function signature
                while lineno <= len(lines):
                    line = lines[lineno - 1].strip()
                    # Skip empty lines, lines ending with comma, and closing parenthesis
                    if not line or line.endswith(',') or line.startswith(')') or line == ')':
                        lineno += 1
                    else:
                        # Found first executable line
                        break
        
        self._si_mode = True
        self.set_break(filename, lineno, temporary=True)
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

# Monkey-patch the pdb module to use our Pdb class
import pdb
pdb.Pdb = Pdb
pdb.set_trace = set_trace
