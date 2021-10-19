"""
BaseRep: parent class for all post-processing representations
"""

from ..config import DISPLAY_PROPS_DEFAULTS
from ..utils import dbg_print

########################################################################
#  Main structure of the BaseRep Class
########################################################################
#
# --> __init__        <== called when a new representation is requested
#    |---> defaults()     and is *indeed* needed (Results.represent)
#    |   1 ^^^^^^^^
#    |---> represent()
#        2 ^^^^^^^^^
# --> update_         <==   called when a change in the representation
#    |---> update(mod_opts) parameters is requested (Results.represent)
#        3 ^^^^^^
#
# --> update_colorbar <== called when the time step is changed (pvcontrol)
#   4 ^^^^^^^^^^^^^^^
########################################################################
#  Main structure of the ColorRep Class
#  based on BaseRep
########################################################################
#   1|---> defaults()                  <= provides the default component
#   2|---> represent()
#      *5|---> customize_source()      <= + PV Filters (Calc, ELNO to *)
#        |---> pvs.Show(self.source ...
#       4|---> update_colorbar()
#
#   3|---> update(mod_opts)
#        |---> pvs.HideAll( ...
#      *6|---> update_source(mod_opts) <= when component changes ...
#        |---> pvs.Show(self.source ...
#       4|---> update_colorbar()
#
########################################################################
#  WarpRep and ContourRep, VectRep, ModesRep, subclasses of ColorRep
#  reimplement/customize:
#   1|---> defaults()                  <= specific opts (ex. ScaleFactor)
#    |---> represent()
#      *5|---> customize_source()      <= + PV Filters (Calc, Warp, etc.)
#   3|---> update(mod_opts)            <= BaseRep + apply specific opts
#        |                                specific opts
#      *6|---> update_source(mod_opts) <= + PV Filters (Calc, ELNO to *)
#       4|---> update_colorbar()       <= minor changes
#                                         w.r.t ColorRep
########################################################################


