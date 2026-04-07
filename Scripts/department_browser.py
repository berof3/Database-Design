
import mimerpy
import getpass
from sshtunnel import SSHTunnel
import pandas as pd

group_name = "ht25_2_1dl301_group_25"
group_password = "pasSWd_25"

def is_leaf(cursor, dept_id):
	cursor.execute(
		f'select p.dept_id, f.dept_id, f.title from department p left join department f on f.child_of = p.dept_id where p.dept_id = {dept_id}'
	)
	rows = cursor.fetchall()
	
	if len(rows) == 0:
		raise Exception("This department ID does not exit.")
	else:
		if rows[0][1] is None:
			return True
		else:
			return False
	
def get_child_depts(cursor, dept_id):
	cursor.execute(
		f'select dept_id, title from department where child_of = {dept_id}'
	)
	return cursor.fetchall()

def get_products(cursor, dept_id):
	cursor.execute(
		f'select prod_id, title, price_retail_no_tax as price_no_tax, tax_percent, discount_perc as disc_percent, round((price_retail_no_tax * (1 + tax_percent)) * (1 - discount_perc),2) as disc_price from product where dept_id = {dept_id}'
	)
	return cursor.fetchall()

def program(mydb):
		while True:
			try:
			
				mycursor = mydb.cursor()
				
				dept_id = int(input('\nEnter department ID to show child depts or products: '))

				if is_leaf(mycursor,dept_id):
					print('\n\nLeaf department, listing products:\n')
					data = get_products(mycursor,dept_id)
					df = pd.DataFrame(data, columns=['ID','TITLE','PRICE WO/TAX','TAX %','DISCNT %','RETAIL PRICE'])
					print(df)

				else:
					print('\n\nNot leaf department, listing child departments:\n')
					data = get_child_depts(mycursor, dept_id)
					df = pd.DataFrame(data, columns=['ID','TITLE'])
					print(df)

				mycursor.close()

				if input('\nDo you want to exit?  (Y/N): ').upper() == 'Y':
					break
			except Exception as e:
				print(f"\n\nException occurred: {e}")

def db_connect():
	mydb = mimerpy.connect(
		dsn="DBIP22024",
		user=group_name,
		password=group_password
	)

	program(mydb)

	mydb.close()

if __name__ == '__main__':
	ssh_username = input("Enter your Studium username: ")
	ssh_password = getpass.getpass("Enter your Studium password A: ")

	tunnel = SSHTunnel(ssh_username, ssh_password, 'groucho.it.uu.se', 22)
	tunnel.start(local_host='127.0.0.1', local_port=13600, remote_host='127.0.0.1', remote_port=1360)

	# Now the tunnel is ready, connect to DB
	db_connect()

	# Stop the tunnel
	tunnel.stop()
