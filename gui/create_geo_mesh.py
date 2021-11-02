#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.4.0 with dump python functionality
###

import sys
import salome

import os
### linux work_dir
work_dir = os.popen('echo `pwd`').read()
### linux work_dir

#work_dir =  os.getcwd()

print('work_dir:',work_dir)

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
#sys.path.insert(0, r'/home/export/online3/amd_share/truss_bridge_app')

###
### SHAPER component 参数化建模
###

from SketchAPI import *
from salome.shaper import model
### set parameters
width = 5
height = 5
length = 50
sections = 6
spacing = length/sections
###
model.begin()
partSet = model.moduleDocument()
Part_1 = model.addPart(partSet)
Part_1_doc = Part_1.document()

model.addParameter(Part_1_doc, "width", str(width))
model.addParameter(Part_1_doc, "height", str(height))
model.addParameter(Part_1_doc, "length", str(length))
model.addParameter(Part_1_doc, "sections", str(sections))
model.addParameter(Part_1_doc, "spacing", str(spacing))

'''model.addParameter(Part_1_doc, "width", "7")
model.addParameter(Part_1_doc, "height", "5")
model.addParameter(Part_1_doc, "length", "40")
model.addParameter(Part_1_doc, "sections", "10")
model.addParameter(Part_1_doc, "spacing", "length/sections")
'''

