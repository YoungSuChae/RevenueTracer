import time
import random

class Stock:

    def __init__(self, stock_status):
        self._stock_status = stock_status

    def get_stock_status(self):
        return self._stock_status

    def set_stock_status(self, value):
        self._stock_status = value

    def stock_status_generator(self):
        while True:
            current_stock = random.randint(-100, 100)
            self.set_stock_status(current_stock)
            time.sleep(3)
            return current_stock

