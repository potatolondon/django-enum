"""
    This class is sort of a C-style enum but with extra magic.

    USAGE:

    class Vegetables(Enum):
        CARROT = "C"
        POTATO = "P"
        CABBAGE = "CA"

    my_veg = Vegetables.CARROT
    assertTrue(my_veg in Vegetables.constants)
    models.CharField(choices=Vegetables.choices)

    If you want nice fancy descriptions for the choices:

    class Vegetables(Enum):
        CARROT = Enum.Entry("CARROT", "An orange vegetable")
        POTATO = Enum.Entry("POTATO", "A root vegetable")

    Vegetables.choices => [ ("CARROT", "An orange vegetable"), ("POTATO", "A root vegetable") ]
    Vegetables.constants => [ "CARROT", "POTATO" ]
    Vegetables.POTATO => "POTATO"
"""

class EnumMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(EnumMetaclass, cls).__new__(cls, name, bases, attrs)
        new_class._constants = []
        new_class._descriptions = {}
        new_class._choices = []

        entries = []
        for attr_name in new_class.__dict__.keys():
            attr = getattr(new_class, attr_name)
            if isinstance(attr, EnumEntry):
                entries.append((attr_name, attr))
        new_class._has_entries = bool(entries)

        entries.sort(key=lambda e: e[1].creation_order)

        for entry_name, entry in entries:
            new_class._constants.append(entry.constant)
            new_class._descriptions[entry.constant] = entry.description

            #Alter the attribute so it can be accessed with NewEnum.MY_CONSTANT
            setattr(new_class, entry_name, entry.constant)

        new_class._choices = [(x, new_class._descriptions[x]) for x in new_class._constants]
        return new_class

    @property
    def choices(cls):
        assert cls._has_entries
        return cls._choices

    @property
    def constants(cls):
        assert cls._has_entries
        return cls._constants

    @property
    def choices_dict(cls):
        assert cls._has_entries
        return dict(cls._choices)


class EnumEntry(object):
    creation_counter = 0

    def __init__(self, constant, desc=None, category=None):
        self.creation_order = Enum.Entry.creation_counter
        Enum.Entry.creation_counter += 1

        self.constant = constant
        self.description = constant if desc is None else desc
        self.category = category

    def __eq__(self, other):
        if isinstance(other, Enum.Entry):
            return super(Enum.Entry, self).__eq__(other)

        return self.constant == other

    def __str__(self):
        return str(self.constant)

    def __unicode__(self):
        return unicode(self.constant)


class Enum(object):
    __metaclass__ = EnumMetaclass

    Entry = EnumEntry

    @classmethod
    def subset(cls, *args):
        assert cls._has_entries
        return [(entry, cls.choices_dict[entry]) for entry in args]

    @classmethod
    def all_except(cls, *args):
        assert cls._has_entries
        return [(entry, cls.choices_dict[entry]) for entry in cls._constants if entry not in args]
