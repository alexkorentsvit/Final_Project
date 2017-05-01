from app import db

class Spec(db.Model):
   __tablename__ = "Spectra"
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(64), index = True, unique = True)
   spectrum = db.Column(db.String(120), index = True, unique = True)
   
   def __init__(self, name, spectrum):
       self.name = name
       self.spectrum = spectrum

   
   def __repr__(self):
       return 'Name: ' + str(self.name) + " spectrum: " + str(self.spectrum)