Sketch_1 = model.addSketch(Part_1_doc, model.defaultPlane("XOY"))
SketchLine_1 = Sketch_1.addLine(5, 7, 0, 7)
SketchLine_2 = Sketch_1.addLine(0, 7, 0, 0)
SketchLine_3 = Sketch_1.addLine(0, 0, 5, 0)
SketchLine_4 = Sketch_1.addLine(5, 0, 5, 7)
SketchConstraintCoincidence_1 = Sketch_1.setCoincident(SketchLine_4.endPoint(), SketchLine_1.startPoint())
SketchConstraintCoincidence_2 = Sketch_1.setCoincident(SketchLine_1.endPoint(), SketchLine_2.startPoint())
SketchConstraintCoincidence_3 = Sketch_1.setCoincident(SketchLine_2.endPoint(), SketchLine_3.startPoint())
SketchConstraintCoincidence_4 = Sketch_1.setCoincident(SketchLine_3.endPoint(), SketchLine_4.startPoint())
SketchConstraintHorizontal_1 = Sketch_1.setHorizontal(SketchLine_1.result())
SketchConstraintVertical_1 = Sketch_1.setVertical(SketchLine_2.result())
SketchConstraintHorizontal_2 = Sketch_1.setHorizontal(SketchLine_3.result())
SketchConstraintVertical_2 = Sketch_1.setVertical(SketchLine_4.result())
SketchProjection_1 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
SketchPoint_1 = SketchProjection_1.createdFeature()
SketchConstraintCoincidence_5 = Sketch_1.setCoincident(SketchAPI_Point(SketchPoint_1).coordinates(), SketchLine_2.endPoint())
SketchConstraintLength_1 = Sketch_1.setLength(SketchLine_1.result(), "spacing")
SketchConstraintLength_2 = Sketch_1.setLength(SketchLine_4.result(), "width")
model.do()
Face_1 = model.addFace(Part_1_doc, [model.selection("FACE", "Sketch_1/Face-SketchLine_1r-SketchLine_2f-SketchLine_3f-SketchLine_4f")])
LinearCopy_1 = model.addMultiTranslation(Part_1_doc, [model.selection("COMPOUND", "all-in-Face_1")], model.selection("EDGE", "PartSet/OX"), "spacing", "sections/2")
Point_2 = model.addPoint(Part_1_doc, 0, 0, 0)
Point_3 = model.addPoint(Part_1_doc, "spacing", "0", "height")
Point_4 = model.addPoint(Part_1_doc, "spacing", "0", "0")
Polyline_1_objects = [model.selection("VERTEX", "all-in-Point_1"), model.selection("VERTEX", "all-in-Point_2"), model.selection("VERTEX", "all-in-Point_3")]
Polyline_1 = model.addPolyline3D(Part_1_doc, Polyline_1_objects, False)
Point_5 = model.addPoint(Part_1_doc, "0", "0", "height")
Polyline_2 = model.addPolyline3D(Part_1_doc, [model.selection("VERTEX", "all-in-Point_4"), model.selection("VERTEX", "all-in-Point_2")], False)
LinearCopy_2 = model.addMultiTranslation(Part_1_doc, [model.selection("COMPOUND", "all-in-Polyline_2"), model.selection("COMPOUND", "all-in-Polyline_1")], model.selection("EDGE", "PartSet/OX"), "spacing", "sections/2-1")
Point_6 = model.addPoint(Part_1_doc, "length/2-spacing", "0", "height")
Point_7 = model.addPoint(Part_1_doc, "length/2", "0", "0")
Polyline_3 = model.addPolyline3D(Part_1_doc, [model.selection("VERTEX", "all-in-Point_6"), model.selection("VERTEX", "all-in-Point_5")], False)
Polyline_4 = model.addPolyline3D(Part_1_doc, [model.selection("VERTEX", "Point_4"), model.selection("VERTEX", "Point_1")], False)
LinearCopy_3_objects = [model.selection("COMPOUND", "LinearCopy_2_1"), model.selection("COMPOUND", "LinearCopy_2_2"), model.selection("WIRE", "Polyline_3_1"), model.selection("WIRE", "Polyline_4_1")]
LinearCopy_3 = model.addMultiTranslation(Part_1_doc, LinearCopy_3_objects, model.selection("EDGE", "PartSet/OY"), "width", 2)
Point_8 = model.addPoint(Part_1_doc, "0", "width", "height")
Polyline_5 = model.addPolyline3D(Part_1_doc, [model.selection("VERTEX", "all-in-Point_7"), model.selection("VERTEX", "all-in-Point_4")], False)
LinearCopy_4 = model.addMultiTranslation(Part_1_doc, [model.selection("COMPOUND", "all-in-Polyline_5")], model.selection("EDGE", "PartSet/OX"), "spacing", "sections/2")
Polyline_6 = model.addPolyline3D(Part_1_doc, [model.selection("VERTEX", "Point_1"), model.selection("VERTEX", "Point_3")], False)
LinearCopy_5 = model.addMultiTranslation(Part_1_doc, [model.selection("COMPOUND", "all-in-Polyline_6")], model.selection("EDGE", "PartSet/OX"), "spacing", "sections/2", model.selection("EDGE", "PartSet/OY"), "width", 2)
Point_9 = model.addPoint(Part_1_doc, "0", "width", "0")
Polyline_7 = model.addPolyline3D(Part_1_doc, [model.selection("VERTEX", "Point_1"), model.selection("VERTEX", "all-in-Point_8")], False)
LinearCopy_6 = model.addMultiTranslation(Part_1_doc, [model.selection("COMPOUND", "all-in-Polyline_7")], model.selection("EDGE", "PartSet/OX"), "spacing", "sections/2+1")
Symmetry_1_objects = [model.selection("COMPOUND", "LinearCopy_1_1"), model.selection("COMPOUND", "LinearCopy_3_1"), model.selection("COMPOUND", "LinearCopy_3_2"), model.selection("COMPOUND", "LinearCopy_3_3"), model.selection("COMPOUND", "LinearCopy_3_4"), model.selection("COMPOUND", "LinearCopy_4_1"), model.selection("COMPOUND", "LinearCopy_5_1"), model.selection("COMPOUND", "LinearCopy_6_1")]
Symmetry_1 = model.addSymmetry(Part_1_doc, Symmetry_1_objects, model.selection("FACE", "PartSet/YOZ"), True)
### linux work_dir

Export_1 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_38aewvdt.xao', model.selection("COMPOUND", "Symmetry_1_1"), 'XAO')
Export_2 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_psxtkyub.xao', model.selection("COMPOUND", "Symmetry_1_2"), 'XAO')
Export_3 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_adr_mof0.xao', model.selection("COMPOUND", "Symmetry_1_3"), 'XAO')
Export_4 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_ho2dmb_g.xao', model.selection("COMPOUND", "Symmetry_1_4"), 'XAO')
Export_5 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_fiasnwck.xao', model.selection("COMPOUND", "Symmetry_1_5"), 'XAO')
Export_6 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_a4lvhf2x.xao', model.selection("COMPOUND", "Symmetry_1_6"), 'XAO')
Export_7 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_c503qf1h.xao', model.selection("COMPOUND", "Symmetry_1_7"), 'XAO')
Export_8 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir)-1)]+'/shaper_jmx8crsu.xao', model.selection("COMPOUND", "Symmetry_1_8"), 'XAO')

