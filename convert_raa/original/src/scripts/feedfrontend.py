from datetime import date, timedelta

import sqlobject
from sqlobject import UnicodeCol, IntCol, DateCol, ForeignKey
from sqlobject import RelatedJoin, MultipleJoin
from sqlobject import SQLObjectNotFound
from sqlobject import AND
from sqlobject.dbconnection import ConnectionHub, connectionForURI

import backend, frontend, datetime_converters

log = open('/tmp/feedfrontend.log', 'w')

def stringToDate(
        year_str, month_str=None, day_str=None, as_end_date=False):
    """
    >>> y, m, d = '2005', '7', '14'
    >>> stringToDate(y, m, d)
    datetime.date(2005, 7, 14)
    >>> y, m, d = '2005', '7', 'xx'
    >>> stringToDate(y, m, d)
    datetime.date(2005, 7, 1)
    >>> y, m, d = '2005', '7', '0'
    >>> stringToDate(y, m, d)
    datetime.date(2005, 7, 1)
    >>> stringToDate(y, m, d, as_end_date=True)
    datetime.date(2005, 7, 31)
    >>> y, m, d = '2005', 'xx', 'xx'
    >>> stringToDate(y, m, d)
    datetime.date(2005, 1, 1)
    >>> y, m, d = '2005', '0', 'xx'
    >>> stringToDate(y, m, d)
    datetime.date(2005, 1, 1)
    >>> stringToDate(y, m, d, as_end_date=True)
    datetime.date(2005, 12, 31)
    >>> y, m, d = '2005', None, None
    >>> stringToDate(y, m, d)
    datetime.date(2005, 1, 1)
    >>> y, m, d = 'foobar', None, None
    >>> stringToDate(y, m, d)
    >>> y, m, d = '0', None, None
    >>> stringToDate(y, m, d)
    """

    try:
        year = int(year_str)
        if not date.min.year <= year <= date.max.year:
            raise ValueError
    except (ValueError, TypeError), e:
        # If we do not even have a year, we just don't have a reasonable
        # date value at all.
        return None

    try:
        month = int(month_str)
        if not 1 <= month <= 12:
            raise ValueError
    except (ValueError, TypeError), e:
        if as_end_date:
            return date(year, 12, 31)
        return date(year, 1, 1)

    try:
        day = int(day_str)
        if not 1 <= day <= 31:
            raise ValueError
    except (ValueError, TypeError), e:
        if as_end_date:
            if month == 12:
                month = 0
                year += 1
            return date(year, month+1, 1) - timedelta(days=1)
        return date(year, month, 1)

    try:
        d = date(year, month, day)
    except ValueError, e:
        print year, month, day
        raise

    return d

def getNamedObject(class_, name, **kwargs):
    if name:
        name = name.encode('utf-8') # the 'q' attributes cannot decode themselves
    query = class_.select(class_.q.naam==name)
    if query.count():
        return query[0] # fetch first item
    return class_(naam=name, **kwargs)

def getNamedLocalObject(class_, name, lokaal, **kwargs):
    if name:
        name = name.encode('utf-8') # the 'q' attributes cannot decode themselves
    query = class_.select(AND(class_.q.naam==name, class_.q.lokaal==lokaal))
    if query.count():
        return query[0] # fetch first item
    return class_(naam=name, lokaal=lokaal, **kwargs)

def aanstellingForPersoonFactory(data, persoon):
    van = stringToDate(data.beginjaar, data.beginmaand, data.begindag)
    known_van = '-'.join(
        [d for d in [data.begindag, data.beginmaand, data.beginjaar] if d])
    tot = stringToDate(
        data.eindjaar, data.eindmaand, data.einddag, as_end_date=True)
    known_tot = '-'.join(
        [d for d in [data.einddag, data.eindmaand, data.eindjaar] if d])

    instelling = functie = None

    try:
        if data.college:
            instelling = getNamedLocalObject(
                frontend.Instelling, data.college.naam, data.college.lokaal,
                toelichting=None
                )
    except SQLObjectNotFound, e:
        log.write(str(e)+' for aanstelling '+str(data.id)+'\n')
        log.flush()
        instelling = None

    try:
        if data.functie:
            functie = getNamedLocalObject(
                frontend.Functie, data.functie.naam, data.functie.lokaal
                )
    except SQLObjectNotFound, e:
        log.write(str(e)+' for aanstelling '+str(data.id)+'\n')
        log.flush()
        functie = None

    regio = provincie = lokaal = stand = periode = None

    if data.provincie:
        provincie = getNamedObject(frontend.Provincie, data.provincie.naam)
    if data.regio:
        regio = getNamedObject(frontend.Regio, data.regio.naam)
    if data.lokaal:
        lokaal = getNamedObject(frontend.Lokaal, data.lokaal.naam)
    if data.stand:
        stand = getNamedObject(frontend.Stand, data.stand.naam)

    aanstelling = frontend.Aanstelling(
        van=van,
        van_als_bekend=known_van,
        tot=tot,
        tot_als_bekend=known_tot,
        persoon=persoon,
        functie=functie,
        instelling=instelling,
        lokaal=lokaal,
        regio=regio,
        provincie=provincie,
        stand=stand,
        vertegenwoordigend=data.vertegenwoordigend,
        opmerkingen=data.opmerkingen,
        )

    return aanstelling

