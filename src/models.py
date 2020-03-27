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
