"""
prplan.py - parse RAS plan file

Version 0.001

Parses very basic information from a RAS plan file.

"""

class PlanTitle(object):
    def __init__(self):
        self.value = None

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Plan Title':
            return True
        return False

    def import_pln(self, line, pln_file):
        self.value = line.split('=')[1][:-1]


        return next(pln_file)

    def __str__(self):
        return 'Plan Title=' + str(self.value) + '\n'

class ShortID(object):
    def __init__(self):
        self.value = None

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Short Identifier':
            return True
        return False

    def import_pln(self, line, pln_file):
        self.value = line.split('=')[1][:-1]


        return next(pln_file)

    def __str__(self):
        return 'Short Identifier=' + str(self.value) + '\n'

class FlowFiles(object):
    def __init__(self):
        self.values = []

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Flow File':
            return True
        return False

    def import_pln(self, line, pln_file):
        value = line.split('=')[1][:-1]
        if value not in self.values:
            self.values.append(value)

        return next(pln_file)

    def __str__(self):
        s = ''
        for value in self.values:
            s += 'Flow File=' + str(value) + '\n'
        return s

class GeomFiles(object):
    def __init__(self):
        self.values = []

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Geom File':
            return True
        return False

    def import_pln(self, line, pln_file):
        value = line.split('=')[1][:-1]
        if value not in self.values:
            self.values.append(value)

        return next(pln_file)

    def __str__(self):
        s = ''
        for value in self.values:
            s += 'Geom File=' + str(value) + '\n'
        return s



class ParseRASPlan(object):
    def __init__(self, plan_file):
        self.plan_title = PlanTitle()
        self.flow_files = FlowFiles()
        self.geom_files = GeomFiles()
        self.short_id = ShortID()


        self.parts = [self.plan_title, self.flow_files, self.geom_files, self.short_id]

        self.pln_list = []

        with open(plan_file, 'rt') as pln_file:
                for line in pln_file:

                    while line != None:
                        for part in self.parts:
                            if part.test(line):
                                # print str(type(part))+' found!'
                                line = part.import_pln(line, pln_file)
                                #self.parts.remove(part)
                                self.pln_list.append(part)
                                break
                        else:  # Unknown line, add as text
                            self.pln_list.append(line)
                            line = next(pln_file,None)
                    #return line

    def __str__(self):
        s = ''
        for line in self.pln_list:
            s += str(line)
        return s + '\n'

    def write(self, out_pln_filename):
        with open(out_pln_filename, 'wt', newline='\r\n') as outfile:
            for line in self.pln_list:
                outfile.write(str(line))
def main():

    pln = ParseRASPlan('C:/Users/u4rrecse/Documents/RAS_FRAZIL/RAS Model/BaldEagleCrRAZFR.p01')

    print(str(pln))
#    import sys
#
#    prp = ParseRASProject(sys.argv[1])
#    print(dir(prp))
#    print(str(prp))


if __name__ == '__main__':
    main()
