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
                # Special handling for super() calls
                if call_expr == 'super' or line.strip().startswith('super()'):
                    return self._handle_super_call(line, frame)
                
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
    
    def _handle_super_call(self, line, frame):
        """Handle super() method calls."""
        try:
            # Extract the method name from super().method_name(...)
            if '.' in line and 'super().' in line:
                # Extract method name after super().
                method_part = line.split('super().')[1]
                method_name = method_part.split('(')[0]
                
                # Get the current class from the frame
                if 'self' in frame.f_locals:
                    self_obj = frame.f_locals['self']
                    current_class = self_obj.__class__
                    # Get parent classes
                    for base in current_class.__mro__[1:]:  # Skip self class
                        if hasattr(base, method_name):
                            parent_method = getattr(base, method_name)
                            if callable(parent_method) and parent_method != getattr(object, method_name, None):
                                return self._handle_callable(parent_method, f'super().{method_name}')
            print("Cannot step into super() call")
            return 0
        except Exception as e:
            print(f"Cannot step into super() call: {e}")
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
        
        # Skip past multi-line function signature to first executable line
        with open(filename, 'r') as f:
            lines = f.readlines()
            # Skip lines that are part of function signature
            while lineno <= len(lines):
                line = lines[lineno - 1].strip()
                if line.endswith(':'):
                    lineno += 1  # Move past the : line to first executable line
                    break
                lineno += 1  # why needed for multi-line definitions
        
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
