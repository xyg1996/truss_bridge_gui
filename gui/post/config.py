

"""Configuration files for AsterStudy Results tab"""

WARP_READY_FIELDS = ['DEPL', 'DEPL_ABSOLU']
VECTOR_READY_FIELDS = ['DEPL', 'VITE', 'ACCE',
                       'DEPL_ABSOLU', 'VITE_ABSOLU', 'ACCE_ABSOLU',
                       'REAC_NODA', 'FORC_NODA']

FIELDS_WITH_MAG = VECTOR_READY_FIELDS + []

TRANSLATIONAL_COMPS = ['DX', 'DY', 'DZ']

REPRESENTATIONS = ['Points',
                   'Wireframe',
                   'Surface',
                   'Surface With Edges']

FIELD_LABELS = {'DEPL': 'Displacement',
                'VITE': 'Velocity',
                'ACCE': 'Acceleration',
                'TEMP': 'Temperature',
                'REAC_NODA': 'Support reaction forces/moments',
                'FORC_NODA': 'Nodal forces/moments',
                'EFGE_ELNO': 'Structural forces/moments (nodes)',
                'EFGE_ELGA': 'Structural forces/moments (integration pts)',
                'EFGE_NOEU': 'Structural forces/moments (interpolated)',
                'SIEF_ELGA': 'Elementary stress (integration pts)',
                'SIEF_ELNO': 'Elementary stress (nodes)',
                'SIEF_NOEU': 'Elementary stress (interpolated)',
                'SIGM_ELGA': 'Global stress (integration pts)',
                'SIGM_ELNO': 'Global stress (nodes)',
                'SIGM_NOEU': 'Global stress (interpolated)',
                'EPSI_ELGA': 'Elementary strain (integration pts)',
                'EPSI_ELNO': 'Elementary strain (nodes)',
                'EPSI_NOEU': 'Elementary strain (interpolated)',
                'EPEQ_ELGA': 'Equivalent strain (integration pts)',
                'EPEQ_ELNO': 'Equivalent strain (nodes)',
                'EPEQ_NOEU': 'Equivalent strain (interpolated)',
                'SIEQ_ELGA': 'Equivalent stress (integration pts)',
                'SIEQ_ELNO': 'Equivalent stress (nodes)',
                'SIEQ_NOEU': 'Equivalent stress (interpolated)',
                'CONT_ELEM': 'Contact pressure and properties',
                'VARI_ELGA': 'Constitutive-law\'s variables (indexed components)',
                'VARI_ELGA_NOMME': 'Constitutive-law\'s variables (named components)',
                'STRX_ELGA': 'Forces/displacements for structural elements',
                'FamilyIdNode': 'Nodal group identifiers',
                'FamilyIdCell': 'Element group identifiers',
                'NumIdCell': 'Element numbering',
                }

_SUFFICES = ['ELNO', 'ELGA', 'NOEU']
_INFOS = ['on nodes, per element', 'on elements', 'on nodes']
for _i in range(1, 11):
    _lbl = 'UT{:02d}_'.format(_i)
    for _j, _sffx in enumerate(_SUFFICES):
        FIELD_LABELS[
            _lbl + _sffx] = 'User-defined field #{} ({})'.format(_i, _INFOS[_j])


MESH_FIELDS = ['FamilyIdNode', 'FamilyIdCell', 'NumIdCell']

# Default values for the display properties, as a function of the
# MAXIMUM mesh dimension, 0 = 0D elements, 1 = 1D elements, etc.
DISPLAY_PROPS_DEFAULTS = [None] * 4
DISPLAY_PROPS_DEFAULTS[0] = {'Representation': 'Points',
                             'Opacity': 1.0,
                             'LineWidth': 0.0,
                             'PointSize': 8.0}
DISPLAY_PROPS_DEFAULTS[1] = {'Representation': 'Surface',
                             'Opacity': 1.0,
                             'LineWidth': 4.0,
                             'PointSize': 8.0}
DISPLAY_PROPS_DEFAULTS[2] = {'Representation': 'Surface',
                             'Opacity': 1.0,
                             'LineWidth': 2.0,
                             'PointSize': 4.0}
DISPLAY_PROPS_DEFAULTS[3] = {'Representation': 'Surface',
                             'Opacity': 1.0,
                             'LineWidth': 1.0,
                             'PointSize': 2.0}

RESULTS_PV_LAYOUT_NAME = str('PFsalome Results Layout')
RESULTS_PV_VIEW_NAME = str('PFsalome Results View')

# 开启result tab 的DEBUG信息
# DEBUG = False
DEBUG = True
