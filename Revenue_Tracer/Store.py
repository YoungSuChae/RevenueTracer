import csv
import uuid
import datetime
from collections import deque


class Store:
    def __init__(self, store_id, store_name, store_address, store_phone, monthly_revenue, date_revenue):
        self._store_id = store_id
        self._store_name = store_name
        self._store_address = store_address
        self._store_phone = store_phone
        self._monthly_revenue = monthly_revenue
        self._date_revenue = date_revenue

    @staticmethod
    def currentMonthlyRevenue():
        currentMonthlyRevenue = None
        with open('Store.csv') as f:
            for line in f:
                split_line = line.strip().split(',')
                if len(split_line) == 6:  # Check that the line contains 6 values
                    store_id,store_name,store_address,store_phone,monthly_revenue,date_revenue = split_line
                    pass
            currentMonthlyRevenue = monthly_revenue
        return currentMonthlyRevenue

    @staticmethod
    def previousMonthlyRevenue():
        previousMonthlyRevenue = None
        with open('Store.csv') as f:
            last_lines = deque(f, 2) 
        
        if len(last_lines) == 2:
            previousMonthlyRevenue = last_lines[0].strip().split(',')[-2]  

        return previousMonthlyRevenue
    
    @staticmethod
    def mostProfitableStore():
        with open('Store.csv') as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) == 6:
                    store_id,store_name,store_address,store_phone,monthly_revenue,date_revenue = fields
                    fields.sort()
                    fields[-1]
        return f"{str(store_name)}, {str(store_address)}"


    @staticmethod
    def add_store(store_name, store_address, store_phone, monthly_revenue, date_revenue):
        with open("Store.csv", "r") as file:
            reader = csv.reader(file)
            stores = list(reader)

        for store in stores:
            if len(store) >= 3 and store[1] == store_name and store[2] == store_address:
                raise ValueError(
                "A store with the same name and address already exists."
            )

        # Find the highest store_id in the file
        highest_store_id = max(int(store[0]) for store in stores if store[0].isdigit()) if stores else 0
        
        # The new store_id is one more than the highest one
        store_id = highest_store_id + 1

        stores.append([store_id, store_name, store_address, store_phone, monthly_revenue, date_revenue])

        with open("Store.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(stores)

    @staticmethod
    def search_store(store_name, store_address):
        with open("Store.csv", "r") as file:
            reader = csv.reader(file)
            stores = list(reader)

        for store in stores:
            if store[1] == store_name and store[2] == store_address:
                return store[1:4]  # return all the information of the store except the store_id

        return "No store found with the given name and address"

    @staticmethod     
    def deleteStore(store_name, store_address):
        with open("Store.csv", "r") as file:
            reader = csv.reader(file)
            stores = list(reader)

        store_deleted = False

        # Iterate through stores and remove the one that matches the name and address
        for store in stores:
            if store[1] == store_name and store[2] == store_address:
                stores.remove(store)
                store_deleted = True
                break  # Stop iteration after deleting the store

        # Rewrite the updated list of stores back to the CSV file
        if store_deleted:
            with open("Store.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(stores)
            return "Store was deleted successfully"
        else:
            raise ValueError("No store found with the given name and address")
        