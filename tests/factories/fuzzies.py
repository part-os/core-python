"""CUSTOM PROVIDER FUNCTIONS TO MAKE THE OBJECT FACTORIES FEEL MORE AUTHENTIC"""
import random
import uuid

from factory.fuzzy import BaseFuzzyAttribute, FuzzyDate
from factory.random import randgen
from faker.providers import BaseProvider


class FuzzyMaterialName(BaseFuzzyAttribute):
    options = [
        '1010 Carbon Steel',
        '1018 Mild Steel',
        '1215 Carbon Steel',
        '316  Stainless Steel',
        'ABS',
        'Aluminum',
        'Carbon Fiber',
        'Aluminum 7075',
        'Titanium',
        'Tool Steel A2',
        'Tool Steel S7',
        'Quartz',
        'Polyurethane',
        'Silicone',
        'Plastic',
        'Polypropylene',
        'Gold',
        'Onyx',
        'Nylon',
        'Fiberglass',
        'Lexan',
        'Brass',
        'Bronze 660' 'Copper',
        'Clear Resin',
        'Composite',
        'Aluminum 7075-T6',
        'Aluminum 6061-T6',
        'Aluminum 6061',
    ]

    def fuzz(self):
        lucky_index = randgen.randrange(0, len(self.options) - 1)
        return self.options[lucky_index]


class FuzzyDateString(FuzzyDate):
    def fuzz(self):
        date = super().fuzz()
        return str(date)


class FuzzyPartFilename(BaseFuzzyAttribute):
    cad_extensions = [
        'ipt',
        'prt',
        'sat',
        'sldprt',
        'x_b',
        'x_t',
        'dxf',
        'stl',
        'step',
        'stp',
        'igs',
        'iges',
    ]

    def fuzz(self):
        lucky_index = randgen.randrange(0, len(self.cad_extensions) - 1)
        return "{}.{}".format(uuid.uuid4().hex, self.cad_extensions[lucky_index])


class FuzzyOperationName(BaseFuzzyAttribute):
    options = [
        'Saw',
        'CAD Design',
        'Support Removal',
        'Fortus 450mc',
        'Admin',
        '3D Printing',
        'Bead-Blasted',
        'Electropolish',
        'Iridate Clear',
        'Iridate Yellow',
        'Milling',
        'Painting',
        'Fixturing',
        'Lathe',
        'Lathe (Manual)',
        'Masking',
        'Heat Treatment',
        'Shipping',
        'Programming',
        'Marking',
        'Powder Coating',
        'Standard Finish',
        'Tapping',
        'Turning (Auto)',
        'Turning (Manual)',
        'Laser Etch',
        'Polish',
        'SLS',
        'SLA',
        'Material Setup',
        'Band Saw',
        'Gun Drill',
        'Tooling',
        'Injection Molding',
        'Waterjet',
        'Plasma cut',
        'Casting',
        'Bending',
        'Sheet Metal',
        'Welding',
        'Urethane Casting',
        'FDM',
        'DMLS',
    ]

    def fuzz(self):
        lucky_index = randgen.randrange(0, len(self.options) - 1)
        return self.options[lucky_index]


class FuzzyPhoneNumber(BaseFuzzyAttribute):
    def fuzz(self):
        phone_number = ""
        for i in range(10):
            phone_number += str(randgen.randrange(0, 9))
        return phone_number


class FuzzyPhoneExt(BaseFuzzyAttribute):
    def fuzz(self):
        ext = ""
        for i in range(4):
            ext += str(randgen.randrange(0, 9))
        return ext
