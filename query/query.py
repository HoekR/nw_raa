from app import db.session # do we do this here?
from .tables import *


def q_aanstelling_onyrs(bj=1492, ej=1862):
    """aanstellingen for fixed period"""
    results = db.session.query(bovenlokaalcollegeregentdetails
                          ).join(college
                          ).join(regent
                          ).filter(bovenlokaalcollegeregentdetails.Beginjaar >= bj
                          ).filter(bovenlokaalcollegeregentdetails.Eindjaar <= ej)
    return results


def query_regent_name(qs="", fuzzy=False):
    """simple regent name search """
    if fuzzy == False:
        results = db.session.query(regent).filter(regent.Geslachtsnaam == qs).all()
    else:
        results = db.session.query(regent).filter(regent.Geslachtsnaam.like(f"%{qs}%")).all()
    return results

def query_college_functienaam(college, functienaam):
    db.session.query(bovenlokaalcollegeregentdetails
                    ).join(college
                    ).filter(college.College.like(f"%{college}%")
                    ).join(functie
                    ).filter(functie.Functie == functienaam)


def query_aanstelling_functie(functienaam):
    results = db.session.query(bovenlokaalcollegeregentdetails
                              ).join(functie
                              ).filter(functie.Functie.like(f'%{functienaam}%'))
    return results


def get_colleges(qs=''):
    colleges = db.session.query(college
                                ).join(bovenlokaalcollegeregentdetails
                                ).filter(college.College.like(f"%{qs}%"))
    return colleges
