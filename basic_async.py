"""
    Модуль предоставляет тестовую реализацию собственного набора асинхронных инструментов.

    author: https://github.com/egor43
"""

import datetime
import collections
import time


class FutureAnswer:
    """
        Описание объекта получения отложенного объекта для работы с event-loop'ом.
        Возвращает заданное значение не раньше указанного времени
    """
    
    def __init__(self, tag, stop_timestamp, answer):
        """
            Инициализация экземпляра.
            Params:
                tag - метка объекта
                stop_timestamp - временная метка по достижению которой можно вернуть результат
                answer - резальтат работы
            Return:
                self - текущий экземпляр класса FutureAnswer
        """
        self.tag = tag
        self.stop_timestamp = stop_timestamp
        self.answer = answer
    
    def __iter__(self):
        """
            Итеаратор объекта.
            Return:
                self - текущий экземпляр класса FutureAnswer
        """
        return self
    
    def __next__(self):
        """
            Выполняет переход на следующую итерацию.
            Проверяется истечение времени и принимается решение о завершении работы
            Return:
                None - если задача еще не закончеа
                StopIteration - при завершении работы задачи
        """
        print(f'Выполняется экземпляр: {self.tag}')
        if self.stop_timestamp < datetime.datetime.now():
            # Отправляем значение асинхронной работы
            raise StopIteration(self.answer)
    
    def __await__(self):
        """
            Возвращает асинхронный итератор
            Return:
                self - текущий экземпляр класса FutureAnswer
        """
        return self
    
    def send(self, arg):
        """
            Обработка входящего значения переданного итератору.
            Params:
                arg - переданное объекту значение
            Return:
                None - если задача еще не закончеа
                StopIteration - при завершении работы задачи
        """
        return self.__next__()


class SimpleLoop:
    """
        Описание простого event-loop 
    """
    
    def __init__(self, *coroutines):
        """
            Инициализация экземпляра
            Params:
                coroutines - корутины, которые будут обрабатываться циклом событий
        """
        self.coroutines = coroutines
        self.starting_coroutines = collections.deque()
    
    def run_loop(self):
        """
            Запуск цикла событий (event-loop)
        """
        for coro in self.coroutines:
            # Запускаем корутину
            try:
                coro.send(None)
                self.starting_coroutines.append(coro)
            except StopIteration:
                pass

        # Пока есть незавершенные корутины
        while self.starting_coroutines:
            coro = self.starting_coroutines.popleft()
            try:
                # "Прокручиваем" корутину
                coro.send(None)
                self.starting_coroutines.append(coro)
                
                # Засыпаем на секунду для удобства отслеживания процесса работы
                time.sleep(1)  
            except StopIteration:
                pass    
