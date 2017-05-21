"""
Tools for sending printouts to clipboard.
Only work for Mac.
"""

import subprocess

def write_to_clipboard(output):
    """
    writes output to clipboard
    """
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def read_from_clipboard():
    """
    Returns a string with whaterver is in the clipboard.
    """
    return subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
    