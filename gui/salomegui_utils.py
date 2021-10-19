


#


"""
Utilities for SALOME
--------------------

Implementation of convenient functions for SALOME front-end.

"""

import re

from ..common import info_message, translate


def get_salome_pyqt():
    """
    Get access to SALOME PyQt interface.

    Returns:
        SalomePyQt: SALOME PyQt interface
    """
    # pragma pylint: disable=no-member
    import SalomePyQt
    return SalomePyQt.SalomePyQt()


def get_salome_gui():
    """
    Get python interface module for SALOME GUI.

    Note:
        Properly deals with `Connect` feature of Salome.
    """
    import salome
    # Deal with `Connect` feature
    if not salome.sg.__dict__:
        import libSALOME_Swig
        return libSALOME_Swig.SALOMEGUI_Swig()
    return salome.sg


def register_meshfile(meshes, meshfile):
    """
    Register mesh object.

    The method puts a file name as a 'Comment' attribute to all study
    objects created by importing meshes from that file.

    Arguments:
        meshes (list[Mesh]): SMESH Mesh objects.
        meshfile (str): Mesh file name.
    """
    import salome
    for mesh in meshes:
        sobject = salome.ObjectToSObject(mesh.mesh) # pragma pylint: disable=no-member
        if sobject is not None:
            builder = salome.myStudy.NewBuilder()
            attr = builder.FindOrCreateAttribute(sobject, 'AttributeComment')
            attr.SetValue(meshfile)


def publish_meshes(medfile):
    """Import meshes from a med file into SMESH.

    Arguments:
        medfile (str): Path to the med file.

    Returns:
        list[Mesh]: List of SMESH Mesh objects.
    """
    # pragma pylint: disable=import-error,no-name-in-module
    from salome.smesh import smeshBuilder
    smesh = smeshBuilder.New()
    objs, _ = smesh.CreateMeshesFromMED(medfile)
    info_message(translate("AsterStudy", "Found meshes: {0}").format(objs))
    register_meshfile(objs, medfile)
    return objs


def decode_view_parameters(text):
    """Decode parameters returned by `SALOMEGUI.getViewParameters()`.

    Arguments:
        text (str): Text returned by `getViewParameters`.

    Returns:
        list: List of tuples, each tuple contains the function name and the
        arguments as float numbers.
    """
    expr = re.compile(r"sg\.(?P<func>\w+)\((?P<args>[0-9\., ]+)\)", re.I)
    ret = []
    for mat in expr.finditer(text):
        args = [float(i) for i in mat.group('args').replace(" ", "").split(",")]
        ret.append((mat.group('func'), args))
    return ret
