# from app import session # do we do this here?
from ..models.tables import *
from ..models.models import *
from flask import abort
from datetime import date

def make_date_from_year(year, yrtype='start'):
    if yrtype == 'start':
        m = 1
        d = 1
    else:
        m = 12
        d = 31
    dt = date(year=year, month=m, day=d)
    return dt

filters = {"aanstelling":
               {"bj": aanstelling.van,
                "ej": aanstelling.van,
                "functie": functie.naam,
                "instelling": instelling.naam,
                "from": aanstelling.van,
                "to": aanstelling.tot,

                }}


def get_regent_by_id(session, regent_id: int = 0):
    results = session.query(persoon).get(regent_id)
    if results is None:
        abort(404)
    return results


def query_regent_name(session, qs="", fuzzy=False):
    """simple regent name search """
    if fuzzy == False:
        results = session.query(persoon).filter(persoon.geslachtsnaam == qs).all()
    else:
        results = session.query(persoon).filter(persoon.geslachtsnaam.like(f"%{qs}%")).all()
    return results


def get_aanstelling_by_id(session, aanstelling_id: int = 0):
    results = session.query(aanstelling
                            ).join(instelling
                                   ).join(persoon
                                          ).join(functie
                                                 ).filter(aanstelling.id == aanstelling_id).all()
    if results is None:
        abort(404)
    return results


def q_aanstelling_onyrs(session, bj=1492, ej=1862):
    """aanstellingen for fixed period"""
    flts = filters['aanstelling']
    bj = make_date_from_year(bj)
    ej = make_date_from_year(ej)
    results = session.query(aanstelling
                            ).join(instelling
                            ).join(persoon
                            ).filter(flts['bj'] >= bj
                            ).filter(flts['ej'] <= ej)
    results = results.order_by(aanstelling.van, instelling.naam)
    if results is None:
        abort(404)

    return results


def q_aanstelling_general(session, params):
    flts = filters['aanstelling']
    for p in params:
        print (p)
    results = session.query(aanstelling
                            ).join(instelling
                                   ).join(persoon
                                          ).filter(*filters)

    if results is None:
        abort(404)
    return results


def query_instelling_functienaam(session, instelling, functienaam):
    session.query(aanstelling
                  ).join(instelling
                         ).filter(instelling.naam.like(f"%{instelling}%")
                                  ).join(functie
                                         ).filter(functie.naam == functienaam)


def query_aanstelling_functie(session, functienaam):
    results = session.query(aanstelling
                            ).join(functie
                                   ).filter(functie.naam.like(f'%{functienaam}%'))
    return results


def get_college_names(session, period=-1):
    results = session.query(instelling)
    #if period > -1:
    #    results = results.filter_by(periode=period)
    return results

def get_college_by_id(session, instelling_id: int = 0):
    results = session.query(instelling).get(instelling_id)
    return results


def get_college_by_name(session, qs='', fuzzy=False):
    colleges = session.query(instelling
                             ).join(aanstelling
                                    ).filter(instelling.naam.like(f"%{qs}%"))
    return colleges


def get_function_names(session, period=-1):
    results = session.query(functie)
    if period > -1:
        results = results.filter_by(periode=period)
    return results

def get_period_names(session):
    results = session.query(periode)
    return results

