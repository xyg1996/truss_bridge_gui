

"""
Post-processing
---------------

The module implements the classes required for parsing and manipulating
results in the Results tab of AsterStudy GUI.

"""

from .utils import parse_file, mesh_dims_nbno
from .config import TRANSLATIONAL_COMPS

class ResultFile():
    """ResultFile implementation."""

    full_source = source = extract_source = dup_source = mode_source = None
    filter_source = group_filter = concepts = shell3d_quad = None
    mesh_proxy = temp_mesh = None

    def __init__(self, path, filetype='med'):
        """
        Parse a new result file given its filename

        Arguments:
            path (str): full path of the result file to post-process
                        (MED format)
        """
        import pvsimple as pvs
        import os.path as osp
        if filetype=='med':
            self.full_source = pvs.MEDReader(FileName=path)
        elif filetype=='of+ccx':
            self.full_source = pvs.PVDReader(FileName=path)

        # pvs.RenameSource('<{}> LOADED'.format(osp.basename(path)),
        #                  self.full_source)
        # self.source contains several interesting references/infos
        # >> steps : self.source.AllTimeSteps.Available, array of strings
        #            self.source.TimestepValues for numeric values !
        # >> file_name : self.source.FileName

        # Parse information from the result file and determine the concept names
        # as well as the field informations
        # finfos = parse_file(self.full_source)
        # print(("Parsing result {}".format(path)))
        # for cname in finfos:
        #     print("  >>", cname, finfos[cname])

        # self.concepts = [None] * len(list(finfos.keys()))
        # for i, cname in enumerate(finfos.keys()):
        #     self.concepts[i] = ResultConcept(self, cname, finfos[cname])

        # self.dims_nbno, self.temp_mesh = mesh_dims_nbno(path)

        # This flag is set to None if there are no QUAD9 elems
        # It is set by default to 0 if QUAD9 elems are detected
        # ------------------------------------------------------------
        # It can be changed by the user (to 1) as to activate special
        # treatments in the representations for 3d shells supported by
        # such (QUAD9) elems, in particular applying QuadraticToLinear
        # Paraview filters
        # self.shell3d_quad = 0 if ((2, 9) in self.dims_nbno) else None

        self.parse_mesh_groups()

        self.source = self.full_source
        # print('Done initializing ResultFile')


    def is_empty(self):
        """
        Returns whether the result file contains fields that can be
        visualized or not...
        """
        if not self.concepts:
            return True

        for concept in self.concepts:
            if concept.fields:
                return False

        return True

    @property
    def path(self):
        """
        Full result file path
        """
        return self.full_source.FileName

    @property
    def max_dim(self):
        """
        Maximum mesh dimension (0 -> 3)
        """
        return max([x[0] for x in self.dims_nbno])

    def lookup(self, cname):
        """
        Looks up a concept given its name
        """
        for concept in self.concepts:
            if concept.name == cname:
                return concept
        return None

    def duplicate_source(self):
        """
        Duplicates the source if needed by reading the mesh file again
        """
        import pvsimple as pvs
        import os.path as osp
        if not self.dup_source:
            self.dup_source = pvs.MEDReader(FileName=self.path)
            pvs.RenameSource(
                '<{}> DUPLICATED'.format(
                    osp.basename(
                        self.path)),
                self.dup_source)
        return self.dup_source

    def mesh_source(self):
        """
        Load the temporary mesh
        """
        import pvsimple as pvs
        import os.path as osp
        if not self.mesh_proxy:
            self.mesh_proxy = pvs.MEDReader(FileName=str(self.temp_mesh))
            pvs.RenameSource(
                '<{}> MESH SOURCE'.format(
                    osp.basename(
                        self.path)),
                self.dup_source)
        return self.mesh_proxy

    def source_as_mode(self):
        """
        Loads the main result file in Mode format
        """
        import pvsimple as pvs
        import os.path as osp
        if not self.mode_source:
            self.mode_source = pvs.MEDReader(FileName=self.path, ActivateMode=1,
                                             GenerateVectors=1)
            pvs.RenameSource(
                '<{}> AS MODE'.format(
                    osp.basename(
                        self.path)),
                self.mode_source)

        return self.mode_source

    def toggle_shell3d(self):
        """
        Toggles the self.shell3d_quad flag upon user choice
        """
        if self.shell3d_quad is not None:
            self.shell3d_quad = 0 if self.shell3d_quad == 1 else 1

    def parse_mesh_groups(self):
        """
        Parses available mesh groups from the input (MED) file
        """
        self.groups = [['Mesh information not available', False]]
        if hasattr(self, 'mesh'):
            import pvsimple as pvs
            # Retrieve the list of available mesh groups and their types
            mesh_source = self.mesh_source()
            keys = mesh_source.GetProperty("FieldsTreeInfo")[::2]
            self.mesh = keys[0]
            mesh_source.AllArrays = [self.mesh]

            extract = pvs.ExtractGroup(Input=mesh_source)
            # brut_groups contains groups and families, this needs to be
            # parsed further.
            # Note: the use of extract.AllGroups would only work in GUI mode
            # and thus breaks all unit tests
            brut_groups = extract.GetProperty("GroupsFlagsInfo")[::2]
            pvs.Show(extract)

            # Properly remove the extract filter, this may seem redundant
            # but at times partial cleaning may cause memory corruption
            # with paraview
            extract.AllGroups = []
            extract.UpdatePipeline()
            extract.UpdatePipelineInformation()
            pvs.HideAll()
            pvs.Delete(extract)

            sep = mesh_source.GetProperty('Separator').GetData()

            # These are the actual group names, we still need to determine
            # their types by reading the family information
            names = [gr[4:] for gr in brut_groups if gr[:4] == 'GRP_']

            self.groups = []
            for grname in names:
                supp = None
                for grfam in brut_groups:
                    if not grfam[:4] == 'FAM_':
                        continue
                    if grname in grfam:
                        supp = grfam.split(sep)[-1]
                        break
                if supp:
                    self.groups.append([grname, supp])

            self.group_filter = []

    def filter_groups(self, group_filter, input_source=None):
        """
        Reads and filters the results source on the requested groups
        group_filter is a list of groups that is handled from the underlying
        representation.
        """
        if self.group_filter == group_filter:
            return self.filter_source

        import pvsimple as pvs
        if not group_filter:
            self.source = self.full_source
            pvs.SetActiveSource(self.source)
            self.group_filter = []
            return self.full_source

        # This allows applying filter on the mode source for example
        source = input_source if input_source else self.full_source

        mesh_source = self.mesh_source()
        mesh_source.AllArrays = [self.mesh]
        if not self.extract_source:
            self.extract_source = pvs.ExtractGroup(mesh_source)
            pvs.RenameSource(
                '<GROUP EXTRACTION FROM MESH>',
                self.extract_source)

        pvs.SetActiveSource(self.extract_source)
        self.extract_source.AllGroups = \
            ['GRP_{}'.format(gr) for gr in group_filter]
        self.extract_source.UpdatePipeline()
        self.extract_source.UpdatePipelineInformation()

        if not self.filter_source:
            self.filter_source = pvs.ResampleWithDataset()
            self.filter_source.MarkBlankPointsAndCells = True
            # self.filter_source.ComputeTolerance = True
            # self.filter_source.CellLocator = str('Cell Locator')
            # self.filter_source.PassCellArrays = True
            # self.filter_source.PassPointArrays = True

        pvs.SetActiveSource(source)
        self.filter_source.Input = source
        self.filter_source.Source = self.extract_source

        self.filter_source.UpdatePipeline()
        self.filter_source.UpdatePipelineInformation()
        pvs.RenameSource('<RESAMPLING ON GROUP>', self.filter_source)
        pvs.Render()

        if not input_source:
            self.source = self.filter_source

        self.group_filter = group_filter
        return self.filter_source


