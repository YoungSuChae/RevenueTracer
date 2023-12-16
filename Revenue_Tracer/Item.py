import pandas as pd
from operator import concat 
import csv



class Item:
    counter = 0
    def __init__(self, item_id, item_name, item_revenue, quantity):
        self._item_id = item_id
        self._item_name = item_name
        self._item_revenue = item_revenue
        self._quantity = quantity

    def __str__(self) -> str:
        return (f"{self._item_id},{self._item_name},{self._item_revenue},{self._quantity}\n")

    @staticmethod
    def get_byte_offset(line_number):
        with open('itemList.csv', 'r') as file:
            for i, line in enumerate(file):
                if i == line_number:
                    return file.tell() - len(line)

#add an item into the csv file
#Use self function to idenfiy the department that teh item belongs too (each dept ahs their own list)
    @staticmethod
    def add_item(item_name, revenue, quantity):
        count = 0
        with open('ItemList.csv', 'r') as file:
            for line in file:
                count += 1
        file.close()
        item_id = count
        item = Item(item_id, item_name, revenue, quantity)
        with open('ItemList.csv', 'a') as file: # append mode
            file.write(f"{item_id},{item_name},{revenue},{quantity}\n")
        return f"The Item: {item_name} has been added. :)"

    @staticmethod
    def search_item(item_name):
        with open('ItemList.csv', 'r') as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) == 4:
                    item_id, name, revenue, quantity = fields
                    current_item = Item(*fields)
                    if item_name == name:
                        return f"Item ID: {item_id} \nItem name: {item_name} \nItem price: ${revenue} \nItem quantity: {quantity}"

            return f"Item {item_name} could not be found"
        
    @staticmethod
    def delete_item(item_name):
        
        item = item_name
        df = pd.read_csv('ItemList.csv')
        df = df.drop(df[df.item_name == item].index)
        df.to_csv('ItemList.csv', index=False)     
        return f"Item {item_name} has been deleted"
        
    @staticmethod  
    def item_revenue():
        item_sales = pd.read_csv("ItemList.csv")

        item_sales = item_sales.drop(columns=['item_id'])
        item_sales = pd.DataFrame(item_sales)
        
        revenue = item_sales['item_price'] * item_sales['item_quantity']
        item_sales['item_revenue'] = revenue

        max_revenue_index = item_sales['item_revenue'].idxmax()
        max_item_name = item_sales.loc[max_revenue_index, 'item_name']
        max_item_rev = item_sales['item_revenue'].max()

        curr_rev =  f"{str(max_item_name)}: ${str(max_item_rev)}"

        return curr_rev
    
    def item_count(itemName):
        with open('ItemList.csv', 'r') as file:
                for line in file:
                    fields = line.strip().split(",")
                    if len(fields) == 4:
                        item_id, item_name, item_price, item_quantity = fields
                        if itemName == item_name:
                            return int(item_quantity)
                return 0
