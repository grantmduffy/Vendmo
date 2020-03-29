from display import show_error

with open('main_output.log' 'w') as f:
    text = f.read()

show_error(text)