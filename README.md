## Note 
- Every time i add a package i need to run : uv add --script web_app.py packageName
- Important to notice the use of type=module
    - <script type="module" src="{{ url_for('static', filename='js/map.js') }}"></script>
    - <script  src="{{ url_for('static', filename='js/chat.js') }}"></script>