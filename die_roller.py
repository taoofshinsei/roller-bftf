import re
from random import randint

RAW_PATTERN = "((?P<_purpose>[A-Za-z]*)\s)?(?P<_dice>(?:\d+d\d+\s?)+)(?P<_mods>(\s?[+-]\d+)*)$"

#Given a string formatted like "Attack 2d20 [3d10] [+-]a...[+-]z", 
#rolls the requested number of dice and sums the modifiers
class Roll(object):
    def __init__(self, raw):
        to_die = lambda x: tuple(map(int, x.split('d')))
        matches = re.match(RAW_PATTERN, raw)
        if not matches:
            raise ValueError("Cannot parse roll")
            
        self.__dict__.update(matches.groupdict())
        self._dice = [to_die(x.group(0)) for x in re.finditer('\d+d\d+', self._dice)]
        self.results = [(c, d, [randint(1, d) for _ in range(c)]) for c,d in self._dice]
        self.mod = sum([int(v.group(0)) for v in re.finditer('[+-]\d+', self._mods)])
        self.value = sum([sum(ls) for _,_,ls in self.results]) + self.mod
        
    def __str__(self):
        return "*{}:* `{}`".format(self._purpose.title() if self._purpose else "Result", self.value)
