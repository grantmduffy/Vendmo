from display import show_error

with open('main_output.log', 'rb') as f:
    text = f.read().decode('latin-1')

show_error(text)