from sys import settrace

def tracer(frame, event, arg=None):
    code = frame.f_code
    func_name = code.co_name
    line_no = frame.f_lineno
    print(f'Событие {event} в функции {func_name}() в строке {line_no}.')
    return tracer

def my_function():
    return "Привет, Практикум!"

def process():
    return my_function()

if __name__ == '__main__':
    settrace(tracer)
    process()
