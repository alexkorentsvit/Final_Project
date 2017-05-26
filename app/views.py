import pylab as plt
from flask import render_template, flash, redirect, session, request, url_for, send_file
from app import app
from app import db
from forms import MyForm, MyForm2, MyForm3
from logic import calc_matrix
from models import Spec



filename = '/home/alex/Документы/Recognition_of_substances/app/static/fonts/graphic.png'
data = Spec.query.all()

@app.route('/')
@app.route('/Info1')
def info1():
    user = { 'nickname': 'Alex' }
    return render_template('Info1.html',
        title = 'Information',
        user = user)
    

@app.route('/Determinetion', methods = ['GET', 'POST'])
def Determinetion():
    data = Spec.query.all()
    form = MyForm()
    flag = False
    if form.validate_on_submit():
        
        prov = form.spectr.data.split(',')
        for i in range(len(prov)):
            try:
                float(prov[i])
            except ValueError:
                return render_template('Determinetion.html', 
                               title = 'Determine the composition',
                               form = form,
                               flag = True)
            
        for i in range(len(data)):
            if form.spectr.data == data[i].spectrum:
                session['output'] = [{'el':{'name':data[i].name},'body':1.0}]
                flag = True
                break
        if calc_matrix(form.spectr.data,data)[0]['body'] + calc_matrix(form.spectr.data,data)[1]['body'] + calc_matrix(form.spectr.data,data)[2]['body'] <= 1.01 and  calc_matrix(form.spectr.data,data)[0]['body'] + calc_matrix(form.spectr.data,data)[1]['body'] + calc_matrix(form.spectr.data,data)[2]['body'] >= 0.98 and flag == False:
            session['output'] = calc_matrix(form.spectr.data,data)
        elif flag == False:
            session['output'] = "Can't identify the spectrum"
        session['spectra'] = form.spectr.data
        if len(session['output']) == 1:
            return redirect('/res2')
        return redirect('/res')
    else:
        return render_template('Determinetion.html', 
                               title = 'Determine the composition',
                               form = form)





    
  
@app.route('/res', methods = ['GET', 'POST'])
def res():
    form2 = MyForm2()
    flag = False
    outputs = session.get('output', None)
    spectra = session.get('spectra', None)
    data = Spec.query.all()
    
    if len(outputs) == 3:
        i = 0
        n = 0
        while n < 3:
            if outputs[i]['body'] == 0.0:
                del outputs[i]
                n += 1
            else:
                i += 1
                n += 1
                
    simple = [1,2,3]            
    Vhid = spectra.split(',')
    for i in range(len(Vhid)):
        Vhid[i] = float(Vhid[i])
    
    
        
    plt.figure('New')
    plt.clf()
    plt.title('New')
    plt.xlabel('wavelength')
    plt.ylabel('intensity')
    
    for i in range(len(outputs)):
        plt.plot(simple, outputs[i]['el']['spectrum'], label = outputs[i]['el']['name'])
    
    plt.plot(simple, Vhid, label = 'New')
    plt.legend()
    plt.savefig(filename)
    


    
    if form2.validate_on_submit():
        for i in range(len(data)):
            if form2.name_of_spectrum.data == data[i].name:
                flag = True
        
        if flag == False:
            for i in range(len(data)):
                if spectra == data[i].spectrum:                    
                    db.session.delete(data[i])
                    db.session.commit()
            session['name'] = form2.name_of_spectrum.data
            return redirect('/substance')       
    return render_template('res.html', 
                           title = 'result',
                           form2 = form2,
                           outputs = outputs,
                           flag = flag,
                           filename = filename
                           )




    
    
@app.route('/substance')
def substance():
    composition = ''
    name = session.get('name', None)
    spectra = session.get('spectra', None)
    outputs = session.get('output', None)
    for i in range(len(outputs)):
        composition += outputs[i]['el']['name']
        composition += ':'
        composition += str(outputs[i]['body'])
        composition += ' '
        
    
    add = Spec(name, spectra, composition[:-1])
    db.session.add(add)
    db.session.commit()
    data = Spec.query.all()
    return render_template('substance.html', 
    title = 'substance',
    name = name,
    spectra = spectra,
    data = data
    )
    
    
    
    
