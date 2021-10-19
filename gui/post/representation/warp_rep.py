

"""
WarpRep: deformed structure representation with optional other-field
         coloring
"""

from ..config import TRANSLATIONAL_COMPS
from ..utils import (default_scale, nb_points_cells, dbg_print)
from .base_rep import BaseRep
from .color_rep import ColorRep


class WarpRep(ColorRep):
    """WarpRep implementation."""

    name = 'Deformed Representation (Warped)'
    warp_source = None

    def defaults(self):
        """
        Add default options to self.opts, called after initialization
        and prior to the represent function
        """
        ColorRep.defaults(self)

        if 'ScaleFactorAuto' in self.opts:
            scale_auto = self.opts['ScaleFactorAuto']
        else:
            scale_auto = 'ScaleFactor' not in self.opts
            if 'ScaleFactor' in self.opts:
                scale_auto = (self.opts['ScaleFactor'] < 1.e-18)

        if scale_auto:
            self.opts['ScaleFactorAuto'] = True
            self.opts['ScaleFactor'] = default_scale(
                self.field.concept.result.source,
                self.field.info['pv-aident'])
        else:
            self.opts['ScaleFactorAuto'] = False

        if 'ColorField' not in self.opts:
            self.opts['ColorField'] = self.field

        self.opts.pop('Slice', None)
        self.opts.pop('SlicePosition', None)
        self.opt_groups['Representation'] = [
            'Component', 'ScaleFactorAuto', 'ScaleFactor']

    def customize_source(self):
        """
        Overload the default source by using a Calculator filter
        to calculate a translational vector for structural elements
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
            trans_disp = BaseRep.register_source(
                'Calculator', self.source, ResultArrayName=arrname,
                Function=formula, AttributeType='Point Data',
                label='<{}:{}> (TRANSLATION)'.format(self.field.concept.name, self.field.name))
            self.array = arrname
            trans_disp.UpdatePipeline()
            trans_disp.UpdatePipelineInformation()
        else:
            trans_disp = self.source

        # Note that the scale factor is intentially not registered
        # so as to avoid new warps are created each time the scale is
        # changed by the user !
        self.warp_source = BaseRep.register_source(
            'WarpByVector', trans_disp,
            label='<{}:{}> DISPLACEMENT WARP'.format(self.field.concept.name, self.field.name))
        self.warp_source.ScaleFactor = self.opts['ScaleFactor']

        pvs.SetActiveSource(self.warp_source)
        self.source = self.warp_source

    def update_source(self, mod_opts):
        """
        For the warp representation coloring the array name
        needs to be adjusted as to allow coloring with other
        arrays than the one calculated for the warp needs.
        """
        import pvsimple as pvs

        if 'ColorField' in mod_opts:
            cfield = self.opts['ColorField']
            if cfield != self.field:
                # Duplicate the ResultConcept PV source for the
                # coloring purposes.
                # Note: this is necessary as the current behaviour
                # of PARAVIS upon reading a med file requires that
                # arrays be selected. They can not be all active
                # at the same time.
                dup_source = cfield.concept.result.duplicate_source()
                dup_source.AllArrays = [cfield.info['pv-fident']]

                # Special treatment for EL* fields requiring resampling
                if cfield.info['disc'] == 'GSSNE':
                    # Apparently no other way than resampling to get a similar
                    # field structure to the original point field data
                    _temp = BaseRep.register_source(
                        'ELNOfieldToSurface', dup_source, ShrinkFactor=1.0,
                        label='<{}:{}> TO POINTS'.format(cfield.concept.name,
                                                         cfield.name))
                    dup_source = BaseRep.register_source(
                        'ResampleWithDataset', _temp,
                        Source=self.field.concept.result.full_source,
                        label='<{}:{}> PROJECTED ON MESH'.format(cfield.concept.name,
                                                                 cfield.name))

                elif cfield.info['disc'] == 'GAUSS':
                    dup_source = BaseRep.register_source(
                        'ELGAfieldToSurfacecellaveraged', dup_source, Max=0, Min=0,
                        label='<{}:{}> CELL AVERAGED'.format(cfield.concept.name,
                                                             cfield.name))

                # elif self.field.concept.result.quadratic:
                #     dup_source = BaseRep.register_source('QuadraticToLinear',
                #         dup_source, label='<{}> DUPL. QUAD. TO LINEAR'.format(
                #             osp.basename(self.field.concept.result.path)))

                dup_source.UpdatePipeline()
                dup_source.UpdatePipelineInformation()

                # Before appending attributes, verify that the number of
                # points and cells are the same
                nbp_warp, nbc_warp = nb_points_cells(self.warp_source)
                nbp_other, nbc_other = nb_points_cells(dup_source)

                do_continue = False
                if cfield.info['support'] == 'POINTS':
                    do_continue = (nbp_warp == nbp_other)
                else:
                    do_continue = (nbc_warp == nbc_other)

                if not do_continue:
                    dbg_print('Incompatible fields, aborting...')
                    self.opts['ColorField'] = self.field
                    self.opts['Component'] = 'Magnitude'
                    pvs.SetActiveSource(self.source)
                    self.update({'ColorField': '-', 'Component': '-'})
                    return

                self.source = BaseRep.register_source(
                    'AppendAttributes', [self.warp_source, dup_source],
                    label='<{}:{} - {}:{}> MIXING'.format(
                        self.field.concept.name, self.field.name,
                        cfield.concept.name, cfield.name))
                self.array = cfield.info['pv-aident']

                if '_ELGA' in cfield.name:
                    self.array = self.array + '_avg'
            else:
                self.source = self.warp_source

            pvs.SetActiveSource(self.source)

        if 'Component' in mod_opts:
            cfield = self.opts['ColorField']
            if cfield == self.field:
                if not self.opts['Component'] == 'Magnitude':
                    self.array = cfield.info['pv-aident']
                elif len(cfield.info['components']) > 3:
                    self.array = '{}:TRAN'.format(cfield.info['pv-aident'])

    def update(self, mod_opts):
        """
        Update the warped field representation based on changes
        in scale factor
        """
        # Coloring by another field => force new title for the color bar
        if 'ColorField' in mod_opts:
            self.opts.pop('Title', None)
            self.opts.pop('Unit', None)

        ColorRep.update(self, mod_opts)

        if 'ScaleFactorAuto' in mod_opts or 'ScaleFactor' in mod_opts:
            if self.opts['ScaleFactorAuto']:
                self.opts['ScaleFactor'] = default_scale(
                    self.field.concept.result.source,
                    self.field.info['pv-aident'])
            self.warp_source.ScaleFactor = self.opts['ScaleFactor']

    def update_colorbar(self, timechange=False):
        """
        Swap field definition just before updating the colorbar
        classically
        """
        warp_field = self.field

        self.field = self.opts['ColorField']

        ColorRep.update_colorbar(self, timechange)

        self.field = warp_field
        BaseRep.show_reference(self)
