#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def drange(start, stop, step):
	r = start
	while r <= stop:
		yield r
		r += step

def cos(a):
	return math.cos(math.radians(a))
def sin(a):
	return math.sin(math.radians(a))

def run(context):
	ui = None
	try:
		app = adsk.core.Application.get()
		ui  = app.userInterface
        
		# Get active design
		product = app.activeProduct
		design = adsk.fusion.Design.cast(product)
		rootComponent = design.rootComponent
		sketch = rootComponent.sketches.add( rootComponent.xYConstructionPlane)

		# Get input parameters
		pinCount = ui.inputBox( "Number of pins", "PinCount", "10" )
		if pinCount[1] == True: return
		pinRadius = ui.inputBox( 'Pin radius', 'PinRadius', "2 mm" )
		if pinRadius[1] == True: return
		pinCircRadius = ui.inputBox( 'Pin circle radius', 'CircleRadius', "42 mm" )
		if pinCircRadius[1] == True: return
		contraction = ui.inputBox( 'Cycloid contraction', 'Contraction', "1 mm" )
		if contraction[1] == True: return
		segmentation = ui.inputBox( 'Angle segments per reduction step', 'Segmentation', "200" )
		if segmentation[1] == True: return

		pinCount = int( pinCount[0] )
		pinRadius = design.unitsManager.evaluateExpression( pinRadius[0], "mm" )
		pinCircRadius = design.unitsManager.evaluateExpression( pinCircRadius[0], "mm" )
		contraction = design.unitsManager.evaluateExpression( contraction[0], "mm" )
		segmentation = int( segmentation[0] )

		rcr = pinCircRadius / pinCount
		reduction = pinCount - 1
		cbr = reduction * rcr

		l_p = None
		line = None
		firstLine = None

		def get_p( angle ):
			x = (cbr + rcr) * cos(angle)
			y = (cbr + rcr) * sin(angle)

			p_x = x + (rcr - contraction) * cos(pinCount * angle)
			p_y = y + (rcr - contraction) * sin(pinCount * angle)
			return adsk.core.Point3D.create( p_x, p_y, 0 )

		for angle in drange(0,360/reduction, 360/(reduction*segmentation)):
			n_p = get_p( angle )

			if l_p != None:
				line = sketch.sketchCurves.sketchLines.addByTwoPoints( l_p, n_p )
				n_p = line.endSketchPoint
				if firstLine == None: firstLine = line
			l_p = n_p
			app.activeViewport.refresh()

		n_p = get_p( 360/reduction )
		line = sketch.sketchCurves.sketchLines.addByTwoPoints( l_p, n_p )

		curves = sketch.findConnectedCurves( firstLine )
		offsetCurves = sketch.offset( curves, adsk.core.Point3D.create(0,0,0), pinRadius )

		ui.messageBox( "Using a contraction of " + str( contraction*10 ) + "mm the offset to the pins should be +" + str( (rcr - contraction)*10) + "mm" )

	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
