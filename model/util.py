

def ask_bool_question(question) -> bool:
    """Ask a yes/no question and return True if answer is yes"""
    while True:
        resp = input(question).lower()
        if resp in ['y', 'yes']:
            return True
        if resp in ['n', 'no']:
            return False
        print('Please answer yes or no')

