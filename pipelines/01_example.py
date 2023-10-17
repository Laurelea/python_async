def target():
    try:
        while True:
            data_chunk = (yield)
            print(f"Target: Получено {data_chunk}")
    except GeneratorExit:
        print("Target: Завершение")


def pipe():
    output = target()
    output.send(None)
    try:
        while True:
            data_chunk = (yield)
            print(f"Pipe: Обработка {data_chunk}")
            output.send(data_chunk * 2)
    except GeneratorExit:
        pass


def source():
    output = pipe()
    output.send(None)
    for data in range(5):
        print(f"Source: Отправлено {data}")
        output.send(data)
    output.close()


if __name__ == "__main__":
    source()
