

class DatasetMap:
    def __init__(self):
        self.DatasetMap = {"Weather": {"minX": -100000,
                                       "maxX": 350000,
                                       "minY": 350000,
                                       "maxY": 650000,
                                       "maxResolution": 128,
                                       "queryParameters": ["Date (YYYYMMDD)"],
                                       "parameters": ["Date", "Rainfall (mm)"]}}
        # self.synMap["1"] = {"name": "CountMin", "parameters": ["keyField", "valueField", "operationMode", "epsilon",
        #                                                      "confidence", "seed"]}
        #
        #
        # self.synMap["30"] = {"name": "SpatialSketch", "parameters": ["KeyField", "ValueField", "OperationMode",
        #                                                            "BasicSketchParameters", "BasicSketchSynID",
        #                                                            "minX", "maxX", "minY", "maxY", "maxResolution"]}

    def getDataset(self, datasetName):
        return self.DatasetMap[datasetName]

    def getDatasetMap(self):
        return self.DatasetMap

    def getDatasetName(self, key):
        for dataset in self.DatasetMap:
            if dataset == key:
                return dataset
        return None

