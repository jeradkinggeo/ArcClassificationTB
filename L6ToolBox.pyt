#Start 

import arcpy


class Toolbox(object):
    def __init__(self):
        self.label = "Toolbox"
        self.description = "Generate a color ramp for a feature class"
        self.canRunInBackground = False
        self.category = "Classification"
        self.alias = "Classification Tool"
        self.tools = [Tool]
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = "Renderer for symbologic classification"
        self.canRunInBackground = False
#Parameter naming
    def getParameterInfo(self):
        param0 = arcpy.Parameter(
        displayName= "Input Project",
        name = "input_project",
        datatype = "DEFile",
        parameterType="Required",
        direction="input",

        )
        param1 = arcpy.Parameter(
            displayName= "Layer Name",
            name = "layer_name",
            datatype="GPFeatureLayer",
            parameterType= "required",
            direction="input"

        )

        param2 = arcpy.Parameter(
            displayName= "Output Project",
            name = "output_project",
            datatype="DEFile",
            parameterType= "required",
            direction="Output"

        )
        params = [param0,param1,param2,]
        return params

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        #Creation of readtimes for progressor
        readTime = 2.5
        start = 0
        maximum = 100
        step = 25
        #file paths
        L6Path = r"C:\Users\Jerad\Desktop\College-Work\GEOG392\GEOG392-JKing\lab6\lab6map\lab6arcmap.aprx" 
        working_dir = r"C:\Users\Jerad\Desktop\College-Work\GEOG392\GEOG392-JKing\lab6\lab6map"
        project = arcpy.mp.ArcGISProject(working_dir + "\\" "lab6arcmap.aprx")
        #first progressor
        arcpy.SetProgressor("step","Starting tool run",start,maximum,step)
        time.sleep(readTime)
        arcpy.AddMessage("Reading in filepath")

        #Bringing in the parameters
        input_project = parameters[0].valueAsText
        layer_name = parameters[1].valueAsText
        output_project = parameters[2].valueAsText
        project = arcpy.mp.ArcGISProject(input_project)
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Looking at your inputs")
        time.sleep(readTime)
        mymap = project.listMaps()[0]
        #Source code for the tool
        for layer in mymap.listLayers():
            if layer.isFeatureLayer == True:
                    arcpy.SetProgressorPosition(start+step)
                    arcpy.SetProgressorLabel("Yup its a feature layer")
                    print(layer.name,end='')
                    symbology = layer.symbology
                    if hasattr(symbology,'renderer') == True:
                        arcpy.arcpy.SetProgressorPosition(start + step)
                        arcpy.arcpy.SetProgressorLabel("Creating renderer now")
                        print(' has a renderer')
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        symbology.renderer.classificationField = "shape_area"
                        symbology.renderer.breakcount = 5
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 classes)')[0]
                        layer.symbology = symbology
                    else:
                        print(' nah no renderer')
                        arcpy.SetProgressorPosition(maximum)
                        arcpy.SetProgressorLabel("Making your project")
                        arcpy.AddMessage("Creating your new project with new classification")
        project.saveACopy(working_dir + "\\" + output_project)
        arcpy.AddMessage("And we're done!")
#fin