@app.route('/res2', methods = ['GET', 'POST'])
def res2():
    data = Spec.query.all()
    outputs = session.get('output', None)
    spectra = session.get('spectra', None)
    
    for i in range(len(data)):
        if data[i].spectrum == spectra:
            label = data[i].name
            buf = data[i].composition.split(' ')
    
    elements_dict = []
    data_el = []
    for i in range(len(buf)):
        data_el.append(buf[i].split(':'))
        for j in range(len(data)):
            if data[j].name == data_el[i][0]:
                elements_dict.append({'el':{'name':data_el[i][0],'spectrum': data[j].spectrum.split(',')}, 'body': data_el[i][1]})
        
        
    for i in range(len(elements_dict)):
        for j in range(len(elements_dict[i]['el']['spectrum'])):
            elements_dict[i]['el']['spectrum'][j] = float(elements_dict[i]['el']['spectrum'][j]) 
    
    simple = [1,2,3]            
    Vhid = spectra.split(',')
    for i in range(len(Vhid)):
        Vhid[i] = float(Vhid[i])
       
    plt.figure(label)
    plt.clf()
    plt.title(label)
    plt.xlabel('wavelength')
    plt.ylabel('intensity')
    
    for i in range(len(elements_dict)):
        plt.plot(simple, elements_dict[i]['el']['spectrum'], label = elements_dict[i]['el']['name'])
    
    plt.plot(simple, Vhid, label = label)
    plt.legend()
    plt.savefig(filename)
    
    
    return render_template('res2.html', 
                               title = 'result',
                               outputs = outputs,
                               spectra = spectra,
                               data = data,
                               filename = filename,
                               elements_dict = elements_dict
                               )



@app.route('/DataBase', methods = ['GET', 'POST'])
def DataBase():
    if request.method == "GET":
        data = Spec.query.all()
        return render_template('DataBase.html', 
                               title = 'Database',
                               data = data
                               )
        
        
    elif request.method == "POST":        
        if request.form["id"]:
            Spec.query.filter(Spec.id == request.form["id"]).delete()
            db.session.commit()
            data = Spec.query.all()
            return render_template('DataBase.html', 
                              title = 'Database',
                              data = data
                              )
        
        
            
            
@app.route('/add', methods = ['GET', 'POST'])
def addspectrum():
        form = MyForm3(request.form)
        if request.method == "POST":
             prov = form.spectr.data.split(',')
             for i in range(len(prov)):
                 try:
                     float(prov[i])
                 except ValueError:
                         return render_template('add.html', 
                                                title = 'Add the spectrum',
                                                form = form,
                                                flag1 = True)
             for i in range(len(data)):
                 if form.name_of_spectrum.data == data[i].name:
                     return render_template('add.html', 
                                            title = 'Add the spectrum',
                                            form = form,
                                            flag2 = True)
                     
             for i in range(len(data)):
                 if form.spectr.data == data[i].spectrum:
                    return render_template('add.html', 
                                            title = 'Add the spectrum',
                                            form = form,
                                            flag3 = True)
            
             new_spectrum = Spec(form.name_of_spectrum.data, form.spectr.data, None)
             db.session.add(new_spectrum)
             db.session.commit()
             return redirect(url_for("DataBase"))
        else:
            return render_template('add.html', 
                                   title = 'Add the spectrum',
                                   form = form,
                                   )
            



@app.route('/Graphics', methods = ['GET', 'POST'])
def Graphics():
    if request.method == "GET":
        data = Spec.query.all()
        return render_template('Graphics.html', 
                               title = 'Graphics',
                               data = data
                               )
        
        
    elif request.method == "POST": 
        data = Spec.query.all()
        flag = False
        for i in range(len(data)):
            if str(i+1) == request.form["id"]:
                Vhid = data[i].spectrum.split(',')
                label = data[i].name
                try:
                    buf = data[i].composition.split(' ')
                except AttributeError:
                    flag = True
                    
        simple = [1,2,3]            
        for i in range(len(Vhid)):
            Vhid[i] = float(Vhid[i]) 
            
        if flag == False:        
            elements_dict = []
            data_el = []
            for i in range(len(buf)):
                data_el.append(buf[i].split(':'))
                for j in range(len(data)):
                    if data[j].name == data_el[i][0]:
                        elements_dict.append({'el':{'name':data_el[i][0],'spectrum': data[j].spectrum.split(',')}, 'body': data_el[i][1]})
                
                
            for i in range(len(elements_dict)):
                for j in range(len(elements_dict[i]['el']['spectrum'])):
                    elements_dict[i]['el']['spectrum'][j] = float(elements_dict[i]['el']['spectrum'][j]) 
            
            simple = [1,2,3]            
            plt.figure(label)
            plt.clf()
            plt.title(label)
            plt.xlabel('wavelength')
            plt.ylabel('intensity')
            
            for i in range(len(elements_dict)):
                plt.plot(simple, elements_dict[i]['el']['spectrum'], label = elements_dict[i]['el']['name'])
                plt.text(2.25, 4.5-i/2,elements_dict[i]['el']['name'] + ' Proportion: ' + elements_dict[i]['body'])
            plt.plot(simple, Vhid, label = label)
            plt.legend()
            plt.savefig(filename)         
            return send_file(filename, mimetype='image/png')
        
        
        else:
            plt.figure(label)
            plt.clf()
            plt.title(label)
            plt.xlabel('wavelength')
            plt.ylabel('intensity')
            
            
            plt.plot(simple, Vhid, label = 'label')
            plt.legend()
            plt.savefig(filename)
            return send_file(filename, mimetype='image/png')





@app.route("/home/alex/Документы/Recognition_of_substances/app/static/fonts/grafic.png")
def show_icon():
     return send_file(filename, mimetype='image/png')
    
    
    
    
