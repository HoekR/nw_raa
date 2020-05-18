# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AcademischeTitel(Base):
    __tablename__ = 'academische_titel'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class AdellijkeTitel(Base):
    __tablename__ = 'adellijke_titel'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class AdelsPredikaat(Base):
    __tablename__ = 'adels_predikaat'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class Bron(Base):
    __tablename__ = 'bron'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class College(Base):
    __tablename__ = 'college'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), unique=True)


class Functie(Base):
    __tablename__ = 'functie'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255))
    lokaal = Column(Integer)


class Instelling(Base):
    __tablename__ = 'instelling'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255))
    toelichting = Column(Text)
    lokaal = Column(Integer)


class InstellingCopy(Base):
    __tablename__ = 'instelling_copy'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255))
    toelichting = Column(Text)
    lokaal = Column(Integer)


class Lokaal(Base):
    __tablename__ = 'lokaal'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class Periode(Base):
    __tablename__ = 'periode'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class Provincie(Base):
    __tablename__ = 'provincie'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class Regent(Base):
    __tablename__ = 'regent'

    id = Column(Integer, primary_key=True)
    heerlijkheid = Column(Text)
    adelspredikaat = Column(Text)
    voornaam = Column(Text)
    tussenvoegsel = Column(Text)
    geslachtsnaam = Column(Text)
    geboortejaar = Column(Date)
    geboortejaar_als_bekend = Column(Text)
    overlijdensjaar = Column(Date)
    overlijdensjaar_als_bekend = Column(Text)
    adellijketitel_id = Column(Integer)
    academischetitel_id = Column(Integer)


class Regio(Base):
    __tablename__ = 'regio'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class Stand(Base):
    __tablename__ = 'stand'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True)


class Persoon(Base):
    __tablename__ = 'persoon'

    id = Column(Integer, primary_key=True)
    adel = Column(Integer)
    heerlijkheid = Column(Text)
    voornaam = Column(Text)
    tussenvoegsel = Column(Text)
    geslachtsnaam = Column(Text)
    searchable_geslachtsnaam = Column(Text)
    geboortedatum = Column(Date)
    geboortedatum_als_bekend = Column(Text)
    geboorteplaats = Column(Text)
    doopjaar = Column(Integer)
    overlijdensdatum = Column(Date)
    overlijdensdatum_als_bekend = Column(Text)
    overlijdensplaats = Column(Text)
    adellijketitel_id = Column(ForeignKey('adellijke_titel.id'), index=True)
    academischetitel_id = Column(ForeignKey('academische_titel.id'), index=True)
    opmerkingen = Column(Text)
    adelspredikaat = Column(String(256))
    eindcontrole = Column(String(256))
    geboortedag = Column(String(256))
    geboortejaar = Column(String(256))
    geboortemaand = Column(String(256))
    old_idacademischetitel = Column(String(256))
    old_idadellijketitel = Column(String(256))
    old_idregent = Column(String(256))
    overlijdensdag = Column(String(256))
    overlijdensjaar = Column(String(256))
    overlijdensmaand = Column(String(256))
    periode = Column(String(256))
    searchable = Column(String(256))

    academischetitel = relationship('AcademischeTitel')
    adellijketitel = relationship('AdellijkeTitel')


class Aanstelling(Base):
    __tablename__ = 'aanstelling'

    id = Column(Integer, primary_key=True)
    van = Column(Date)
    van_als_bekend = Column(Text)
    tot = Column(Date)
    tot_als_bekend = Column(Text)
    persoon_id = Column(ForeignKey('persoon.id'), index=True)
    functie_id = Column(ForeignKey('functie.id'), index=True)
    instelling_id = Column(ForeignKey('instelling.id'), index=True)
    regio_id = Column(ForeignKey('regio.id'), index=True)
    provincie_id = Column(ForeignKey('provincie.id'), index=True)
    lokaal_id = Column(ForeignKey('lokaal.id'), index=True)
    stand_id = Column(ForeignKey('stand.id'), index=True)
    vertegenwoordigend = Column(Integer)
    opmerkingen = Column(Text)
    begindag = Column(String(256))
    beginjaar = Column(String(256))
    beginmaand = Column(String(256))
    einddag = Column(String(256))
    eindjaar = Column(String(256))
    eindmaand = Column(String(256))
    old_id = Column(String(256))
    old_idcollege = Column(String(256))
    old_idfunctie = Column(String(256))
    old_idregent = Column(String(256))
    old_lokaal = Column(String(256))
    old_provinciaal = Column(String(256))
    old_regio = Column(String(256))
    old_stand = Column(String(256))
    old_vertegenwoordigend = Column(String(256))
    periode = Column(String(256))
    provinciaal = Column(String(256))
    regio = Column(String(256))
    stand = Column(String(256))
    regent_id = Column(String(256))

    functie = relationship('Functie')
    instelling = relationship('Instelling')
    lokaal = relationship('Lokaal')
    persoon = relationship('Persoon')
    provincie = relationship('Provincie')
    regio1 = relationship('Regio')
    stand1 = relationship('Stand')


class Alia(Base):
    __tablename__ = 'alias'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255))
    persoon_id = Column(ForeignKey('persoon.id'), index=True)
    old_idpersoon = Column(String(256))

    persoon = relationship('Persoon')


class BronDetail(Base):
    __tablename__ = 'bron_details'

    id = Column(Integer, primary_key=True)
    details = Column(Text)
    bron_id = Column(ForeignKey('bron.id'), index=True)
    persoon_id = Column(ForeignKey('persoon.id'), index=True)
    old_idregent = Column(String(256))
    old_idbron = Column(String(256))
    regent_id = Column(String(256))

    bron = relationship('Bron')
    persoon = relationship('Persoon')


class BronRegent(Base):
    __tablename__ = 'bron_regent'

    id = Column(Integer, primary_key=True)
    bron_id = Column(ForeignKey('aanstelling.id'), nullable=False, index=True)
    persoon_id = Column(ForeignKey('persoon.id'), nullable=False, index=True)

    bron = relationship('Aanstelling')
    persoon = relationship('Persoon')