def try_padding(possible_int):
    try:
        return '%02d'%int(possible_int)
    except ValueError as e:
        return possible_int

def persoonFactory(data):

    # list of heerlijkheden
    if data.heerlijkheid:
        heerlijkheden = data.heerlijkheid
        if data.heerlijkheid2:
            heerlijkheden = heerlijkheden + ' en ' + data.heerlijkheid2
    else:
        heerlijkheden = ''

    known_geboortedatum = '-'.join(
        [try_padding(d) for d in [
            data.geboortedag, data.geboortemaand, data.geboortejaar] if d])
    geboortedatum = stringToDate(
        data.geboortejaar, data.geboortemaand, data.geboortedag
        )

    doopjaar = (data.doopjaar == '1')

    known_overlijdensdatum = '-'.join(
        [try_padding(d) for d in [
            data.overlijdensdag, data.overlijdensmaand, data.overlijdensjaar] if d]
        )
    overlijdensdatum = stringToDate(
        data.overlijdensjaar, data.overlijdensmaand, data.overlijdensdag,
        as_end_date=True
        )

    if data.adellijketitel and \
            data.adellijketitel.naam != 'Geen titel' and \
            data.adellijketitel.naam != 'Onbekend' and \
            data.adellijketitel.naam is not None:
        adellijketitel = getNamedObject(
            frontend.AdellijkeTitel, data.adellijketitel.naam.lower())
    elif data.adelspredikaat: # catch the 'Jonkheer' items
        adellijketitel = getNamedObject(
            frontend.AdellijkeTitel, data.adelspredikaat.lower())
    else:
        adellijketitel = None

    if data.academischetitel and \
            data.academischetitel.naam != 'Geen' and \
            data.academischetitel.naam != 'Onbekend' and \
            data.academischetitel.naam is not None:
        academischetitel = getNamedObject(
            frontend.AcademischeTitel, data.academischetitel.naam.lower()
            )
    else:
        academischetitel = None

    searchable = data.geslachtsnaam
    if data.tussenvoegsel:
        searchable = data.tussenvoegsel+' '+searchable

    persoon = frontend.Persoon(
        adel=bool(data.adel),
        heerlijkheid=heerlijkheden,
        voornaam=data.voornaam,
        tussenvoegsel=data.tussenvoegsel,
        geslachtsnaam=data.geslachtsnaam,
        searchable_geslachtsnaam=searchable,
        geboortedatum=geboortedatum,
        geboortedatum_als_bekend=known_geboortedatum,
        geboorteplaats=data.geboorteplaats or None,
        doopjaar=doopjaar,
        overlijdensdatum=overlijdensdatum,
        overlijdensdatum_als_bekend=known_overlijdensdatum,
        overlijdensplaats=data.overlijdensplaats or None,
        adellijketitel=adellijketitel,
        academischetitel=academischetitel,
        opmerkingen=data.opmerkingen,
        )

    _ = [
        frontend.Alias(naam=name, persoon=persoon)
        for name in set([alias.naam for alias in data.aliassen]) if name
        ]

    _ = [
        aanstellingForPersoonFactory(aanstelling, persoon)
        for aanstelling in data.aanstellingen
        ]

    for b in data.bronnen:
       bron = getNamedObject(frontend.Bron, b.bron.naam)
       details = frontend.BronDetails(
           bron=bron,
           persoon=persoon,
           details=b.details
           )

    return persoon

def massage():
    for record in backend.Regent.select():
        persoon = persoonFactory(record)
    print (
        '%s persoon records created, with a total of '
        '%s aanstelling records.') % (
            frontend.Persoon.select().count(),
            frontend.Aanstelling.select().count()
        )

if __name__ == '__main__':
    import sys, optparse
    version = '1.0'
    usage = (
        'usage: %prog [options] SOURCE_DB_URL TARGET_DB_URL\n\nExample:\n\n'
        '  python ./scripts/feedfrontend.py --drop-target \\\n'
        '  "mysql://root@localhost/negentien" \\\n'
        '  "mysql://root@localhost/raa_web2?sqlobject_encoding=latin-1"')
    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option(
        '--drop-target', dest='drop_target', default=False,
        action='store_true', help=(
            'Drop target database to have it recreated. This obviously will '
            'destroy all the data currently in the target database!'))
    parser.add_option(
        '--debug', dest='debug', default=False, action='store_true',
        help=(
            'Print the SQLObject debug messages while creating and '
            'inserting data.'))
    parser.add_option(
        '--test', dest='test', default=False, action='store_true',
        help=('Run internal doctests.'))

    options, urls = parser.parse_args()

    if options.test:
        import doctest
        doctest.testmod()
        sys.exit(0)

    if options.debug:
        urls[1] = urls[1] + '?debug=True'

    backend.hub.threadConnection = connectionForURI(urls[0])
    frontend.hub.threadConnection = connectionForURI(urls[1])

    if options.drop_target:
        frontend.dropTables()
    frontend.createTables()
    massage()
