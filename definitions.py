# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AcademischeTitel(Base):
    __tablename__ = 'academische_titel'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class AdellijkeTitel(Base):
    __tablename__ = 'adellijke_titel'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class AdelsPredikaat(Base):
    __tablename__ = 'adels_predikaat'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class Bron(Base):
    __tablename__ = 'bron'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class College(Base):
    __tablename__ = 'college'

    id = Column(Integer, primary_key=True)
    naam = Column(String(255), unique=True)


class Functie(Base):
    __tablename__ = 'functie'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255))
    lokaal = Column(TINYINT)


class Instelling(Base):
    __tablename__ = 'instelling'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255))
    toelichting = Column(Text)
    lokaal = Column(TINYINT)


class InstellingCopy(Base):
    __tablename__ = 'instelling_copy'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255))
    toelichting = Column(Text)
    lokaal = Column(TINYINT)


class Lokaal(Base):
    __tablename__ = 'lokaal'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class Periode(Base):
    __tablename__ = 'periode'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class Provincie(Base):
    __tablename__ = 'provincie'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class Regent(Base):
    __tablename__ = 'regent'

    id = Column(INTEGER, primary_key=True)
    heerlijkheid = Column(Text)
    adelspredikaat = Column(Text)
    voornaam = Column(Text)
    tussenvoegsel = Column(Text)
    geslachtsnaam = Column(Text)
    geboortejaar = Column(Date)
    geboortejaar_als_bekend = Column(Text)
    overlijdensjaar = Column(Date)
    overlijdensjaar_als_bekend = Column(Text)
    adellijketitel_id = Column(INTEGER)
    academischetitel_id = Column(INTEGER)


class Regio(Base):
    __tablename__ = 'regio'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class Stand(Base):
    __tablename__ = 'stand'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255), nullable=False, unique=True, server_default=text("''"))


class Persoon(Base):
    __tablename__ = 'persoon'

    id = Column(INTEGER, primary_key=True)
    adel = Column(TINYINT)
    heerlijkheid = Column(Text)
    voornaam = Column(Text)
    tussenvoegsel = Column(Text)
    geslachtsnaam = Column(Text)
    searchable_geslachtsnaam = Column(Text)
    geboortedatum = Column(Date)
    geboortedatum_als_bekend = Column(Text)
    geboorteplaats = Column(Text)
    doopjaar = Column(TINYINT)
    overlijdensdatum = Column(Date)
    overlijdensdatum_als_bekend = Column(Text)
    overlijdensplaats = Column(Text)
    adellijketitel_id = Column(ForeignKey('adellijke_titel.id'), index=True)
    academischetitel_id = Column(ForeignKey('academische_titel.id'), index=True)
    opmerkingen = Column(Text)

    academischetitel = relationship('AcademischeTitel')
    adellijketitel = relationship('AdellijkeTitel')


class Aanstelling(Base):
    __tablename__ = 'aanstelling'

    id = Column(INTEGER, primary_key=True)
    van = Column(Date)
    van_als_bekend = Column(Text)
    tot = Column(Date)
    tot_als_bekend = Column(Text)
    persoon_id = Column(ForeignKey('persoon.id'), index=True)
    functie_id = Column(ForeignKey('functie.id'), index=True)
    instelling_id = Column(ForeignKey('instelling.id'), index=True)
    regio_id = Column(INTEGER)
    provincie_id = Column(INTEGER)
    lokaal_id = Column(INTEGER)
    stand_id = Column(INTEGER)
    vertegenwoordigend = Column(TINYINT)
    opmerkingen = Column(Text)

    functie = relationship('Functie')
    instelling = relationship('Instelling')
    persoon = relationship('Persoon')


class Alia(Base):
    __tablename__ = 'alias'

    id = Column(INTEGER, primary_key=True)
    naam = Column(String(255))
    persoon_id = Column(ForeignKey('persoon.id'), index=True)

    persoon = relationship('Persoon')


class BronDetail(Base):
    __tablename__ = 'bron_details'

    id = Column(INTEGER, primary_key=True)
    details = Column(Text)
    bron_id = Column(ForeignKey('bron.id'), index=True)
    persoon_id = Column(ForeignKey('persoon.id'), index=True)

    bron = relationship('Bron')
    persoon = relationship('Persoon')


class BronRegent(Base):
    __tablename__ = 'bron_regent'

    id = Column(INTEGER, primary_key=True)
    bron_id = Column(ForeignKey('aanstelling.id'), nullable=False, index=True, server_default=text("'0'"))
    persoon_id = Column(ForeignKey('persoon.id'), nullable=False, index=True, server_default=text("'0'"))

    bron = relationship('Aanstelling')
    persoon = relationship('Persoon')
