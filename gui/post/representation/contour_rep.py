

"""
ContourRep: iso-surfaces representation on scalar (point/cell) fields
"""

from ..utils import get_array_range
from .base_rep import BaseRep
from .color_rep import ColorRep


class ContourRep(ColorRep):
    """ContourRep implementation."""

    name = 'Iso-surfaces Representation (Contours)'
    calc_source = basic_source = None

    def defaults(self):
        """
        Add default options to self.opts, called after initialization
        and prior to the represent function
        """
        ColorRep.defaults(self)
        if 'NbContours' not in self.opts:
            self.opts['NbContours'] = 10

        self.opts.pop('Slice', None)
        self.opts.pop('SlicePosition', None)
        self.opt_groups['Representation'] = ['Component', 'NbContours']

    def customize_source(self):
        """
        Overload the default source by using a Calculator filter
        to calculate a translational vector for structural elements
        """
        import pvsimple as pvs

        # The basic coloring source is saved since it is used
        # as input to the scalar field extractor for iso surfaces
        if self.basic_source is None:
            self.basic_source = self.source

        ColorRep.customize_source(self)
        pvs.Hide(self.source, self.ren_view)

        comp = self.opts['Component']

        self.calc_source = self.source
        if comp != 'Magnitude' and len(self.field.info['components']) > 1:
            att_type = 'Point Data' if self.field.info['support'] == 'POINTS'\
                else 'Cell Data'
            formula = '%s_%s' % (self.array, comp)
            arrname = '{}:{}'.format(self.field.name, comp)
            self.calc_source = BaseRep.register_source(
                'Calculator', self.calc_source, ResultArrayName=arrname,
                Function=formula, AttributeType=str(att_type),
                label='<{}:{}:{}> EXTRACT'.format(self.field.concept.name,
                                                  self.field.name, comp.upper()))
            self.calc_source.UpdatePipeline()
            self.array = arrname

        pvs.SetActiveSource(self.calc_source)
        filterfunc = 'Contour' if self.field.info['support'] == 'POINTS'\
            else 'ContourOnCells'

        self.source = BaseRep.register_source(
            str(filterfunc), self.calc_source, ComputeNormals=0,
            GenerateTriangles=0, ComputeScalars=1,
            label='<{}:{}:{}> CONTOUR'.format(self.field.concept.name,
                                              self.field.name, comp.upper()))

        self.update_contours()

    def update_source(self, mod_opts):
        """
        For the contour representation, update the source
        as to extract another scalar as needed.
        """
        import pvsimple as pvs
        # print('in update_source, mod_opts=', mod_opts)

        if 'Component' in mod_opts:
            # Reset PV source (pipeline node) AND array name
            # Then call the source customizer function
            self.source = self.field.concept.result.source
            self.array = self.field.info['pv-aident']
            self.calc_source = None
            pvs.SetActiveSource(self.source)
            self.customize_source()

    def update_contours(self):
        """
        Updates contours based on the number of iso value surfaces
        """
        # Determine min and max of the array for component 0 = scalar
        atype = self.field.info['support'].lower()[:-1]
        vmin, vmax = get_array_range(
            self.calc_source, self.array, 0, atype=atype)
        # print("vmin = %g, vmax = %g"%(vmin, vmax))

        if vmax - vmin < 1.e-8:
            isos = [vmin]
            self.opts['NbContours'] = 1
        else:
            # (x) intermediate contours (+2) extreme contours
            nbcont = self.opts['NbContours']
            vdiff = (vmax - vmin) * 1.0 / nbcont
            isos = [vmin] + [vmin + 0.5 * vdiff + vdiff *
                             i for i in range(nbcont)] + [vmax]

        self.source.ContourBy = [self.field.info['support'], self.array]
        self.source.Isosurfaces = isos
        self.source.UpdatePipeline()

        BaseRep.show_reference(self)

    def update_colorbar(self, timechange=False):
        """
        Swap coloring component since the source already extracts the
        contour component. However once the coloring is done, set the
        component back to its previous value.

        Note: update_colorbar of ColorRep uses self.opts['Component']
        to look for the coloring component in self.array, in our case
        self.array is already modified to include the component.
        """
        comp = self.opts['Component']
        self.opts['Component'] = 'Scalar'
        ColorRep.update_colorbar(self, timechange)
        self.opts['Component'] = comp

    def update(self, mod_opts):
        """
        Update the warped field representation based on changes
        in scale factor
        """
        ColorRep.update(self, mod_opts)
        self.update_contours()
