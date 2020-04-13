"""
    Модуль демонстрационных примеров работы модуля basic_async

    author: https://github.com/egor43
"""

import datetime
import basic_async


def generator_coroutine(tag, stop_timestamp, answer):
    """
        Реализация простейшей корутины основанной на генераторе.
        Params:
            tag - метка корутины
            stop_timeatamp - временная метка после которой должен вернуться результат
            answer - результат, который необходимо вернуть
        Return:
            результат операции, который был передан в answer
    """
    while stop_timestamp > datetime.datetime.now():
        print(f'Итерация корутины: {tag}')
        yield None
    return answer


def future_coroutine(tag, stop_timestamp, answer):
    """
        Реализация корутины на основе FutureAnswer-объекта
        Params:
            tag - метка корутины
            stop_timeatamp - временная метка после которой должен вернуться результат
            answer - результат, который необходимо вернуть
        Return:
            результат операции, который был передан в answer
    """
    future = basic_async.FutureAnswer(tag, stop_timestamp, answer)
    yield from future
    return future.answer


def basic_task(label, stop_timestamp):
    """
        Реализация асинхронной задачи с использованием корутины-генератора.
        Имитация функционала, который реализует пользователь.
        Params:
            label - метка задачи
            stop_timeatamp - временная метка после которой должен вернуться результат
    """
    answer = yield from generator_coroutine(label, stop_timestamp, "BASIC ANSWER")
    print(f'Basic task answer: {answer}')


def future_task(label, stop_timestamp):
    """
        Реализация асинхронной задачи с использованием корутины на основе future объекта.
        Имитация функционала, который реализует пользователь.
        Params:
            label - метка задачи
            stop_timeatamp - временная метка после которой должен вернуться результат
    """
    answer = yield from future_coroutine(label, stop_timestamp, "FUTURE ANSWER")
    print(f'Future task answer: {answer}')


async def future_async_task(label, stop_timestamp):
    """
        Реализация асинхронной задачи, с использованием async/await.
        В задаче использется future объект напрямую.
        Имитация функционала, который реализует пользователь.
        Params:
            label - метка задачи
            stop_timeatamp - временная метка после которой должен вернуться результат
    """
    answer = await basic_async.FutureAnswer(label, stop_timestamp, "FUTURE ASYNC ANSWER")
    print(f'Future async task answer: {answer}')


def main():
    loop = basic_async.SimpleLoop(basic_task('A', datetime.datetime.now() + datetime.timedelta(seconds=10)),
                                  future_task('B', datetime.datetime.now() + datetime.timedelta(seconds=5)),
                                  future_async_task('C', datetime.datetime.now() + datetime.timedelta(seconds=3)))

    loop.run_loop()
    print('Finish all tasks')

if __name__ == '__main__':
    main()