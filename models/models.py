def make_fullname(self):
    voorvoegsels = [getattr(self.record.academischetitel_id, "AcademischeTitel", ""),
                    self.record.voornaam,
                    getattr(self.record.adellijketitel_id, "AdellijkeTitel", ""),
                    self.record.tussenvoegsel]
    voorvoegsel = ' '.join([v for v in voorvoegsels if v]).strip()
    achtervoegsels = [self.record.heerlijkheid]
    achtervoegsel = ' '.join([a for a in achtervoegsels if a]).strip()
    if achtervoegsel:
        achtervoegsel = ", Heer van " + achtervoegsel
    fullname_parts = {"prepos": voorvoegsel,
                      "name": f"{self.record.geslachtsnaam}",
                      "postpos": achtervoegsel}
    return fullname_parts


def make_aanstellingen(self):
    """this prepares the aanstellingen that are retrieved only at calling time.
    Aanstellingen are sorted by start date"""
    for aanstelling in self.record.aanstelling_collection:
        college = getattr(aanstelling.instelling, "naam", "")
        college_ref = getattr(aanstelling.instelling, "id", 0)  # so that we can refer to the institution
        aanstelling_ref = getattr(aanstelling, "id")
        functie = {'college': college,
                   'college_ref': college_ref,
                   'aanstelling_ref': aanstelling_ref,
                   'functie': getattr(aanstelling.functie, 'Functie', ''),
                   'functie_ref': getattr(aanstelling, "functie_id", ''),
                   'startdate': aanstelling.van,
                   'start_text': aanstelling.van_als_bekend,
                   'enddate': aanstelling.tot,
                   'end_text': aanstelling.tot_als_bekend,
                   }
        self.aanstellingen.append(functie)
    sorted(self.aanstellingen, key=lambda x: x.get("start_text"))


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
        fullname_normalized = ''.join((parts['name'], parts['postpos'], ", ", parts['prepos']))
        return fullname_normalized

    def get_fullname(self):
        parts = self.make_fullname()
        fullname = ''.join((parts['prepos'], ' ', parts['name'], parts['postpos'])).strip()
        return fullname

    def get_references(self):
        if not self.references:
            for reference in self.record.bron_details_collection:
                bron = reference.bron.naam
                d_en_p = getattr(reference, "details", '')
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
        result = {k: getattr(self.record, k) for k in self.record.__table__.columns.keys()}
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
        # for aanstelling in self.record:
        college = getattr(aanstelling.instelling, "naam", "")
        college_ref = getattr(aanstelling, "instelling_id", 0)  # so that we can refer to the institution
        regent = Persoon(aanstelling.persoon).get_fullname()
        regent_ref = getattr(aanstelling, "persoon_id")
        functie_ref = getattr(aanstelling, "functie_id")
        functie = getattr(aanstelling.functie, "naam", "")

        functie = {'regent': regent,
                   'regent_ref': regent_ref,
                   'college': college,
                   'college_ref': college_ref,
                   'functie': functie,
                   'functie_ref': functie_ref,
                   'startdate': aanstelling.van,
                   'start_text': aanstelling.van_als_bekend,
                   'enddate': aanstelling.tot,
                   'end_text': aanstelling.tot_als_bekend,
                   }
        return functie

    def repr(self):
        return self.get_aanstelling()


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
            "college": getattr(self.record, 'naam', ''),
            "college_ref": getattr(self.record, "id")
        }
        return result