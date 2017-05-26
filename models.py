from app import db

class Spec(db.Model):
   __tablename__ = "Spectra"
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(64), index = True, unique = True)
   spectrum = db.Column(db.String(120), index = True, unique = True)
   composition = db.Column(db.String(120), index = True, unique = False)
   
   def __init__(self, name, spectrum, composition):
       self.name = name
       self.spectrum = spectrum
       self.composition = composition

   
   def __repr__(self):
       return 'Name: ' + str(self.name) + " spectrum: " + str(self.spectrum)

