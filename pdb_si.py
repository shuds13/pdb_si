"""
pdb extension adding "si" (step into next call).

Skips function argument lines and steps directly into function bodies.
"""
import sys, pdb as _pdb
import os
import re
import inspect

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
                # For super() calls need to get class context
                call_expr = self._handle_super_call(call_expr, frame)
              
                try:
                    func = eval(call_expr, frame.f_globals, frame.f_locals)
                    if callable(func):
                        return self._handle_callable(func, call_expr)
                except Exception:
                    print("Could not step into function")
                    return 0
            
            print("Not a function call")
            return 0
    
    def _extract_function_call(self, line):
        s = line.strip()
        if '(' not in s:
            return None

        # find first '(' at top level (ignore inside [] and {})
        b = c = 0
        i = -1
        for k, ch in enumerate(s):
            if ch == '[': b += 1
            elif ch == ']': b -= 1
            elif ch == '{': c += 1
            elif ch == '}': c -= 1
            elif ch == '(' and b == 0 and c == 0:
                i = k
                break
        if i == -1:
            return None

        # find matching ')' for that '(' to detect ".method(" chain (e.g., super().__init__)
        p = 0
        j = -1
        for k in range(i, len(s)):
            if s[k] == '(': p += 1
            elif s[k] == ')':
                p -= 1
                if p == 0:
                    j = k
                    break
        if j != -1 and j + 1 < len(s) and s[j + 1] == '.':
            nxt = s.find('(', j + 1)
            if nxt != -1:
                i = nxt

        left = s[:i].strip()
        if left.startswith('return '):
            left = left[len('return '):].strip()
        if '=' in left:
            left = left.split('=', 1)[-1].strip()
        return left

    def _current_class(self, frame):
        selfobj = frame.f_locals.get('self')
        if not selfobj:
            return None
        name = frame.f_code.co_name
        for cls in inspect.getmro(selfobj.__class__):
            f = cls.__dict__.get(name)
            func = getattr(f, '__func__', f)
            if getattr(func, '__code__', None) is frame.f_code:
                return cls
        return selfobj.__class__

    def _handle_super_call(self, call_expr, frame):
        """Handle super() method calls by replacing with explicit class reference."""
        if call_expr and call_expr.startswith('super().') and 'self' in frame.f_locals:
            cls = self._current_class(frame)
            if cls:
                call_expr = call_expr.replace('super()', f'super({cls.__name__}, self)', 1)
        return call_expr

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
        
        # Use raw_function if available to avoid stopping in validators/decorators
        if hasattr(callable_obj, 'raw_function'):
            callable_obj = callable_obj.raw_function
        
        filename = callable_obj.__code__.co_filename
        lineno = callable_obj.__code__.co_firstlineno
        
        # Skip to first executable line
        lineno = self._find_first_executable_line(filename, lineno)
        
        self._si_mode = True
        self.set_break(filename, lineno, temporary=True)
        self.set_continue()
        return 1
    
    def _find_first_executable_line(self, filename, lineno):
        """Find the first executable line after function signature."""
        with open(filename, 'r') as f:
            lines = f.readlines()
            while lineno <= len(lines):
                line = lines[lineno - 1].strip()
                if line.endswith(':'):
                    lineno += 1  # Move past the : line to first executable line
                    break
                lineno += 1

            # Skip comment lines and docstrings to find first executable line
            in_doc = False
            dq = None
            while lineno <= len(lines):
                s = lines[lineno - 1].strip()
                if in_doc:
                    if dq in s:
                        in_doc = False
                    lineno += 1
                    continue
                if not s or s.startswith('#'):
                    lineno += 1
                    continue
                m = re.match(r"^[rbuftRBUFT]*([\"']{3})", s)
                if m:
                    dq = m.group(1)
                    # single-line docstring if closing quotes also on this line
                    if s.find(dq, m.end()) == -1:
                        in_doc = True
                    lineno += 1
                    continue
                break  # first non-comment, non-docstring line
        
        return lineno

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
