#!/usr/bin/env python3
import json
from subprocess import check_output
from dmiparser import DmiParser

__all__ = ['DmiDecode']

class DmiDecode(object):
    '''This is an simple example to show how to use dmiparser.
    '''

    def __init__(self, arguments=None, command='dmidecode'):
        '''
        arguments:  str, command's extra arguments like '-t 4'
        command:    str, dmidecode command
        '''
        self._command = command

        if arguments and type(arguments) is str:
            self._command = "%s %s" %(self._command, arguments)

        if type(command) is not str:
            raise TypeError("%s want a %s but got %s" %(
                self.__class__, type(__name__), type(command)))

        try:
            text = check_output(self._command, shell=True, encoding='utf8')
            parser = DmiParser(text)
            self._text = str(parser)
            self._data = json.loads(self._text)
        except:
            # XXX do something here
            raise

    def text(self):
        '''return str
        '''
        return self._text

    def data(self):
        '''return [{}, ...]
        '''
        return self._data

    def sections(self):
        '''return  [(id, name), ...]
        '''
        return [(x['handle']['id'], x['name']) for x in self._data]

    def get(self, *keys, id=None, name=None):
        '''get information for a section

        keys:   str, hash keys for a section
        id:     str, section id like '0x0020'
        name:   str, section name like 'Processor Information'
        '''
        data = self._data
        values = []

        if len (keys) == 0:
            raise AttributeError ("%s.%s does not accept empty parameters"
                %(self.__class__, self.get.__name__))

        for d in data:
            if id and id != d['handle']['id']:
                continue

            if name and name != d['name']:
                continue

            d_ = d

            for k in keys:
                try:
                    d_ = d_[k]
                except (KeyError, TypeError):
                    d_ = None
                    break

            if d_:
                values.extend(d_)

        return values

    def getProp(self, prop, id=None, name=None):
        '''get values for a section property

        prop:   str, property name
        id:     str, section id like '0x0020'
        name:   str, section name like 'Processor Information'
        '''
        keys_ = ['props']
        keys_.extend([prop, 'values'])

        return self.get(*keys_, id=id, name=name)

if '__main__' == __name__:
    '''Show CPU information, will print output like below.

    CPU1:
        Family: Xeon
        Version: Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
        Voltage: 1.8 V
        Speed: 2200 MHz/4000 MHz
        Status: Populated, Enabled
        Core: 10/10
        Thread: 20
    CPU2:
        Family: Xeon
        Version: Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
        Voltage: 1.8 V
        Speed: 2200 MHz/4000 MHz
        Status: Populated, Enabled
        Core: 10/10
        Thread: 20
    '''
    from functools import partial

    dmi = DmiDecode('-t 4')     # Type 4 is Processor
    secs = dmi.sections()

    for id, name in secs:
        getvals = partial(dmi.getProp, id=id, name=name)
        # XXX Here assumes that all items exist
        getfirst = lambda *args: getvals(*args)[0]

        print("%s:" %(getfirst('Socket Designation')))

        print("\tFamily: %s" %(getfirst('Family')))
        print("\tVersion: %s" %(getfirst('Version')))
        print("\tVoltage: %s" %(getfirst('Voltage')))
        print("\tSpeed: %s/%s" %(getfirst('Current Speed'), getfirst('Max Speed')))
        print("\tStatus: %s" %(getfirst('Status')))
        print("\tCore: %s/%s" %(getfirst('Core Enabled'), getfirst('Core Count')))
        print("\tThread: %s" %(getfirst('Thread Count')))

