from pprint import pp, pprint
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
import pprint
from flask_app.models import user

db = 'dream_board_customs_2'

class Pedal:
    def __init__(self, data):
        self.id = data['id']
        self.pedal_name = data['pedal_name']
        self.pedal_price = data['pedal_price']
        self.pedal_pic = data['pedal_pic']
        self.pedal_url = data['pedal_url']
        self.pedal_desc = data['pedal_desc']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pedal_id = data['pedal_id']

    @classmethod
    def save_pedal(cls, data):
        query = "INSERT INTO user_has_pedals (user_id, pedal_id) VALUES (%(user_id)s, %(pedal_id)s);"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM user_has_pedals WHERE user_id = %(user_id)s AND pedal_id = %(pedal_id)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def show_all_pedals(cls):
        query = "SELECT * FROM pedals;"
        results = connectToMySQL(db).query_db(query)
        all_pedals = []
        for p in results:
            all_pedals.append(p)
        return all_pedals

    @classmethod
    def show_pedals_by_user(cls, data):
        query = "SELECT * FROM users JOIN user_has_pedals ON users.id = user_has_pedals.user_id \
            JOIN pedals ON pedals.id = user_has_pedals.pedal_id WHERE users.id = %(id)s;"    
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def show_one_pedal_by_id(cls, data):
        query = "SELECT * FROM pedals WHERE pedals.id = %(pedal_id)s;"    
        result = connectToMySQL(db).query_db(query, data)
        one_pedal = []
        for this_pedal in result:
            one_pedal.append(this_pedal)
        print(one_pedal[0]['pedal_url'])
        return one_pedal
    
    @classmethod
    def calculate_total(cls, data):
        query = "SELECT * FROM users JOIN user_has_pedals ON users.id = user_has_pedals.user_id \
            JOIN pedals ON pedals.id = user_has_pedals.pedal_id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        total = 0
        for row in results:
            pedal_price = int(row['pedal_price'])
            total += pedal_price
            price_length = len(str(total))
        if price_length > 6:
            total = total[:price_length - 6] + "," + total[price_length -6:price_length -3] + "," + total[price_length - 3:price_length]
        elif price_length > 3:
            total = str(total)[:len(str(total)) - 3] + "," + str(total)[len(str(total)) - 3:len(str(total))]
        return total

    @classmethod
    def calculate_tax(cls,data):
        query = "SELECT * FROM users JOIN user_has_pedals ON users.id = user_has_pedals.user_id \
            JOIN pedals ON pedals.id = user_has_pedals.pedal_id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        total = 0
        for row in results:
            pedal_price = int(row['pedal_price'])
            total += pedal_price
        sales_tax = round(total * 0.05)
        sales_length = len(str(sales_tax))
        return sales_tax

    @classmethod
    def grand_total(cls, data):
        query = "SELECT * FROM users JOIN user_has_pedals ON users.id = user_has_pedals.user_id \
            JOIN pedals ON pedals.id = user_has_pedals.pedal_id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        total = 0
        for row in results:
            pedal_price = int(row['pedal_price'])
            total += pedal_price
        sales_tax = round(total * 0.05)
        grand_total = total + sales_tax
        total_length = len(str(grand_total))
        if total_length > 6:
            grand_total = grand_total[:total_length - 6] + "," + sales_tax[total_length -6:total_length -3] + "," + sales_tax[total_length - 3:total_length]
        elif total_length > 3:
            grand_total = str(grand_total)[:len(str(grand_total)) - 3] + "," + str(grand_total)[len(str(grand_total)) - 3:len(str(grand_total))]
        print(grand_total)
        return grand_total

    



