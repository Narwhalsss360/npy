from npy import terminal, npy
from time import sleep

user_saved_items = dict()

terminal_app = terminal.TerminalApp('Terminal App Test Title', entry_marker=' → ')

def add(s):
    result = 0
    for index, number in enumerate(s.args):
        result += int(number)

    for index, flag in enumerate(s.flags):
        if flag == '--negate':
            result *= -1
        if flag == '--abs':
            result = abs(result)
    print(result)

def subtract(s):
    result = int(s.args[0])
    s.args.pop(0)
    for index, number in enumerate(s.args):
        result -= int(number)

    for index, flag in enumerate(s.flags):
        if flag == '--negate':
            result *= -1
        if flag == '--abs':
            result = abs(result)
    print(result)

def show_a_text_file(s):
    path = s.args[0]
    lines = list()
    temp_lines = list()
    with open(path, 'r') as text_file:
        temp_lines = text_file.readlines()

    for line_number, line in enumerate(temp_lines):
        status = int(npy.mapf(line_number, 0, len(temp_lines) - 1, 0, 100))
        terminal.loading_bar(status, f'Loading file... {path}', clear_on_each=False)
        lines.append(line)
        sleep(0.08)

    output = ' '.join(lines)
    for index, flag in enumerate(s.flags):
        if flag == '--raw':
            output = lines

    print(f'\n{output}\n')

def save_item(s):
    global user_saved_items
    user_saved_items.update({ s.args[0] : s.args[1] })

def custom_help(s):
    print('Just read the source code...')

def exit_app(s):
    print('Exiting...')
    exit()

add_command = terminal.TerminalCommand('add', add, ': <numbers...> Adds numbers together.')
subtract_command = terminal.TerminalCommand('subtract', subtract, ': <minuend> <subtrahend...> Subtracts numbers.')
clear_command = terminal.TerminalCommand('clear', terminal.clear, ': Clears the terminal window.')
show_text_file_command = terminal.TerminalCommand('show', show_a_text_file, ': <filepath> Shows a text file.')
custom_help_command = terminal.TerminalCommand('help', custom_help, ': Show help.')
save_item_command = terminal.TerminalCommand('save', save_item, ': Save and item')
exit_command = terminal.TerminalCommand('exit', exit_app, ': Exits application.')

terminal_app.commands.append(add_command)
terminal_app.commands.append(subtract_command)
terminal_app.commands.append(clear_command)
terminal_app.commands.append(show_text_file_command)
#terminal_app.commands.append(custom_help_command) #Uncomment for a custom help message.
terminal_app.commands.append(save_item_command)
terminal_app.commands.append(exit_command)

while True:
    terminal_app.get()