### linux work_dir
'''Export_1 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_38aewvdt.xao', model.selection("COMPOUND", "Symmetry_1_1"), 'XAO')
Export_2 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_psxtkyub.xao', model.selection("COMPOUND", "Symmetry_1_2"), 'XAO')
Export_3 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_adr_mof0.xao', model.selection("COMPOUND", "Symmetry_1_3"), 'XAO')
Export_4 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_ho2dmb_g.xao', model.selection("COMPOUND", "Symmetry_1_4"), 'XAO')
Export_5 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_fiasnwck.xao', model.selection("COMPOUND", "Symmetry_1_5"), 'XAO')
Export_6 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_a4lvhf2x.xao', model.selection("COMPOUND", "Symmetry_1_6"), 'XAO')
Export_7 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_c503qf1h.xao', model.selection("COMPOUND", "Symmetry_1_7"), 'XAO')
Export_8 = model.exportToXAO(Part_1_doc, work_dir[0:(len(work_dir))]+'\shaper_jmx8crsu.xao', model.selection("COMPOUND", "Symmetry_1_8"), 'XAO')
'''
model.end()

###
### GEOM component 转为几何文件并分组
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()
### linux work_dir

(imported, road, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_38aewvdt.xao')
(imported, Symmetry_1_2, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_psxtkyub.xao')
(imported, lateral_beams_1, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_adr_mof0.xao')
(imported, Symmetry_1_4, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_ho2dmb_g.xao')
(imported, Symmetry_1_5, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_fiasnwck.xao')
(imported, top_beams, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_a4lvhf2x.xao')
(imported, Symmetry_1_7, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_c503qf1h.xao')
(imported, bottom_beams, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir)-1)]+'/shaper_jmx8crsu.xao')

### linux work_dir
'''
(imported, road, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_38aewvdt.xao')
(imported, Symmetry_1_2, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_psxtkyub.xao')
(imported, lateral_beams_1, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_adr_mof0.xao')
(imported, Symmetry_1_4, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_ho2dmb_g.xao')
(imported, Symmetry_1_5, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_fiasnwck.xao')
(imported, top_beams, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_a4lvhf2x.xao')
(imported, Symmetry_1_7, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_c503qf1h.xao')
(imported, bottom_beams, [], [], []) = geompy.ImportXAO(work_dir[0:(len(work_dir))]+'\shaper_jmx8crsu.xao')
'''
main_beams = geompy.MakeCompound([Symmetry_1_2, Symmetry_1_4, Symmetry_1_7])
lateral_beams = geompy.MakeCompound([Symmetry_1_5, lateral_beams_1])
geompy.addToStudy( road, 'road' )
geompy.addToStudy( Symmetry_1_2, 'Symmetry_1_2' )
geompy.addToStudy( lateral_beams_1, 'lateral_beams_1' )
geompy.addToStudy( Symmetry_1_4, 'Symmetry_1_4' )
geompy.addToStudy( Symmetry_1_5, 'Symmetry_1_5' )
geompy.addToStudy( top_beams, 'top_beams' )
geompy.addToStudy( Symmetry_1_7, 'Symmetry_1_7' )
geompy.addToStudy( bottom_beams, 'bottom_beams' )
geompy.addToStudy( main_beams, 'main_beams' )
geompy.addToStudy( lateral_beams, 'lateral_beams' )

main = geompy.MakeCompound([road, top_beams, bottom_beams, main_beams, lateral_beams])
#main = geompy.MakeCompound([top_beams, bottom_beams, main_beams, lateral_beams])
road_1 = geompy.CreateGroup(main, geompy.ShapeType["FACE"])
road_id_half1 = [i for i in range(5,int(5+(sections*0.5-1)*11+1),11)]
road_id_half2 = [i for i in range(road_id_half1[-1]+12,int(road_id_half1[-1]+12+(sections*0.5-1)*11+1),11)]
road_id = road_id_half1 + road_id_half2
#geompy.UnionIDs(road_1, [204, 104, 5, 215, 116, 16, 127, 27, 138, 38, 149, 49, 160, 60, 171, 71, 182, 82, 193, 93])
geompy.UnionIDs(road_1, road_id)
geompy.addToStudy( main, 'main' )
geompy.addToStudyInFather( main, road_1, 'road' )
### top_beams
top_beams_1 = geompy.CreateGroup(main, geompy.ShapeType["EDGE"])
#top_beams_id = [road_id(-1)+19,int(road_id(-1)+19+(sections*0.5-1)*11+1)]
top_beams_id_half1 = [i for i in range(road_id[-1]+19,int(road_id[-1]+19+(sections*0.5-2)*5+1),5)]
top_beams_id_half2 = [i for i in range(top_beams_id_half1[-1]+6,int(top_beams_id_half1[-1]+6+(sections*0.5-1)*5+1),5)]
top_beams_id = top_beams_id_half1 + top_beams_id_half2
#print(top_beams_id)
geompy.UnionIDs(top_beams_1, top_beams_id)
geompy.addToStudyInFather( main, top_beams_1, 'top_beams' )
### bottom_beams
bottom_beams_1 = geompy.CreateGroup(main, geompy.ShapeType["EDGE"])
bottom_beams_id_half1 = [i for i in range(top_beams_id[-1]+12,int(top_beams_id[-1]+12+(sections*0.5-1)*5+1),5)]
bottom_beams_id_half2 = [i for i in range(bottom_beams_id_half1[-1]+6,int(bottom_beams_id_half1[-1]+6+(sections*0.5)*5+1),5)]
bottom_beams_id = bottom_beams_id_half1 + bottom_beams_id_half2
geompy.UnionIDs(bottom_beams_1, bottom_beams_id)
geompy.addToStudyInFather( main, bottom_beams_1, 'bottom_beams' )
#print(bottom_beams_id)
### main_beams
main_beams_1 = geompy.CreateGroup(main, geompy.ShapeType["EDGE"])
a = int(sections*0.5)
main_beams_id_11 = [i for i in range(bottom_beams_id[-1]+9,bottom_beams_id[-1]+9+(a-2)*5+1,5)] 
main_beams_id_12 = [j for j in range(main_beams_id_11[-1]+6,main_beams_id_11[-1]+6+(a-2)*5+1,5)]
main_beams_id_21 = [k for k in range(main_beams_id_12[-1]+7,main_beams_id_12[-1]+7+(a-2)*5+1,5)]
main_beams_id_22 = [i for i in range(main_beams_id_21[-1]+6,main_beams_id_21[-1]+6+(a-2)*5+1,5)]
main_beams_id_3 = [main_beams_id_22[-1]+6,main_beams_id_22[-1]+6+4,main_beams_id_22[-1]+6+4+5,main_beams_id_22[-1]+6+4+5+4]
main_beams_id_41 = [i for i in range(main_beams_id_3[-1]+7,main_beams_id_3[-1]+7+(a*2-1)*5+1,5)]
main_beams_id_42 = [j for j in range(main_beams_id_41[-1]+6,main_beams_id_41[-1]+6+(a*2-1)*5+1,5)]
main_beams_id = main_beams_id_11 + main_beams_id_12 + main_beams_id_21 + main_beams_id_22 + main_beams_id_3 + main_beams_id_41 +main_beams_id_42
geompy.UnionIDs(main_beams_1, main_beams_id)
geompy.addToStudyInFather( main, main_beams_1, 'main_beams' )
### lateral_beams
lateral_beams_1 = geompy.CreateGroup(main, geompy.ShapeType["EDGE"])
lateral_beams_id_1 = [main_beams_id[-1]+16,main_beams_id[-1]+16+4]

lateral_beams_id_11 = [i for i in range(lateral_beams_id_1[-1]+8,lateral_beams_id_1[-1]+8+(a-1)*7,7)]
lateral_beams_id_12 = [j for j in range(lateral_beams_id_1[-1]+8+3,lateral_beams_id_1[-1]+8+3+(a-1)*7,7)]

lateral_beams_id_21 = [i for i in range(lateral_beams_id_12[-1]+5,lateral_beams_id_12[-1]+5+(a-1)*7,7)]
lateral_beams_id_22 = [j for j in range(lateral_beams_id_12[-1]+5+3,lateral_beams_id_12[-1]+5+3+(a-1)*7,7)]

lateral_beams_id_31 = [i for i in range(lateral_beams_id_22[-1]+6,lateral_beams_id_22[-1]+6+(a-1)*7,7)]
lateral_beams_id_32 = [j for j in range(lateral_beams_id_22[-1]+6+3,lateral_beams_id_22[-1]+6+3+(a-1)*7,7)]

lateral_beams_id_41 = [i for i in range(lateral_beams_id_32[-1]+5,lateral_beams_id_32[-1]+5+(a-1)*7,7)]
lateral_beams_id_42 = [j for j in range(lateral_beams_id_32[-1]+5+3,lateral_beams_id_32[-1]+5+3+(a-1)*7,7)]

lateral_beams_id = lateral_beams_id_1 + lateral_beams_id_11 + lateral_beams_id_12 + lateral_beams_id_21 + lateral_beams_id_22 + lateral_beams_id_31 + lateral_beams_id_32 + lateral_beams_id_41 + lateral_beams_id_42


geompy.UnionIDs(lateral_beams_1, lateral_beams_id)
geompy.addToStudyInFather( main, lateral_beams_1, 'lateral_beams' )

### left
left_1 = geompy.CreateGroup(main, geompy.ShapeType["EDGE"])
left_id = [bottom_beams_id[-1]]
geompy.UnionIDs(left_1, left_id)
geompy.addToStudyInFather( main, left_1, 'left' )

### right
right_1 = geompy.CreateGroup(main, geompy.ShapeType["EDGE"])
right_id = [bottom_beams_id[int(sections*0.5)-1]]
geompy.UnionIDs(right_1, right_id)
geompy.addToStudyInFather(main, right_1, 'right' )

### all_beams
all_beams_1 = geompy.CreateGroup(main, geompy.ShapeType["EDGE"])
all_beams_id = main_beams_id + lateral_beams_id + top_beams_id + bottom_beams_id
geompy.UnionIDs(all_beams_1, all_beams_id)
geompy.addToStudyInFather(main, all_beams_1, 'all_beams' )
###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)
local_length = spacing/8
Mesh_1 = smesh.Mesh(main)
Regular_1D = Mesh_1.Segment()
Local_Length_1 = Regular_1D.LocalLength(local_length,None,1e-07)
Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
Quadrangle_Parameters_1 = Quadrangle_2D.QuadrangleParameters(smeshBuilder.QUAD_STANDARD,-1,[],[])
isDone = Mesh_1.Compute()

Mesh_2 = smesh.Mesh(road)
status = Mesh_2.AddHypothesis(Local_Length_1)
Regular_1D_1 = Mesh_2.Segment()
status = Mesh_2.AddHypothesis(Quadrangle_Parameters_1)
Quadrangle_2D_1 = Mesh_2.Quadrangle(algo=smeshBuilder.QUADRANGLE)
isDone = Mesh_2.Compute()

all_beams_2 = Mesh_1.GroupOnGeom(all_beams_1,'all_beams',SMESH.EDGE)
top_beams_2 = Mesh_1.GroupOnGeom(top_beams_1,'top_beams',SMESH.EDGE)
bottom_beams_2 = Mesh_1.GroupOnGeom(bottom_beams_1,'bottom_beams',SMESH.EDGE)
main_beams_2 = Mesh_1.GroupOnGeom(main_beams_1,'main_beams',SMESH.EDGE)
lateral_beams_3 = Mesh_1.GroupOnGeom(lateral_beams_1,'lateral_beams',SMESH.EDGE)
left_2 = Mesh_1.GroupOnGeom(left_1,'left',SMESH.EDGE)
right_2 = Mesh_1.GroupOnGeom(right_1,'right',SMESH.EDGE)
all_beams_3 = Mesh_1.GroupOnGeom(all_beams_1,'all_beams',SMESH.NODE)

top_beams_3 = Mesh_1.GroupOnGeom(top_beams_1,'top_beams',SMESH.NODE)
bottom_beams_3 = Mesh_1.GroupOnGeom(bottom_beams_1,'bottom_beams',SMESH.NODE)
main_beams_3 = Mesh_1.GroupOnGeom(main_beams_1,'main_beams',SMESH.NODE)
lateral_beams_4 = Mesh_1.GroupOnGeom(lateral_beams_1,'lateral_beams',SMESH.NODE)
left_3 = Mesh_1.GroupOnGeom(left_1,'left',SMESH.NODE)
right_3 = Mesh_1.GroupOnGeom(right_1,'right',SMESH.NODE)
road_2 = Mesh_2.GroupOnGeom(road,'road',SMESH.FACE)
road_3 = Mesh_2.GroupOnGeom(road,'road',SMESH.NODE)
Compound_Mesh_1 = smesh.Concatenate( [ Mesh_1.GetMesh(), Mesh_2.GetMesh() ], 1, 1, 1e-05, False )
#[ GrMesh_1_Nodes, GrMesh_1_Edges, GrMesh_1_Faces, top_beams_4, bottom_beams_4, main_beams_4, lateral_beams_5, left_3, right_3, top_beams_5, bottom_beams_5, main_beams_5, lateral_beams_6, left_4, right_4, GrMesh_2_Nodes, GrMesh_2_Edges, GrMesh_2_Faces, road_4, road_5 ] = Compound_Mesh_1.GetGroups()


## Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(road_3, 'road_node')
smesh.SetName(Local_Length_1, 'Local Length_1')
smesh.SetName(Quadrangle_Parameters_1, 'Quadrangle Parameters_1')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Compound_Mesh_1.GetMesh(), 'Mesh_com')
smesh.SetName(Mesh_2.GetMesh(), 'Mesh_2')
smesh.SetName(top_beams_2, 'top_beams_edge')
smesh.SetName(road_2, 'road_face')
smesh.SetName(main_beams_2, 'main_beams_edge')
smesh.SetName(bottom_beams_2, 'bottom_beams_edge')
smesh.SetName(bottom_beams_3, 'bottom_beams_node')
smesh.SetName(left_2, 'left')
smesh.SetName(main_beams_3, 'main_beams_node')
smesh.SetName(lateral_beams_3, 'lateral_beams_edge')
smesh.SetName(top_beams_3, 'top_beams_node')
smesh.SetName(right_2, 'right')
smesh.SetName(right_3, 'right')
smesh.SetName(lateral_beams_4, 'lateral_beams_node')
smesh.SetName(left_3, 'left')

fname = 'Mesh_1.med'
### linux work_dir
fdir = os.path.join(work_dir[0:(len(work_dir)-1)],fname)
### linux work_dir
#fdir = '/home/export/online3/amd_share/truss_bridge_app/Mesh_1.med'
#fdir = os.path.join(work_dir[0:(len(work_dir))],fname)
try:
  Compound_Mesh_1.ExportMED(r'%s' % fdir,auto_groups=0,minor=40,overwrite=1,meshPart=None,autoDimension=1)
  pass
except:
  print('ExportMED() failed. Invalid file name?')

### linux work_dir

os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_38aewvdt.xao')
os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_psxtkyub.xao')
os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_adr_mof0.xao')
os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_ho2dmb_g.xao')
os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_fiasnwck.xao')
os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_a4lvhf2x.xao')
os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_c503qf1h.xao')
os.remove(work_dir[0:(len(work_dir)-1)]+'/shaper_jmx8crsu.xao')

### linux work_dir
'''
os.remove(work_dir[0:(len(work_dir))]+'\shaper_38aewvdt.xao')
os.remove(work_dir[0:(len(work_dir))]+'\shaper_psxtkyub.xao')
os.remove(work_dir[0:(len(work_dir))]+'\shaper_adr_mof0.xao')
os.remove(work_dir[0:(len(work_dir))]+'\shaper_ho2dmb_g.xao')
os.remove(work_dir[0:(len(work_dir))]+'\shaper_fiasnwck.xao')
os.remove(work_dir[0:(len(work_dir))]+'\shaper_a4lvhf2x.xao')
os.remove(work_dir[0:(len(work_dir))]+'\shaper_c503qf1h.xao')
os.remove(work_dir[0:(len(work_dir))]+'\shaper_jmx8crsu.xao')
'''


if salome.sg.hasDesktop():
  #salome.sg.updateObjBrowser()
  pass










