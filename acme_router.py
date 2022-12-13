import multiprocessing
from threading import Thread


class PreProcessor:

    _vowels: set = {'a','e','i','o','u'}
    _consonants: set = {'b', 'c', 'd', 'f', 'g', 'h',
        'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 
        's', 't', 'v', 'w', 'x', 'y', 'z'}
    
    def driver_names(self, names: list[str], result: list[dict]):
        '''Preprosesor for driver names
        '''
        for name in names:

            vowel_amount = 0
            consonant_amount = 0
            for char in name:
                if char.lower() in self._vowels:
                    vowel_amount += 1
                if char.lower() in self._consonants:
                    consonant_amount += 1

            result.append({
                'name': name,
                'len': len(name),
                'value': (vowel_amount*1.5, consonant_amount),
            })    
        
    
    def street_names(self, streets: list[str], result: list[int]):
        '''Preprosesor for street names
        '''
        for street in streets:
            
            result.append({
                'len': len(street),
                'is_even': 0 if len(street)%2 == 0 else 1,
            })
        

class LLNode:
    
    def __init__(self, name, val) -> None:
        self.name = name
        self.val = val
        self.next = None
        self.prev = None


class AcmeRouter:
    
    preprocess_drivers = []
    preprocess_streets = []
    
    def __init__(self) -> None:
        self.pre_processor = PreProcessor()
        self.cpu_amount = multiprocessing.cpu_count()

    def _pre_processor_divide_work(self, streets, names) -> list[list[str]]:
        half_amount = self.cpu_amount//2
        
        names_split_size = int(len(names) // half_amount)
        streets_split_size = int(len(streets) // half_amount)
        
        nss_c = 0
        sss_c = 0
        
        names_divide = []
        street_divide = []
        for i in range(0, half_amount-1):
            names_divide.append(names[nss_c:nss_c+names_split_size])
            street_divide.append(streets[sss_c:sss_c+streets_split_size])
            nss_c = nss_c+names_split_size
            sss_c = sss_c+streets_split_size

        names_divide.append(names[nss_c:])
        street_divide.append(streets[sss_c:])
        return [names_divide, street_divide]
    
    def _pre_process(self, streets, names) -> None:
        names_section, street_section = self._pre_processor_divide_work(streets, names)
        
        threads = []
        for index in range(0, self.cpu_amount//2):
            
            names_current_thread = Thread(
                target=self.pre_processor.driver_names, args=[names_section[index], self.preprocess_drivers])
            names_current_thread.start()
            threads.append(names_current_thread)
            
            street_current_thread = Thread(
                target=self.pre_processor.street_names, args=[street_section[index], self.preprocess_streets])
            street_current_thread.start()
            threads.append(street_current_thread)
        
        for index, thread in enumerate(threads):
            thread.join()
    
    def _sum_healper(self, street, driver):
        '''Sum streat and driver SS
        '''
        base_ss = driver['value'][street['is_even']]
        
        if driver['len'] != 1 and street['len']%driver['len'] == 0:
            base_ss *=1.5
        
        return base_ss
    
    def _calculate_street_driver(self):
        results = []
        for street in self.preprocess_streets:
            street_sums = []
            for driver in self.preprocess_drivers:
                street_sums.append((driver['name'], self._sum_healper(street, driver)))
            street_sums.sort(key=lambda x: x[1],reverse=True)
            
            locations = {}
            driver_list = None
            current_node = None
            for current_driver in street_sums:
                if driver_list is None:
                    driver_list = LLNode(current_driver[0], current_driver[1])
                    current_node = driver_list
                else:
                    new_node = LLNode(current_driver[0], current_driver[1])
                    current_node.next = new_node
                    new_node.prev = current_node
                    current_node = new_node
                
                locations[current_node.name] = current_node
                    
            results.append({
                'locations': locations,
                'driver_list': driver_list
            })
            
        return results
    
    def calculate(self, streets: list[str], names: list[str]) -> float:
        self._pre_process(streets, names)    

        streat_driver_matrix = self._calculate_street_driver()
        final_result = 0
        while streat_driver_matrix:
            
            max_sum_index = None
            max_sum = LLNode(None, 0)
            for index, current_sum in enumerate(streat_driver_matrix):
                if current_sum['driver_list'].val > max_sum.val:
                    max_sum = current_sum['driver_list']
                    max_sum_index = index

            for index, current_sum in enumerate(streat_driver_matrix):
                if index != max_sum_index:
                    node_to_remove = current_sum['locations'][max_sum.name]
                    prev = node_to_remove.prev
                    next = node_to_remove.next
                    
                    if not prev:
                        current_sum['driver_list'] = next
                        next.prev = None
                    elif not next:
                        prev.next = None
                    else:
                        prev.next = next
                        next.prev = prev
                    
                    
                    del current_sum['locations'][max_sum.name]
            del streat_driver_matrix[max_sum_index]
            final_result += max_sum.val

        return final_result
