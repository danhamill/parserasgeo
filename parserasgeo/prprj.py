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


        return prj_file

    def __str__(self):
        return 'Proj Title=' + str(self.value)+ '\n'

class PlanFiles(object):
    def __init__(self):
        self.values = []

    @staticmethod
    def test(line):
        if line.split('=')[0] == 'Plan File':
            return True
        return False

    def import_prj(self, line, prj_file):
        value = line.split('=')[1].strip()
        if value not in self.values:
            self.values.append(value)

        return prj_file
    def add_plan(self, plan_str):
        self.values.append(plan_str)
    def __str__(self):
        s = ''
        for value in self.values:
            s += 'Plan File=' + str(value)+ '\n'
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

        value = line.split('=')[1].strip()
        self.values.append(value)
        return prj_file

    def add_geom(self, geom_str):
        self.values.append(geom_str)

    def __str__(self):
        s = ''
        for value in self.values:
            s += 'Geom File=' + str(value) +'\n'
        return s


class UnknownParam(object):
    def __init__(self):
        self.value = None

    def import_prj(self, line, prj_file):
        self.value = line
        return prj_file

    def __str__(self):
        return str(self.value) + + '\n'



class ParseRASProject(object):
    def __init__(self, project_file):

        self.project_title = ProjectTitle()
        self.plan_files = PlanFiles()
        self.geom_files = GeomFiles()
        self.prj_list = []

        with open(project_file, 'rt') as prj_file:
                for line in prj_file:
                    if ProjectTitle.test(line):
                        pt = ProjectTitle()
                        pt.import_prj(line, prj_file)
                        self.prj_list.append(pt)
                    elif GeomFiles.test(line):
                        gf = GeomFiles()
                        gf.import_prj(line, prj_file)
                        self.prj_list.append(gf)
                    elif PlanFiles.test(line):
                        pf = PlanFiles()
                        pf.import_prj(line, prj_file)
                        self.prj_list.append(pf)
                    else:
                        uk = UnknownParam()
                        uk.import_prj(line, prj_file)
                        self.prj_list.append(line)


    def write(self, out_prj_filename):
        with open(out_prj_filename, 'wt', newline='\r\n') as outfile:
            for line in self.prj_list:
                outfile.write(str(line))

class AddData(object):
    def __init__(self, prj_list):
        self.prj_list = prj_list

    def add_geom_to_prj(self, geom_str):
        #find index of last valid geom
        g = [isinstance(e, GeomFiles) for e in self.prj_list]
        idx_insert = [i for i, val in enumerate(g) if val][-1]
        gf = GeomFiles()
        gf.add_geom(geom_str)
        self.prj_list.insert(idx_insert+1, gf)

    def add_plan_to_prj(self, plan_str):

        #find index of last valid geom
        g = [isinstance(e, PlanFiles) for e in self.prj_list]
        idx_insert = [i for i, val in enumerate(g) if val][-1]
        pf = PlanFiles()
        pf.add_plan(plan_str)
        self.prj_list.insert(idx_insert+1, pf)

    def write(self, out_prj_filename):
        with open(out_prj_filename, 'wt', newline='\r\n') as outfile:
            for line in self.prj_list:
                outfile.write(line.__str__())

def main():

    prj = ParseRASProject(r"C:\Users\RDCRLDDH\Desktop\NENMRHB4\NENMRHB4_hec_ras.prj")


    new = AddData(prj.prj_list)

    new.add_geom_to_prj('g09')
    new.add_plan_to_prj('p09')


    new.write(r"C:\Users\RDCRLDDH\Desktop\NENMRHB4\NENMRHB4_hec_ras.prj1")




if __name__ == '__main__':
    main()
