import math
from flask import render_template, flash, redirect, session, request, url_for
from app import app
from app import db
from forms import MyForm, MyForm2, MyForm3
from logic import calc_matrix
from models import Spec



data = Spec.query.all()



@app.route('/Determinetion', methods = ['GET', 'POST'])
def login():
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


@app.route('/')
@app.route('/Info1')
def info1():
    user = { 'nickname': 'Alex' }
    return render_template('Info1.html',
        title = 'Information',
        user = user)


    
    
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
                           flag = flag
                           )



@app.route('/res2', methods = ['GET', 'POST'])
def res2():
    data = Spec.query.all()
    outputs = session.get('output', None)
    spectra = session.get('spectra', None)
    
    return render_template('res2.html', 
                               title = 'result',
                               outputs = outputs,
                               spectra = spectra,
                               data = data
                               )
    
    
@app.route('/substance')
def substance():
    name = session.get('name', None)
    spectra = session.get('spectra', None)
    add = Spec(name, spectra)
    db.session.add(add)
    db.session.commit()
    data = Spec.query.all()
    return render_template('substance.html', 
    title = 'substance',
    name = name,
    spectra = spectra,
    data = data
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
            
             new_spectrum = Spec(form.name_of_spectrum.data, form.spectr.data)
             db.session.add(new_spectrum)
             db.session.commit()
             return redirect(url_for("DataBase"))
        else:
            return render_template('add.html', 
                                   title = 'Add the spectrum',
                                   form = form,
                                   )