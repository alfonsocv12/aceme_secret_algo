# Acme routing algo

Acme needs to outsource their shipment router, inside the 
organization,
the 3rd party trucking fleets can only route one shipment per 
driver a day.

## Predefine requirements

The program has to be a CLI 

### Routing model

A group of data scientists created a mathematical model that 
determines which driver is best suited to deliver each shipment

``` python
def ss_calculator(street_name, driver_name) -> float:
    is_even: bool = len(street_name)%2 == 0
    vowels: set = {'a','e','i','o','u'}
    consonants: set = {'b', 'c', 'd', 'f', 'g', 'h',
        'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 
        's', 't', 'v', 'w', 'x', 'y', 'z'}

    ss = 0.0

    for char in driver_name:
        if is_even and char.lower() in vowels:
            ss += 1
        elif char.lower() in consonants:
            ss += 1

    if is_even: ss = ss*1.5

    if (len(driver_name) != 1 and 
        len(destination_street_name) % len(driver_name) == 0):
        ss = ss*1.5
    
    return ss
```

### Input

Every day the program will receive a list of shipment destinations
and drivers, this will come in a separate file each new line will
be a destination or a driver.

Example:

Destinations file
``` text
address 1
address 2
address 3
```

Drivers file
``` text
driver 1
Driver 2
drivEr 3
```

For development take into consideration that the inputs are
case-sensitive.

## Solution

### Take into consideration

I need to find an optimal solution for each driver and street 
name, each different convination of address and driver will 
result in a different base_ss, but I can divide the calculation 
function to pre-process some stuff like the driver_name base_ss.

#### Pre-process

On the pre-process I need to use multithread to divide workload 
first haf of the cores will process the vowels and consonats of
each driver_name the other half will get if streat names are even or not.

```python
[
    True,
    False
]
[
    (even_ss, not_even_ss),
    (even_ss, not_even_ss),
]
```

#### Selection stage

Base on the pre_process data I need to select the best convination of street and driver name.

Brute force solution will be to convine every posibility that is not require because the numbers can tell what is the best conbination.

I try to make this as simple as possible I believe it endedup a little more complex than intended, I'm happy with the speed and how much,
more divisiable the work is.
