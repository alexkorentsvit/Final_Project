def calc_matrix(spectrum_vhid,data):
    spectrum = spectrum_vhid.split(',')
    him_el = []
    for i in range(3):
        him_el.append([data[i].name, data[i].spectrum.split(',')])
    matrix = []
    for i in range(3):
        matrix.append([float(him_el[0][1][i]),float(him_el[1][1][i]),float(him_el[2][1][i]), float(spectrum[i])])
    
    buf_del = matrix[0][0]
    for i in range(len(matrix[0])):
        matrix[0][i] = matrix[0][i] / buf_del
            
    buf_del = - matrix[1][0]
    for i in range(len(matrix[0])):
        matrix[1][i] = matrix[0][i]*buf_del + matrix[1][i]
        
    buf_del = - matrix[2][0]
    for i in range(len(matrix[0])):
        matrix[2][i] = matrix[0][i]*buf_del + matrix[2][i]
    
        
    buf_del = matrix[1][1]
    for i in range(len(matrix[0])):
        matrix[1][i] = matrix[1][i] / buf_del
       
        
        
    buf_del = -matrix[2][1]
    for i in range(len(matrix[0])):
        matrix[2][i] = matrix[1][i]*buf_del + matrix[2][i]
        
        
    buf_del = matrix[2][2]
    for i in range(len(matrix[0])):
        matrix[2][i] = matrix[2][i] / buf_del
        
        
        # Obratnij Hod
    N = round(matrix[2][3], 3)
    H = round(matrix[1][3] - matrix[1][2]*N, 3)
    O = round(matrix[0][3] - matrix[0][1]*H - matrix[0][2]*N, 3)
    return [{'el':{'name':him_el[0][0]},'body':O}, {'el':{'name':him_el[1][0]},'body':H}, {'el':{'name':him_el[2][0]},'body':N}]