class BaseRep():
    """BaseRep implementation."""

    name = 'Basic Representation'

    # Attributes manipulated by object instances
    field = source = array = display = opts = scene = None

    # Class reserved attributes
    _sources = {}      # Register database of all added sources
    # Tuple (source, display) of reference surface representation
    _reference = None
    _refdisp = True    # Flag criterion whether reference is allowed or not

    # Option groups (for the sidebar edit box)
    opt_groups = {'Display': ['Opacity', 'Representation', 'LineWidth'],
                  'Animation': ['FrameRate']}

    pickable = True  # Allow probing and plotting on the current representation

    def __init__(self, field, **opts):
        """
        Create a new representation based on a given field
        and additional options.

        Arguments:
            field (ResultField): field to represent
            opts (dict): additional options
        """
        dbg_print("#" * 70)
        dbg_print(
            "New {} of the field {}".format(
                self.name.lower(),
                field.name))
        if self.opts:
            dbg_print("Options")
            dbg_print("-------")
            for opt in self.opts:
                dbg_print(' > {} : {}'.format(opt, self.opts[opt]))
        else:
            dbg_print("Default options requested...")
        dbg_print("#" * 70)

        import pvsimple as pvs
        self.field = field
        self.source = field.concept.result.source
        self.array = field.info['pv-aident']
        self.ren_view = pvs.GetActiveView()
        assert self.ren_view

        import copy
        self.opts = copy.copy(opts)

        # Load the array corresponding to the current field
        result = self.field.concept.result
        result.full_source.AllArrays = [self.field.info['pv-fident']]
        pvs.SetActiveSource(self.source)

        self.defaults()
        self.represent()

        self.ren_view.Update()

    def update_(self, opts):
        """
        Callback function for updating a representation, determines the
        effectively modified options and then calls the representation
        specific update function with this information in order to render
        the update as efficiently as possible...
        """
        modified = []
        for opt in opts:
            if opt in self.opts:
                if self.opts[opt] != opts[opt]:
                    modified.append(opt)
            else:
                modified.append(opt)

        full_update_needed = False
        for mod_opt in modified:
            if mod_opt not in DISPLAY_PROPS_DEFAULTS[0]:
                full_update_needed = True
                break

        mod_opts = {}
        for mod_opt in modified:
            if mod_opt in opts:
                mod_opts[mod_opt] = None
                if mod_opt in self.opts:
                    mod_opts[mod_opt] = self.opts[mod_opt]
        self.opts.update(opts)

        if 'GroupsFilter' in mod_opts or 'GroupsFilterOptions' in mod_opts:
            result = self.field.concept.result
            if self.opts['GroupsFilter']:
                groups_to_filter = [grdef[0]
                                    for grdef in self.opts['GroupsFilterOptions']
                                    if grdef[1]]
                result.filter_groups(groups_to_filter)
            else:
                result.filter_groups([])

            return self.redraw()

        dbg_print("#" * 70)
        dbg_print(
            "Updating {} ({})".format(
                self.name.lower(),
                self.field.name))
        if mod_opts:
            dbg_print("Modified options")
            dbg_print("----------------")
            for opt in mod_opts:
                dbg_print(' > {} : {}'.format(opt, self.opts[opt]))
        else:
            dbg_print("No options modified")
        dbg_print("#" * 70)

        if full_update_needed:
            self.update(mod_opts)

        self.update_display_props(mod_opts)
        self.ren_view.Update()

        return self

    def represent(self):
        """
        This is where paraview python commands are carefully coded
        in order to provide the requested representation.
        ----------------------------------------------------------
        The Base class does not provide this function, it should
        be coded in the subclasses
        """
        raise NotImplementedError("Must be defined in a subclass")

    def defaults(self):
        """
        Complete the opts attribute (dictionnary) with defaults for
        missing keys
        """
        max_dim = self.field.concept.result.max_dim
        dprops = DISPLAY_PROPS_DEFAULTS[max_dim]
        for dprop in dprops:
            if dprop not in self.opts:
                self.opts[dprop] = dprops[dprop]

        if 'FrameRate' not in self.opts:
            self.opts['FrameRate'] = 1

        # Default group filtering is global and needs thus to be retrieved
        # from the options saved in the result
        result = self.field.concept.result
        if result.mesh:
            self.opts['GroupsFilter'] = bool(result.group_filter)
            self.opts['GroupsFilterOptions'] = []
            for gname, supp in result.groups:
                flag = (gname in result.group_filter)
                self.opts['GroupsFilterOptions'].append([gname, flag, supp])

    def update(self, mod_opts):
        """
        This is where paraview python commands are carefully coded
        in order to provide an update for the same representation
        as to consider changes in the display options for example.

        IMPORTANT
        mod_opts is a dict giving the modified options with the
        values for the PREVIOUS representation.
        The new options are already saved in self.opts

        This information should allow to program an efficient
        update of the representation
        ----------------------------------------------------------
        The Base class does not provide this function, it should
        be coded in the subclasses
        """
        raise NotImplementedError("Must be defined in a subclass")

    def redraw(self):
        """
        Redraw the current representation
        """
        import pvsimple as pvs
        pvs.HideAll(self.ren_view)
        new_opts = {}
        new_opts.update(self.opts)
        self.opts = None
        self.__init__(self.field, **new_opts)
        self.ren_view.ResetCamera()
        return self

    @classmethod
    def refresh_available_sources(cls):
        """
        Based on the available sources in the paraview central proxy manager,
        update all available sources in the internal registry.
        """
        import pvsimple as pvs
        proxy_man = pvs.servermanager.ProxyManager()
        available_keys = list(proxy_man.GetProxiesInGroup('sources').keys())
        available_sources = list(proxy_man.GetProxiesInGroup('sources').values())

        to_pop = []
        for root in cls._sources:
            if not isinstance(root, str):
                if not root in available_sources:
                    to_pop.append(root)
                    continue

            for filter_name in cls._sources[root]:
                av_filters = cls._sources[root][filter_name]
                to_remove = []
                for i, av_filter in enumerate(av_filters):
                    if not av_filter['PVKey'] in available_keys:
                        to_remove.append(i)
                src = cls._sources[root][filter_name] + []
                cls._sources[root][filter_name] = [src[i] for i in range(len(src))
                                                   if not i in to_remove]
        for root in to_pop:
            cls._sources.pop(root, None)

    @classmethod
    def register_source(cls, filter_name, root, label=None, **params):
        """
        Creates and registers a new source in order to avoid
        unnecessarly duplicating PV pipeline nodes for
        identical filters.
        All information is saved in the base class cls._sources
        """
        import pvsimple as pvs

        # Dealing with multiple inputs (such as for AppendAttributes)
        if isinstance(root, (tuple, list)):
            params.update({'Inputs': root})
            root = root[0]

        source = cls.is_available_source(filter_name, root, params)
        if source:
            # dbg_print('Source of type {} already available !'.format(filter_name))
            if label:
                pvs.RenameSource(label, source)
            return source

        # dbg_print('Registering new source of type {}'.format(filter_name))
        callfunc = getattr(pvs, filter_name)
        if isinstance(root, str):
            # Filter with no input like PV sources (sphere par ex.)
            newsource = callfunc()
        elif 'Inputs' in params:
            # Filter with multiple inputs (like AppendAttributes)
            newsource = callfunc(Input=params['Inputs'])
        else:
            # Default case, filter based on one input
            newsource = callfunc(Input=root)

        for param in params:
            if param == 'Inputs':
                continue
            setattr(newsource, param, params[param])

        if not root in cls._sources:
            cls._sources[root] = {}
        if not filter_name in cls._sources[root]:
            cls._sources[root][filter_name] = []

        params['PVSource'] = newsource

        cls._sources[root][filter_name].append(params)

        if label:
            pvs.RenameSource(label, newsource)

        # Retrieve and save PV internal key (label + identifier)
        # for later coherence and availability checks
        key = None
        proxy_man = pvs.servermanager.ProxyManager()
        for key in proxy_man.GetProxiesInGroup('sources'):
            if proxy_man.GetProxiesInGroup('sources')[key] == newsource:
                break
        params['PVKey'] = key

        return newsource

    @classmethod
    def is_available_source(cls, filter_name, root, params):
        """
        Returns a boolean specifying if a source already exists
        """
        if root in cls._sources:
            if filter_name in cls._sources[root]:
                av_filters = cls._sources[root][filter_name]
                for av_filter in av_filters:
                    comparison = [(params[p] == av_filter[p])
                                  for p in params if p in av_filter]
                    if False not in comparison:
                        return av_filter['PVSource']
        return False

    @classmethod
    def clear_sources_base(cls):
        """
        Clears all existing sources from the Paraview pipeline
        Note: since the file loading is not handled by the
        representation, these proxies (loaded med, duplicated,
        loaded as med) are not affected by this class method.
        """
        import pvsimple as pvs
        for root in cls._sources:
            for filter_name in cls._sources[root]:
                av_filters = cls._sources[root][filter_name]
                for av_filter in av_filters:
                    pv_source = av_filter['PVSource']
                    pvs.Delete(pv_source)
                    del pv_source
                av_filters = []
            cls._sources[root] = {}
        cls._sources = {}

    @classmethod
    def toggle_reference_base(cls, rep):
        """
        Base class method for toggling view of the reference position
        """
        cls._refdisp = not cls._refdisp
        if cls._refdisp is False:
            cls.hide_reference_base()
        else:
            cls.show_reference(rep)

    @classmethod
    def hide_reference_base(cls):
        """
        Base class method for hiding the reference position
        """
        import pvsimple as pvs
        if cls._reference:
            source, _ = cls._reference
            pvs.Hide(source)

    @classmethod
    def show_reference(cls, rep, opacity=None):
        """
        Adds a reference representation of the field's grid/mesh.
        Does not change the active source
        """
        if not cls._refdisp:
            return

        # Classes admitted to show reference position
        if not rep.name in [
                'Colored Representation',
                'Iso-surfaces Representation (Contours)',
                'Mode Animation',
                'Vector Representation (Glyphs)',
                'Deformed Representation (Warped)']:
            return

        # Default opacity values
        opacity = opacity if opacity is not None \
            else {'Colored Representation': 0.02,
                  'Iso-surfaces Representation (Contours)': 0.04,
                  'Mode Animation': 0.04,
                  'Vector Representation (Glyphs)': 0.05,
                  'Deformed Representation (Warped)': 0.05}[rep.name]

        import pvsimple as pvs
        source = cls.register_source(
            'ExtractSurface', rep.field.concept.result.source,
            label='<REFERENCE POSITION>')

        # Reference initial position (solid color)
        display = pvs.Show(source, rep.ren_view)
        rep.ren_view.Update()

        # Save previous source as to be able to toggle the active one
        prev_source = pvs.GetActiveSource()
        pvs.SetActiveSource(source)
        pvs.Render()

        display.Representation = 'Surface'
        display.DiffuseColor = [0.0, 0.0, 0.0]
        display.Opacity = opacity
        display.Pickable = 0
        display.LineWidth = 4

        cls._reference = (source, display)

        # Set the previous source as active
        pvs.SetActiveSource(prev_source)

    @staticmethod
    def clear_sources():
        """
        Proxy for calling the BaseRep clear_sources_base method properly
        """
        BaseRep.clear_sources_base()

    def toggle_reference(self):
        """
        Proxy for calling the BaseRep toggle_reference method properly
        """
        BaseRep.toggle_reference_base(self)

    @staticmethod
    def hide_reference():
        """
        Proxy for calling the BaseRep hide_reference method properly
        """
        BaseRep.hide_reference_base()

    def update_display_props(self, mod_opts):
        """
        Updates display properties (Representation and Opacity)
        """
        for mod_opt in mod_opts:
            if mod_opt in DISPLAY_PROPS_DEFAULTS[0]:
                setattr(self.display, mod_opt, self.opts[mod_opt])

    def animate(self, play=True):
        """
        Animates the current representation
        """
        import pvsimple as pvs

        if not self.scene:
            pvsm = pvs.servermanager

            #####################################################
            # Reimplementation of pvsimple AnimateReader function
            # in order to customize the animation
            # ---------------------------------------------------
            # pvs.AnimateReader(self.field.concept.result.source,
            #     self.ren_view)
            #####################################################

            # ---------------------------------------------------
            # "reader" is the PV source with timestep information
            # ----------------------------------------------------
            # This can not be any source like a Calculator or Warp
            # since these do not contain the time step information
            reader = self.field.concept.result.full_source
            view = self.ren_view

            # scene = pvsm.animation.AnimationScene()
            scene = pvs.GetAnimationScene()

            try:
                # Search for existing time keepers
                proxyman = pvsm.ProxyManager()
                tkeeper = next(iter(list(
                    proxyman.GetProxiesInGroup("timekeeper").values())))
                scene.TimeKeeper = tkeeper
            except IndexError:
                # Creates a new time keeper
                tkeeper = pvsm.misc.TimeKeeper()
                scene.TimeKeeper = tkeeper

            if not reader in tkeeper.TimeSources:
                tkeeper.TimeSources.append(reader)
            if not view in tkeeper.Views:
                tkeeper.Views.append(view)

            scene.ViewModules = [view]
            reader.UpdatePipelineInformation()
            scene.StartTime = reader.TimestepValues.GetData()[0]
            scene.EndTime = reader.TimestepValues.GetData()[-1]

            scene.PlayMode = str('Snap To TimeSteps')
            scene.NumberOfFrames = len(reader.TimestepValues)

            cue = pvsm.animation.TimeAnimationCue()
            cue.AnimatedProxy = view
            cue.AnimatedPropertyName = "ViewTime"
            scene.Cues = [cue]

            self.scene = scene

        # Time annotation in the top right corner
        annotate = BaseRep.register_source('AnnotateTime',
                                           'root', label='<TIME ANNOTATION>')

        # self.scene.UpdateAnimationUsingDataTimeSteps()

        annotate.Format = 'Time: %g s'

        display = pvs.Show(annotate, self.ren_view)

        display.FontFamily = str('Arial')
        display.FontSize = 6
        display.Color = (0.25, 0.25, 0.45)
        display.WindowLocation = str('AnyLocation')
        display.Position = [0.85, 0.95]

        if play:
            self.scene.Play()
