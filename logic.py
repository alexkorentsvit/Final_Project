def calc_matrix(spectrum_vhid,data):
    spectrum = spectrum_vhid.split(',')
    him_el = []
    for i in range(5):
        him_el.append([data[i].name, data[i].spectrum.split(',')])
    matrix = []
    for i in range(5):
        matrix.append([float(him_el[0][1][i]), float(him_el[1][1][i]), float(him_el[2][1][i]), float(him_el[3][1][i]), float(him_el[4][1][i]), float(spectrum[i])])
    
    
    
    
    buf_del = matrix[0][0]
    for i in range(len(matrix[0])):
        matrix[0][i] = matrix[0][i] / buf_del
            
    buf_del = - matrix[1][0]
    for i in range(len(matrix[0])):
        matrix[1][i] = matrix[0][i]*buf_del + matrix[1][i]
        
    buf_del = - matrix[2][0]
    for i in range(len(matrix[0])):
        matrix[2][i] = matrix[0][i]*buf_del + matrix[2][i]                                                
        
    buf_del = - matrix[3][0]
    for i in range(len(matrix[0])):
        matrix[3][i] = matrix[0][i]*buf_del + matrix[3][i]
    
    buf_del = - matrix[4][0]
    for i in range(len(matrix[0])):
        matrix[4][i] = matrix[0][i]*buf_del + matrix[4][i]
        
    
                
        
    buf_del = matrix[1][1]
    for i in range(len(matrix[0])):
        matrix[1][i] = matrix[1][i] / buf_del
                       
    buf_del = -matrix[2][1]
    for i in range(len(matrix[0])):
        matrix[2][i] = matrix[1][i]*buf_del + matrix[2][i]
             
    buf_del = -matrix[3][1]
    for i in range(len(matrix[0])):
        matrix[3][i] = matrix[1][i]*buf_del + matrix[3][i]
    
    buf_del = -matrix[4][1]
    for i in range(len(matrix[0])):
        matrix[4][i] = matrix[1][i]*buf_del + matrix[4][i]
        
                     
        
    buf_del = matrix[2][2]
    for i in range(len(matrix[0])):
        matrix[2][i] = matrix[2][i] / buf_del

    buf_del = -matrix[3][2]
    for i in range(len(matrix[0])):
        matrix[3][i] = matrix[2][i]*buf_del + matrix[3][i]
        
    buf_del = -matrix[4][2]
    for i in range(len(matrix[0])):
        matrix[4][i] = matrix[2][i]*buf_del + matrix[4][i]




    buf_del = matrix[3][3]
    for i in range(len(matrix[0])):
        matrix[3][i] = matrix[3][i] / buf_del
              
    buf_del = -matrix[4][3]
    for i in range(len(matrix[0])):
        matrix[4][i] = matrix[3][i]*buf_del + matrix[4][i]



        
    buf_del = matrix[4][4]
    for i in range(len(matrix[0])):
        matrix[4][i] = matrix[4][i] / buf_del



    
        
        
        # Obratnij Hod
    
    
    Na = round(matrix[4][5], 3)
    C = round(matrix[3][5] - matrix[3][4]*Na, 3)
    N = round(matrix[2][5] - matrix[2][3]*C - matrix[2][4]*Na, 3)
    H = round(matrix[1][5] - matrix[1][2]*N - matrix[1][3]*C - matrix[1][4]*Na, 3)
    O = round(matrix[0][5] - matrix[0][1]*H - matrix[0][2]*N - matrix[0][3]*C - matrix[0][4]*Na, 3)
    return [{'el':{'name':him_el[0][0], 'spectrum': him_el[0][1]},'body':O}, {'el':{'name':him_el[1][0], 'spectrum': him_el[1][1]},'body':H}, {'el':{'name':him_el[2][0], 'spectrum': him_el[2][1]},'body':N}, {'el':{'name':him_el[3][0], 'spectrum': him_el[3][1]},'body':C}, {'el':{'name':him_el[4][0], 'spectrum': him_el[4][1]},'body':Na}]

#print(calc_matrix('4.26,4.48,4.4,2.58,3.14', [{'name':'Oxygen','spectrum':'4.0,5.0,5.0,3.1,3.5' },{'name':'Hidrogen','spectrum': '2.0,1.0,2.0,2.5,1.5'},{'name':'Nitrogen','spectrum':'1.0,1.0,1.0,1.0,1.0' },{'name':'Carbon','spectrum': '3.1,3.7,3.5,1.8,2.6'},{'name':'Sodium','spectrum':'5.2,4.5,3.8,4.5,4.9'}]))