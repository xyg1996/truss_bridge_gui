

"""
VectorRep: vector (arrow glyphs) representation of vector (point) fields
"""

from ..config import TRANSLATIONAL_COMPS
from .base_rep import BaseRep
from .color_rep import ColorRep


class VectorRep(ColorRep):
    """VectorRep (Glyphs) implementation."""

    name = 'Vector Representation (Glyphs)'
    pickable = False  # Probing and plotting are not allowed
    glyph_array = None

    def defaults(self):
        """
        Add default options to self.opts, called after initialization
        and prior to the represent function
        """
        ColorRep.defaults(self)

        if 'MaxArrowSize' not in self.opts:
            data_info = self.source.GetDataInformation().DataInformation
            xmin, xmax, ymin, ymax, zmin, zmax = data_info.GetBounds()
            box_dim_max = max([xmax - xmin, ymax - ymin, zmax - zmin])
            self.opts['MaxArrowSize'] = box_dim_max * 0.05

        self.opts.pop('Slice', None)
        self.opts.pop('SlicePosition', None)
        self.opt_groups['Representation'] = ['Component', 'MaxArrowSize']

    def customize_source(self):
        """
        Overload the default source by using a Glyph filter
        to calculate a translational vector of nodal forces
        or reaction forces.
        """
        import pvsimple as pvs

        ColorRep.customize_source(self)
        pvs.Hide(self.source, self.ren_view)

        # pragma pylint: disable=duplicate-code
        if self.field.needs_extraction():
            mag_comps = TRANSLATIONAL_COMPS
            array = self.field.info['pv-aident']
            formula = []
            for i, comp in enumerate(mag_comps):
                if comp in self.field.info['components']:
                    formula.append('{}_{}*{}Hat'.format(array, comp, 'ijk'[i]))
            formula = '+'.join(formula)

            arrname = '{}:TRAN'.format(array)
            trans_disp = BaseRep.register_source('Calculator',
                                                 self.source, ResultArrayName=arrname,
                                                 Function=formula, AttributeType='Point Data',
                                                 label='<{}:{}> (TRANSLATION)'.format(
                                                     self.field.concept.name, self.field.name))
            self.glyph_array = str(arrname)
        else:
            trans_disp = self.source
            self.glyph_array = self.field.info['pv-aident']

        pvs.SetActiveSource(trans_disp)
        self.source = BaseRep.register_source('Glyph', trans_disp,
                                              GlyphType='Arrow', GlyphMode='All Points',
                                              label='<{}:{}> VECTOR REP (GLYPHS)'.format(
                                                  self.field.concept.name, self.field.name))

        # Force selection of the proper coloring array
        self.update_source({'Component': ''})
        self.update_glyphs()

    def update(self, mod_opts):
        """
        Update the warped field representation based on changes
        in scale factor, in representation, or colored component
        """
        ColorRep.update(self, mod_opts)

        if 'MaxArrowSize' in mod_opts:
            self.update_glyphs()

    def update_source(self, mod_opts):
        """
        For the vector representation the array name for coloring may
        need to be adjusted as to treat magnitude and rotational
        coloring for displacement or forces with structural elements.

        Note update_source is called from ColorRep.update(..)

        self.array is used in order to color the glyph representation.
        """
        if 'Component' in mod_opts:
            array = self.field.info['pv-aident']
            self.array = array
            if (self.opts['Component'] == 'Magnitude'
                    and len(self.field.info['components']) > 3):
                # Note that this is calculated by ColorRep
                self.array = '{}:MAGTRAN'.format(array)

    def update_glyphs(self):
        """
        Updates glyphs by changing the scale of the representation
        """
        self.source.OrientationArray = ['POINTS', self.glyph_array]
        self.source.ScaleArray = ['POINTS', self.glyph_array]
        self.source.RescaleGlyphs = 1
        self.source.VectorScaleMode = 'Scale by Magnitude'

        self.source.MaximumGlyphSize = self.opts['MaxArrowSize']
        self.source.UpdatePipeline()

        BaseRep.show_reference(self)
