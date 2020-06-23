import numpy as np

def load_from(path):

    with open(path, 'r') as f:
        lines = list(map(lambda l: l.replace('\n', '').split(), f.readlines()))
        file_name = lines[0][2]
        
        
        capacity = int(lines[5][2])
        cities_nb = int(lines[3][2])
        
        vehicules_nb = int(file_name.split("k",1)[1]) 
        
        cities_coords = []
        
        
        cities = lines[7:]
        for line in cities:
            if(line[0] == 'EOF' or line[0] == 'DEMAND_SECTION'):
                break;
            cities_coords.append(line)
        return np.array(cities_coords), capacity, cities_nb, vehicules_nb
            

def get_particular_info(path, string):
    with open(path, 'r') as f:
        lines = list(map(lambda l: l.replace('\n', '').split(), f.readlines()))
        for line in lines:
            if string == line[0]:
                return int(line[-1])
        return None
    
def get_data(cities_coords):
    length = len(cities_coords)
    adjacency_mat = np.zeros((length,length))
    cities_coords =  cities_coords.astype(np.int)
    for i, city in enumerate(cities_coords):
        #print(city)
        a = np.array([city[1],city[2]])
        for j in range(length):
            b =  np.array([cities_coords[j][1], cities_coords[j][2]])
            
            dist = np.linalg.norm(a-b)
            #print('A:',a,'B:',b,'out:',dist) 
            adjacency_mat[j][i] = dist
    return adjacency_mat
            

            
def  from_file_to_adj_matr(path):
    cities_coords, capacity, cities_nb,vehicules_nb = load_from(path)
    return get_data(cities_coords), capacity, cities_nb,vehicules_nb 
               
'''
if __name__ == '__main__':
    print(from_file_to_adj_matr('../data/A-VRP/A-n32-k5.vrp'))
'''
