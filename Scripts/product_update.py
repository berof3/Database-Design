
import mimerpy
import getpass
from sshtunnel import SSHTunnel

group_name = "ht25_2_1dl301_group_25"
group_password = "pasSWd_25"

def get_product(cursor, prod_id):
	cursor.execute(
		f'select prod_id, title, price_retail_no_tax as price_no_tax, tax_percent, discount_perc as disc_percent, round((price_retail_no_tax * (1 + tax_percent)) * (1 - discount_perc),2) as disc_price, featured from product where prod_id = {prod_id}'
	)
	if cursor.rowcount == 0:
		raise Exception("ProductID is not in the database.")
	return cursor.fetchall()

def print_product_details(cursor):
	
	product = cursor

	print(f'\n========================================================')
	print(f'Product ID  : {product[0][0]}')
	print(f'Title       : {product[0][1]}')
	print(f'Price wo/tax: {round(product[0][2],2)}')
	print(f'Tax percent : {round(product[0][3]*100,2)}%')
	print(f'Discount    : {round(product[0][4]*100,2)}%')
	print(f'Retail Price: {round(product[0][5],2)}')
	print(f'Featured    : {product[0][6]}')
	print(f'========================================================')


def update_title(cursor, prod_id, new_title):
	cursor.execute(
		f"update product set title = '{new_title}' where prod_id = {prod_id}"
	)

def update_featured(cursor, prod_id, new_featured):
	cursor.execute(
		f"update product set featured = '{new_featured}' where prod_id = {prod_id}"
	)

def update_price_no_tax(cursor, prod_id, new_price):
	cursor.execute(
		f'update product set price_retail_no_tax = {new_price} where prod_id = {prod_id}'
	)

def update_tax(cursor, prod_id, new_tax):
	cursor.execute(
		f'update product set tax_percent = {new_tax} where prod_id = {prod_id}'
	)

def update_discount(cursor, prod_id, new_discnt):
	cursor.execute(
		f'update product set discount_perc = {new_discnt} where prod_id = {prod_id}'
	)

def commit_update(mydb, cursor):
	if cursor.rowcount > 0:
		print(f'Updated! {cursor.rowcount} row(s) affected.')
		mydb.commit()
	else:
		print("WARNING: No rows affected!")

def program(mydb):

	while True:
		try:
			mycursor = mydb.cursor()

			prod_id = int(input('\nEnter product ID to show details: '))

			product = get_product(mycursor, prod_id)

			print_product_details(product)

			print('\n\nWhat do you want to do?')
			print('1. Update title')
			print('2. Update price before tax')
			print('3. Update tax percent')
			print('4. Update discount percent')
			print('5. Update featured')
			print('9. Select another product')
			print('0. Exit program')
			option = int(input('\nEnter the option number: '))

			if option == 1:
				new_title = input('Enter new title: ')
				update_title(mycursor, prod_id, new_title)
				commit_update(mydb, mycursor)
				print('New information: ')
				product = get_product(mycursor, prod_id)
				print_product_details(product)

			elif option == 2:
				new_price = float(input('Enter new price: '))
				update_price_no_tax(mycursor, prod_id, new_price)
				commit_update(mydb, mycursor)
				print('New information: ')
				product = get_product(mycursor, prod_id)
				print_product_details(product)

			elif option == 3:
				new_tax = float(input('Enter new tax percent (0-100): '))/100
				update_tax(mycursor,prod_id,new_tax)
				commit_update(mydb, mycursor)
				print('New information: ')
				product = get_product(mycursor, prod_id)
				print_product_details(product)

			elif option == 4:
				new_discount = float(input('Enter new discount (0-100): '))/100
				update_discount(mycursor,prod_id,new_discount)
				commit_update(mydb, mycursor)
				print('New information: ')
				product = get_product(mycursor, prod_id)
				print_product_details(product)

			elif option == 5:
				new_featured = input('Enter 1 for feature the product, 0 for unfeature: ')
				update_featured(mycursor, prod_id, new_featured)
				commit_update(mydb, mycursor)
				print('New information: ')
				product = get_product(mycursor, prod_id)
				print_product_details(product)

			elif option == 9:
				mycursor.close()

			elif option == 0:
				print('\nEnding program.\n')
				mycursor.close()
				break

			if option != 9:
				if input('\nDo you want to exit?  (Y/N): ').upper() == 'Y':
					break
		except Exception as e:
			print(f"\n\nException occurred: {e}")
			if input('\nDo you want to exit?  (Y/N): ').upper() == 'Y':
					break

	mycursor.close()

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
