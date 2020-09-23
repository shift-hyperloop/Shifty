import sqlite3
import datetime

conn = sqlite3.connect('mydatabase')

c = conn.cursor()

current_time = datetime.datetime.now()
old_data_time = current_time + datetime.timedelta(days=10)

c.execute(f"DELETE FROM attendance WHERE check_in < {old_data_time};")
c.execute(f'UPDATE attendance SET check_out = {current_time} WHERE check_out = NULL;')
