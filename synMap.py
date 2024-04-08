

class SynMap:
    def __init__(self):
        self.synMap = {}
        self.synMap["1"] = {"name": "CountMin", "parameters": ["keyField", "valueField", "operationMode", "epsilon",
                                                             "confidence", "seed"]}
        self.synMap["30"] = {"name": "SpatialSketch", "parameters": ["KeyField", "ValueField", "OperationMode",
                                                                   "BasicSketchParameters", "BasicSketchSynID",
                                                                   "minX", "maxX", "minY", "maxY", "maxResolution"]}

    def getSynMap(self):
        return self.synMap
# synMap = {}
#
# # Map containing synopses. From synID to parameters that need to be specified.
#
# synMap[1] = {"name": "CountMin", "parameters": ["keyField", "valueField", "operationMode", "epsilon", "confidence", "seed"]}
# synMap[30] = {"name": "SpatialSketch", "parameters": ["KeyField", "ValueField", "OperationMode", "BasicSketchParameters",
#               "BasicSketchSynID", "minX", "maxX", "minY", "maxY", "maxResolution"]}
