def make_fullname(self):
    voorvoegsels = [getattr(self.record.academischetitel, "AcademischeTitel", ""),
                    self.record.Voornaam,
                    getattr(self.record.adellijketitel, "AdellijkeTitel", ""),
                    self.record.Tussenvoegsel]
    voorvoegsel = ' '.join([v for v in voorvoegsels if v]).strip()
    achtervoegsels = [self.record.Heerlijkheid, self.record.Heerlijkheid2]
    achtervoegsel = ' '.join([a for a in achtervoegsels if a]).strip()
    if achtervoegsel:
        achtervoegsel = ", Heer van " + achtervoegsel
    fullname_parts = {"prepos":voorvoegsel,
                      "name": f"{self.record.Geslachtsnaam}",
                      "postpos": achtervoegsel}
    return fullname_parts


def make_aanstellingen(self):
    """this prepares the aanstellingen that are retrieved only at calling time.
    Aanstellingen are sorted by start date"""
    for aanstelling in self.record.bovenlokaalcollegeregentdetails_collection:
        college = getattr(aanstelling.college, "College", "")
        college_ref = getattr(aanstelling.college, "IDCollege", 0) # so that we can refer to the institution
        aanstelling_ref = getattr(aanstelling, "ID")
        functie = {'college': college,
                   'college_ref': college_ref,
                   'aanstelling_ref': aanstelling_ref,
                   'functie': getattr(aanstelling.functie, 'Functie', ''),
                   'functie_ref': getattr(aanstelling, "IDFunctie", ''),
                   'startdate':  '{bjaar}-{bmaand}-{bdag}'.format(bjaar=aanstelling.Beginjaar, # should we get a min_date?
                                                             bmaand=aanstelling.Beginmaand,
                                                             bdag=aanstelling.Begindag),
                   'starty':aanstelling.Beginjaar,
                   'startm':aanstelling.Beginmaand,
                   'startd':aanstelling.Begindag,
                   'enddate':  '{ejaar}-{emaand}-{edag}'.format(ejaar=aanstelling.Eindjaar,
                                                             emaand=aanstelling.Eindmaand,
                                                             edag=aanstelling.Einddag),
                   'endy':aanstelling.Eindjaar,
                   'endm':aanstelling.Eindmaand,
                   'endd':aanstelling.Einddag
                    }
        self.aanstellingen.append(functie)
    sorted(self.aanstellingen, key=lambda x: (x.get("starty"), x.get("startm"), x.get("startd")))


class Persoon(object):
    def __init__(self, record):
        self.record = record
        self.aanstellingen = []
        self.references = []
        self.fullname = self.get_fullname()
        self.normalized_fullname = self.get_fullname_normalized()


    def make_fullname(self):
        return make_fullname(self)

    def get_fullname_normalized(self):
        parts = self.make_fullname()
        fullname_normalized = ''.join((parts['name'], parts['postpos'] , ", ", parts['prepos']))
        return fullname_normalized

    def get_fullname(self):
        parts = self.make_fullname()
        fullname = ''.join((parts['prepos'], ' ', parts['name'], parts['postpos'])).strip()
        return fullname

    def get_references(self):
        if not self.references:
            for reference in self.record.bronregentdetails_collection:
                bron = reference.bron.Bron
                d_en_p = getattr(reference.bron, "deel en paginanummer", '')
                if d_en_p:
                    rf = f"{bron}, {d_en_p}"
                else:
                    rf = f"{bron}"
                self.references.append(rf)
        return self.references

    def get_aanstellingen(self):
        if not self.aanstellingen:
            make_aanstellingen(self)
        return self.aanstellingen

    def repr(self):
        result = {k:getattr(self.record, k) for k in self.record.__table__.columns.keys()}
        result['fullname'] = self.get_fullname()
        result['normalized_fullname'] = self.get_fullname_normalized()
        result['references'] = self.get_references()
        result['aanstellingen'] = self.get_aanstellingen()
        return result

    def __getattr__(self, fieldname):
        """this mirrors the record object"""
        if fieldname in self.record.keys():
            return getattr(self.record, fieldname, '')
        elif fieldname in ['fullname', 'normalized_fullname']:
            return getattr(self, fieldname, '')
        elif fieldname == 'references':
            return self.get_references()
        elif fieldname == 'aanstellingen':
            return self.get_aanstellingen()
        else:
            raise AttributeError

    def __repr__(self):
        nm = self.get_fullname()
        nm = nm + f"({self.Geboortejaar or '?'}, {self.Overlijdensjaar or '?'})"
        return nm


class Aanstelling(object):

    def __init__(self, record):
        self.record = record

    def get_aanstelling(self):
        aanstelling = self.record
        #for aanstelling in self.record:
        college = getattr(aanstelling.college, "College", "")
        college_ref = getattr(aanstelling.college, "IDCollege", 0) # so that we can refer to the institution
        regent = Persoon(aanstelling.regent).get_fullname()
        regent_ref = getattr(aanstelling, "IDRegent")
        functie_ref = getattr(aanstelling, "IDFunctie")
        functie = getattr(aanstelling.functie, "Functie", "")

        functie = {'regent': regent,
                   'regent_ref': regent_ref,
                   'college': college,
                   'college_ref': college_ref,
                   'functie': functie,
                   'functie_ref': functie_ref,
                   'aanstelling_ref': getattr(aanstelling, "ID"),
                   'startdate':  '{bjaar}-{bmaand}-{bdag}'.format(bjaar=aanstelling.Beginjaar, # should we get a min_date?
                                                             bmaand=aanstelling.Beginmaand,
                                                             bdag=aanstelling.Begindag),
                   'starty':aanstelling.Beginjaar,
                   'startm':aanstelling.Beginmaand,
                   'startd':aanstelling.Begindag,
                   'enddate':  '{ejaar}-{emaand}-{edag}'.format(ejaar=aanstelling.Eindjaar,
                                                             emaand=aanstelling.Eindmaand,
                                                             edag=aanstelling.Einddag),
                   'endy':aanstelling.Eindjaar,
                   'endm':aanstelling.Eindmaand,
                   'endd':aanstelling.Einddag
                    }
        #self.aanstellingen.append(functie)
        #sorted(self.aanstellingen, key=lambda x: (x.get("starty"), x.get("startm"), x.get("startd")))
        return functie



class College(object):

    def __init__(self, record):
        self.record = record
        self.aanstellingen = []

    def get_aanstellingen(self):
        if not self.aanstellingen:
            make_aanstellingen(self)
        return self.aanstellingen

    def repr(self):
        result = {
            "college": getattr(self.record, 'College', ''),
            "college_ref": getattr(self.record, "IDCollege"),
            "aanstellingen": self.get_aanstellingen()
            }
        return result
