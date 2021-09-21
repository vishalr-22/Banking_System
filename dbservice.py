from datetime import datetime
import mysql.connector as mysql
from datetime import datetime,date
from datetime import timedelta

class dbservice:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_database()
        self.create_table()
    
    def connect_database(self):
        self.connector = mysql.connect(host='127.0.0.1', user='root', password='vishal')

        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('USE banking_system')

    def create_table(self):

        self.dbcursor.execute(''' CREATE TABLE IF NOT EXISTS `Customer` (
            `Cust_ID` INT NOT NULL AUTO_INCREMENT,
            `Name` VARCHAR(40) NOT NULL,
            `Balance` INT(40) NOT NULL,
            PRIMARY KEY(`Cust_ID`)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Transaction`(
            `Trans_ID` INT NOT NULL AUTO_INCREMENT,
            `Amount` VARCHAR(25) NOT NULL,
            `Payee` INT(40) NOT NULL,
            `Payer` INT(40) NOT NULL,
            `Status` VARCHAR(25) NOT NULL,
            PRIMARY KEY(`Trans_ID`),
            FOREIGN KEY(`Payee`) REFERENCES Customer(`Cust_ID`) ON DELETE CASCADE,
            FOREIGN KEY(`Payer`) REFERENCES Customer(`Cust_Id`) ON DELETE CASCADE
        );''')

        
        self.connector.commit()

    def transfer(self, table1, table2, input_data):
        payee = input_data[0]
        payer = input_data[1]
        amount = input_data[2]
        bal1 = (f"SELECT Balance FROM {table1} WHERE Cust_ID={payee}")
        bal2 = (f"SELECT Balance FROM {table1} WHERE Cust_ID={payer}")
        try:
            self.dbcursor.execute(bal1)
            record1 = self.dbcursor.fetchone()
            record1 = record1[0]
            self.dbcursor.execute(bal2)
            record2 = self.dbcursor.fetchone()
            record2 = record2[0]
            if int(amount) > record2:
                status = 'Unsuccessful'
                trans = (f"INSERT INTO {table2}(Amount, Payee, Payer, Status) VALUES({amount}, {payee}, {payer}, '{status}')")
                self.dbcursor.execute(trans)
                self.connector.commit()
                
                return 0
            elif int(amount) <= record2:
                b2 = int(record2) - int(amount)
                b1 = int(record1) + int(amount)
                new_bal1 = (f"UPDATE {table1} SET Balance = {b2} WHERE Cust_ID={payer}")
                new_bal2 = (f"UPDATE {table1} SET Balance = {b1} WHERE Cust_ID={payee}")
                self.dbcursor.execute(new_bal1)
                self.dbcursor.execute(new_bal2)
                status = 'Successful'
                trans = (f"INSERT INTO {table2}(Amount, Payee, Payer, Status) VALUES({amount}, {payee}, {payer}, '{status}')")
                self.dbcursor.execute(trans)
                self.connector.commit()
                return 1
            else:
                return 2

        except Exception as e:
            print(e)
        return 0
    
    
    def transfer_1cust(self, table, id, amount):
        
        query1 = (f"UPDATE {table} SET Balance = {amount} WHERE Cust_ID={id}")
        try:
            self.dbcursor.execute(query1)
            self.connector.commit()
                
        except Exception as e:
            print(e)
        return 0
    

    def fetch_column_data(self, table_name, columns, condition_name=None, condition_value=None):
        fetch_query = 'SELECT '

        for i,column in enumerate(columns):
            if i < len(columns)-1:
                fetch_query += f'{column}, '
            else:
                fetch_query += f'{column} FROM {table_name}'
        
        if condition_name != None and condition_value != None:
            fetch_query += f' WHERE {condition_name} = %(condition_value)s'
            try:
                self.dbcursor.execute(fetch_query, {'condition_value': condition_value})
            except Exception as e:
                print(e)
        else:
            try:
                self.dbcursor.execute(fetch_query)
            except Exception as e:
                print(e)
        columns_data = self.dbcursor.fetchall()
        
        return columns_data


        

