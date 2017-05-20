from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class MyForm(Form):
    spectr = TextField('spectr', validators = [Required()])

class MyForm2(Form):
    name_of_spectrum = TextField('name_of_spectrum', validators = [Required()])
    
class MyForm3(Form):
    name_of_spectrum = TextField('name_of_spectrum', validators = [Required()])
    spectr = TextField('spectr', validators = [Required()])
    
