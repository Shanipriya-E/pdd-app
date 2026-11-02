import js2py
import traceback
try:
    with open('events.js', 'r', encoding='utf-8') as f:
        code = f.read()
    js2py.parse_js(code)
    print("No syntax errors")
except Exception as e:
    print(traceback.format_exc())
