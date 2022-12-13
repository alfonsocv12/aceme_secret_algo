from acme_router import AcmeRouter

streets_file_path = input('Streets File path ').strip()
drivers_file_path = input('drivers File path ').strip()


streets_file = open(streets_file_path)
streets = streets_file.read().split('\n')
streets_file.close()
drivers_file = open(drivers_file_path)
drivers = drivers_file.read().split('\n')
drivers_file.close()


if len(streets) != drivers:
    raise Exception('The driver amount most be equal to street amount') 


print(f'result: {AcmeRouter().calculate(streets, drivers)}')