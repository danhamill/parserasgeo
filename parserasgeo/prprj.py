"""
prprj.py - parse RAS project file

Version 0.001

Parses very basic information from a RAS project file.

"""

class ProjectTitle(object):
    def __init__(self):
        self.value = None

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Proj Title':
            return True
        return False

    def import_prj(self, line, prj_file):
        self.value = line.split('=')[1][:-1]


        return next(prj_file)

    def __str__(self):
        return 'Proj Title=' + str(self.value) + '\n'

class PlanFiles(object):
    def __init__(self):
        self.values = []

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Plan File':
            return True
        return False

    def import_prj(self, line, prj_file):
        value = line.split('=')[1][:-1]
        if value not in self.values:
            self.values.append(value)

        return next(prj_file)

    def __str__(self):
        s = ''
        for value in self.values:
            s += 'Plan File=' + str(value) + '\n'
        return s

class GeomFiles(object):
    def __init__(self):
        self.values = []

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Geom File':
            return True
        return False

    def import_prj(self, line, prj_file):
        value = line.split('=')[1][:-1]
        if value not in self.values:
            self.values.append(value)

        return next(prj_file)

    def __str__(self):
        s = ''
        for value in self.values:
            s += 'Geom File=' + str(value) + '\n'
        return s



class ParseRASProject(object):
    def __init__(self, project_file):
        self.project_title = ProjectTitle()
        self.plan_files = PlanFiles()
        self.geom_files = GeomFiles()


        self.parts = [self.project_title, self.plan_files, self.geom_files]

        self.prj_list = []

        with open(project_file, 'rt') as prj_file:
                for line in prj_file:

                    while line != None:
                        for part in self.parts:
                            if part.test(line):
                                # print str(type(part))+' found!'
                                line = part.import_prj(line, prj_file)
                                #self.parts.remove(part)
                                self.prj_list.append(part)
                                break
                        else:  # Unknown line, add as text
                            self.prj_list.append(line)
                            line = next(prj_file,None)
                    #return line

    def __str__(self):
        s = ''
        for line in self.prj_list:
            s += str(line)
        return s + '\n'

    def write(self, out_prj_filename):
        with open(out_prj_filename, 'wt', newline='\r\n') as outfile:
            for line in self.prj_list:
                outfile.write(str(line))
def main():

    prj = ParseRASProject('C:/Users/u4rrecse/Documents/RAS_FRAZIL/RAS Model/BaldEagleCrRAZFR.prj')

    print(str(prj))
#    import sys
#
#    prp = ParseRASProject(sys.argv[1])
#    print(dir(prp))
#    print(str(prp))


if __name__ == '__main__':
    main()
