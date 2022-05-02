'''
This is an implementation of an open Hash Table with search and insert operations and the ability to grow dynamically

More Information: https://rpucella.net/other/is-dsa-sp22/
'''  
from cProfile import label
import timeit
import matplotlib.pyplot as plt

class OpenHashTable():
    def __init__(self, size = 1, probe = 'linear'):
        self.table = [[]]*size
        self.probe = probe
        
    def hash_key(self, k):
        '''
        Hashes keys
        '''
        return hash(k) % self.get_size()

    def hash2_key(self, k):
        '''
        Secondary hash function for double hashing
        '''
        return (((k//self.get_size()) % (self.get_size()// 2)) * 2) + 1
       
    
    def convert_probe_function(self, probe, k, hashed_key):
        '''
        Converts the probe name into the probe function to be used
        '''

        switcher = {
            'linear': self.linear_probe(k, hashed_key),
            'quadratic': self.quadratic_probe(k, hashed_key),
            'double hashing': self.double_hashing(k, hashed_key)
        }
    
        return switcher.get(probe, 'Error')

    def get_size(self):
        '''
        Returns the size of the hashtable
        '''
        return len(self.table)

    def get_num_used_slots(self):
        '''
        Returns the number of slots/indices in the hashtable that are used
        '''
        return len(list(filter(lambda elem: len(elem) > 0, self.table)))

    def need_to_resize(self):
        '''
        Returns true if needed to resize and false otherwise
        '''
        size = self.get_size()
        slots_used = self.get_num_used_slots()

        if slots_used / size > .75:
            return True
        else:
            return False

    def resize(self):
        '''
        This method doubles the old size of the array and rehashes all of the existing elements accordingly
        '''
        old_table = [num for sublist in self.table for num in sublist]
        self.table = [[]] * (2 * self.get_size())

        for elem in old_table:
            self.insert(elem[0], elem[1])

    def linear_probe(self, k, hashed_key):
        '''
        This method inserts a key and value using a linear probe 
        '''
        while self.table[hashed_key]:
            if k == self.table[hashed_key][0][0]:
                return hashed_key
            else:
                hashed_key = self.hash_key(hashed_key + 1)
        
        return hashed_key

    def quadratic_probe(self, k, hashed_key):
        '''
        This method inserts a key and value using a quadratic probe
        '''
        i = 0
        
        while self.table[hashed_key] and i < self.get_size():
            i += 1
            if k == self.table[hashed_key][0][0]:
                return hashed_key
            else:
                hashed_key = self.hash_key(hashed_key + i*i)
        
        return hashed_key

    def double_hashing(self, k, hashed_key):
        '''
        This method inserts a key and value using double hashing
        '''

        i = 0
        while self.table[hashed_key] and i < self.get_size():
            i += 1
            if k == self.table[hashed_key][0][0]:
                return hashed_key
            else:
                hashed_key = (self.hash_key(hashed_key) + i * self.hash2_key(hashed_key)) % self.get_size()
        return hashed_key

    def insert(self, k, v):
        '''
        This method inserts the key value pair k, v at the hashtable index, and if key k already exists in the table, replaces the existing value with v
        '''
        if self.need_to_resize():
            self.resize()

        h_key = self.hash_key(k)

        hashed_key = self.convert_probe_function(self.probe, k, h_key)
        
        self.table[hashed_key] = [(k,v)]
           
    def search(self, k):
        '''
        This method searches the array for a given key and returns the value from that key
        '''
       
        h_key = self.hash_key(k)

        hashed_key = self.convert_probe_function(self.probe, k, h_key)

        if self.table[hashed_key]:
            return self.table[hashed_key][0][1]
        else:
            return None
        
    def print_table(self):
        '''
        This method prints the hash table
        '''
        for item in self.table:
            print(item)

def linear_time(list_size = 1000, table_size = 100):
    num_runs = 100
    list_size = list_size
    table_size = table_size

    SETUP = '''from __main__ import OpenHashTable
from random import random
my_list = [(int(random()*10000), "value") for n in range(list_size)]
table = OpenHashTable(table_size)
        '''
    CODE = '''
for pair in my_list:
    table.insert(pair[0],pair[1])
        '''
    times = timeit.timeit(setup = SETUP, stmt = CODE, globals = locals(), number = num_runs)
    return times/num_runs

def quadratic_time(list_size = 1000, table_size = 100):
    num_runs = 100
    list_size = list_size
    table_size = table_size
    print('here')

    SETUP = '''from __main__ import OpenHashTable
from random import random
my_list = [(int(random()*10000), "value") for n in range(list_size)]
table = OpenHashTable(table_size, probe = 'quadratic')
        '''
    CODE = '''
for pair in my_list:
    table.insert(pair[0],pair[1])
        '''
    times = timeit.timeit(setup = SETUP, stmt = CODE, globals = locals(), number = num_runs)
    return times/num_runs

def double_hash_time(list_size = 1000, table_size = 100):
    num_runs = 100
    list_size = list_size
    table_size = table_size

    SETUP = '''from __main__ import OpenHashTable
from random import random
my_list = [(int(random()*10000), "value") for n in range(list_size)]
table = OpenHashTable(table_size, probe = 'double hashing')
        '''
    CODE = '''
for pair in my_list:
    table.insert(pair[0],pair[1])
        '''
    times = timeit.timeit(setup = SETUP, stmt = CODE, globals = locals(), number = num_runs)
    return times/num_runs

def close_hash_time(list_size = 1000, table_size = 100):
    num_runs = 100
    list_size = list_size
    table_size = table_size
    print(list_size)

    SETUP = '''from hashtable import HashTable
from random import random
my_list = [(int(random()*10000), "value") for n in range(list_size)]
table = HashTable(table_size)
        '''
    CODE = '''
for pair in my_list:
    table.insert(pair[0],pair[1])
        '''
    times = timeit.timeit(setup = SETUP, stmt = CODE, globals = locals(), number = num_runs)
    return times/num_runs

if __name__ == "__main__":

    # print('linear: ' + str(linear_time()))
    # print('quadratic: ' + str(quadratic_time()))
    # print('double hashing: ' + str(double_hash_time()))
    # print('close hash time: ' + str(close_hash_time()))

    lin_table_times = []
    quad_table_times = []
    double_table_times = []
    close_table_times = []

    # change inital table size
    for i in range (10, 1000, 20):
        lin_table_times.append([i, linear_time(table_size = i)])
        quad_table_times.append([i, quadratic_time(table_size = i)])
        double_table_times.append([i, double_hash_time(table_size = i)])
        close_table_times.append([i, close_hash_time(table_size = i)])
    
    plt.plot([item[0] for item in lin_table_times], [item[1] for item in lin_table_times], label = "linear probing")
    plt.plot([item[0] for item in quad_table_times],[item[1] for item in quad_table_times], label = "quadratic probing")
    plt.plot([item[0] for item in double_table_times], [item[1] for item in double_table_times], label = "double hashing")
    plt.plot([item[0] for item in close_table_times], [item[1] for item in close_table_times], label = "closed hashing")
    plt.legend()
    plt.savefig('table_size.png')

    lin_list_times = []
    quad_list_times = []
    double_list_times = []
    close_list_times = []

    # change inital list size
    for i in range (100, 10000, 50):
        lin_list_times.append([i, linear_time(list_size = i)])
        quad_list_times.append([i, quadratic_time(list_size = i)])
        double_list_times.append([i, double_hash_time(list_size = i)])
        close_list_times.append([i, close_hash_time(list_size = i)])
        
    plt.plot([item[0] for item in lin_list_times], [item[1] for item in lin_list_times], label = "linear probing")
    plt.plot([item[0] for item in quad_list_times],[item[1] for item in quad_list_times], label = "quadratic probing")
    plt.plot([item[0] for item in double_list_times], [item[1] for item in double_list_times], label = "double hashing")
    plt.plot([item[0] for item in close_list_times], [item[1] for item in close_list_times], label = "closed hashing")
    plt.legend()
    plt.savefig('list_size.png')
    
    

    # table1 = OpenHashTable(10, probe = 'double hashing')
    # table1.insert(1, "hello")
    # table1.insert(7, "goodbye")
    # table1.insert(2, "check")
    # table1.insert(3, "see")
    # table1.insert(33, "jokes")
    # table1.insert(12, "maia")
    # table1.insert(12, "work?")
    # table1.insert(20, "exciting!")
    # table1.insert(31, "yay!!")
    # print(table1.search(2))
    # print(table1.search(12))
    # print(table1.search(4))
    # print(table1.search(32))
    # table1.insert(87, "test6")
    # table1.insert(37, "test5") 
    # table1.insert(57, "test4")
    # table1.insert(97, "test3")
    # table1.insert(17, "test2")
    # table1.insert(31, "test1")
    # table1.print_table()
    