# Импортируются модули для работы с потоками, генерации случайных чисел и управления временем.
import threading
import random
import time


# Определяется класс Bank, который моделирует банковские операции.
class Bank:
    # Конструктор __init__ инициализирует: balance - начальный баланс равен 0.
    # lock - объект блокировки для управления доступом к балансу в многопоточной среде.
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    # Метод deposit для пополнения счета.
    def deposit(self):
        # Цикл будет выполнен 100 раз.
        for _ in range(100):
            # Генерируется случайная сумма от 50 до 500 и добавляется к балансу.
            money = random.randint(50, 500)
            self.balance += money
            # Если баланс достигает 500 и замок заблокирован, он разблокируется.
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            # Выводится информация о пополнении и текущем балансе.
            print(f'Пополнение {money}. Баланс:  {self.balance}.')
            # Ожидание 0.001 секунды, чтобы смоделировать задержку.
            time.sleep(0.001)

    # Метод take для снятия средств.
    def take(self):
        # Цикл также выполнится 100 раз.
        for _ in range(100):
            # Генерируется случайная сумма для снятия и выводится запрос.
            money = random.randint(50, 500)
            print(f'Запрос на {money}.')
            # Если запрашиваемая сумма меньше или равна балансу, она снимается, и выводится обновленный баланс.
            if money <= self.balance:
                self.balance -= money
                print(f'Снятие {money}. Баланс: {self.balance}.')
            # Если запрашиваемая сумма превышает баланс, выводится сообщение об отказе, и поток блокируется.
            if money > self.balance:
                print(f'Запрос отклонен,недостаточно средств.')
                self.lock.acquire()
            # Ожидание 0.001 секунды.
            time.sleep(0.001)


# Создается объект bk класса Bank.
bk = Bank()
# Создаются два потока: один для метода deposit, другой для метода take.
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))
# Запускаются потоки.
th1.start()
th2.start()
# Основной поток ожидает завершения потоков th1 и th2.
th1.join()
th2.join()
# После завершения потоков выводится итоговый баланс.
print(f'Итоговый баланс: {bk.balance}')