class ResultConcept():
    """ResultConcept implementation."""

    result = name = fields = None

    def __init__(self, result, name, finfos):
        """
        Create/intialize a new concept based on preliminary
        parsed fields information.

        Arguments:
            result (ResultFile): parent result file.
            name (str): concept name.
            finfos (dict): parsed fields information.
        """
        # print("Initializing concept {}".format(name))
        self.result = result
        self.name = name

        self.fields = []
        for fname in finfos:
            # Do not associate the mesh fields to a concept
            if finfos[fname]['mesh'] == fname:
                self.result.mesh = finfos[fname]['pv-fident']
                continue
            field = ConceptField(self, fname, finfos[fname])
            self.fields.append(field)

        # print('Done initializing ResultConcept')

    def lookup(self, fname):
        """
        Looks up a field given its name
        """
        for field in self.fields:
            if field.name == fname:
                return field
        return None


class ConceptField():
    """ConceptField implementation."""

    concept = name = info = None
    params = {}

    def __init__(self, concept, name, info):
        """
        Create a new field based on preliminary parsed
        information from a concept read in a results file.

        Arguments:
            result (ResultConcept): parent concept.
            info (dict): userful information about the field

        ***************
        <info> contents
        ***************
        label: field label created based on the aster field name
        pv-fident: paraview field identifier <--- useful to filter out other fields
        pv-aident: paraview array identifier <--- useful in selection/coloring/etc.
        components: available components within the field
        support: geometrical support (point or cell)

        """
        # print("Initializing field {}".format(name))
        self.concept = concept
        self.name = name
        self.info = info
        # print('Done initializing ConceptField')

    def needs_extraction(self):
        """
        Method that verifies whether tranlsational extraction of
        the field is required (Displacement or force fields)
        """
        comps = self.info['components']
        if len(comps) != 3:
            return True

        for comp in comps:
            if comp not in TRANSLATIONAL_COMPS:
                return True

        return False
