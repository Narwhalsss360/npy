import os

def clear(*args):
    if os.name == 'nt':
        os.system('CLS')
    else:
        os.system('clear')

def loading_bar(status, message = '', clear_on_each = False, fill_char = '=', todo_char = '.', head = '>'):
    if clear_on_each:
        clear()
    
    if status == 0:
        print(f'{message}[>.......................] 0%')
        return
    if status == 100:
        print(f'{message}[========================] 100%')
        return
    if status > 96:
        print(f'{message}[=======================>] {status}%')
        return

    done = status * .25
    bar = f'{message}['
    for i in range(int(done)):
        bar += fill_char
    for i in range(25 - int(done) - 1):
        if i == 0:
            bar += head
            continue
        bar += todo_char
    bar += ('] ' + str(status) + '%')

    print(bar)

class TerminalCommand:
    def __init__(self, name, callback, explanation):
        self.name = name
        self.callback = callback
        self.explanation = explanation

class TerminalCallbackArgs:
    def __init__(self, flags, args, raw):
        self.flags = flags
        self.args = args
        self.raw = raw

class TerminalApp:
    def __init__(self, title = 'Terminal App', entry_marker = '>', flag_delimiter = '--'):
        self.title = title
        self.entry_marker = entry_marker
        self. flag_delimiter = flag_delimiter
        self.commands = list()
    
    def show_error(self, message, info = ''):
        print(f'{self.title} | Error: {message} {info}')

    def show_help(self, command_name = None):
        if command_name is not None:
            for index, command in enumerate(self.commands):
                if command_name == command.name:
                    print(f'    {self.entry_marker}{command.name}{command.explanation} {command.callback}\n')
                    return
        help_message = f'\n{self.title} Help:\n'
        for index, command in enumerate(self.commands):
            help_message += f'    {self.entry_marker}{command.name}{command.explanation} {command.callback}\n'
        print(help_message)

    def ask(self, message) -> TerminalCallbackArgs:
        raw = input(message)
        statements = raw
        statements = statements.strip()

        if statements == '':
            return None

        args = statements.split('"')[1::2]
        for index, quote in enumerate(args):
            statements = statements.replace(f' "{quote}"', '')

        statements = statements.split() 

        flags = list()
        for index, statement in enumerate(statements):
            if statement.startswith(self.flag_delimiter):
                flags.append(statement)
            else:
                args.append(statement)

        return TerminalCallbackArgs(flags, args, raw)

    def get(self):
        raw = input(f'{self.title}{self.entry_marker}')
        statements = raw
        statements = statements.strip()

        if statements == '':
            return
        
        command_name = statements.split(' ')[0]

        args = statements.split('"')[1::2]
        for index, quote in enumerate(args):
            statements = statements.replace(f' "{quote}"', '')

        statements = statements.split() 
        statements.pop(0)

        flags = list()
        for index, statement in enumerate(statements):
            if statement.startswith(self.flag_delimiter):
                flags.append(statement)
            else:
                args.append(statement)
        for index, command in enumerate(self.commands):
            if command_name == command.name:
                command.callback(TerminalCallbackArgs(flags, args, raw))
                return

        if command_name == 'help':
            self.show_help()
            return

        self.show_error('Command does not exist in current context')