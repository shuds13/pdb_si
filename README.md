## pdb-si

A Python pdb extension that adds an `si` (step into) command to skip function
argument lines and step directly into function bodies.

Also skips decorators, validators and other redirects.

### Setup

1. Copy `pdb_si.py` to any directory
2. Add that directory to your PYTHONPATH in your `.bashrc`:
   ```bash
   export PYTHONPATH="$PYTHONPATH:/path/to/directory/containing/pdb_si.py"
   ```

### Usage

Add ``import pdb_si`` at the top of your code and then use pdb as normal.

See [tests/test_simple.py](tests/test_simple.py) for demo.


### Limitations

The function must be the top level call on a line - does not work with embedded functions. 

E.g., does not work with:


```python

a = [funca()]

```

### Issues

Please report issues in github issues.
