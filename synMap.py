

class SynMap:
    def __init__(self):
        self.synMap = {}
        # self.synMap["1"] = {"name": "CountMin", "parameters": ["keyField", "valueField", "operationMode", "epsilon",
        #                                                      "confidence", "seed"]}
        #
        #
        # self.synMap["30"] = {"name": "SpatialSketch", "parameters": ["KeyField", "ValueField", "OperationMode",
        #                                                            "BasicSketchParameters", "BasicSketchSynID",
        #                                                            "minX", "maxX", "minY", "maxY", "maxResolution"]}

        # Add
#         #1	CountMin	KEY	Count	Frequent Itemsets	KeyField, ValueField,OperationMode, epsilon, cofidence, seed
# 2	BloomFilter	KEY	Member of a Set	Membership	KeyField, ValueField,OperationMode, numberOfElements, FalsePositive
# 3	AMS	KEY	L2 norm, innerProduct, Count	Frequent Itemsets	KeyField, ValueField,OperationMode, Depth, Buckets
# 4	DFT	similarity score	Fourier Coefficients	Correlation	KeyField, ValueField, timeField,OperationMode,Interval in Seconds, Basic Window Size in Seconds, Sliding Window Size in Seconds , #coefficients
# 5	LSH	none	BucketID - Projected features	Correlation	KeyField, ValueField,OperationMode, windowSize, Dimensions, numberOfBuckets
# 6	Coresets	theNumberOfClustersK	Coresets used for kmeans	Clustering	KeyField, ValueField,OperationMode, maxBucketSize,dimensions
# 7	FM Sketch	none	Cardinality	Cardinality	keyField, ValueField, OperationMode, Bitmap size, epsilon relative error, probabilityofFailure
# 8	HyperLogLog	none	Cardinality	Cardinality	keyField, ValueField, OperationMode, rsd ( relative standard deviation )
# 9	StickySampling	KEY	FrequentItems, isFrequent, Count	Frequent Itemsets	keyField, ValueField, OperationMode, support, epsilon, probabilityofFailure
# 10	LossyCounting	KEY	Count, FrequentItems	Frequent Itemsets	keyField, ValueField, OperationMode, epsilon ( the maximum error bound )
# 11	ChainSampler	none	Sample of the data	Sampling	keyField, ValueField, OperationMode, size of sample, size of the window
# 12	GKQuantiles	KEY	Quantile	Quantiles	keyField , ValueField, OperationMode, epsilon ( the maximum error bound )
# 13	MarinetimeSKetch	none	Ship positions(Sample)	Sampling	keyField, ValueField, OperationMode, minsamplingperiod, minimumDistance, speed(knots) ,corse(degrees)
# 14	TopK	none	TopK	TopK	keyField, ValueField, OperationMode, numberOfK, countDown
# 15	OptimalDistributedWindowSampling	none	Sample of the data	Sampling	keyField, ValueField, OperationMode, windowSize
# 16	OptimalDistributedSampling	none	Sample of the data	Sampling	keyField, ValueField, OperationMode
# 17	WindowedQuantiles	KEY	Quantile	Quantiles	keyField , ValueField, OperationMode, epsilon ( the maximum error bound ),windowSize
# 18	Radius Sketch Family	similarity score	List of streams/windows	similarity/distance	KeyField, ValueField, OperationMode,Group Size, Sketch Size,Window Size, Number of Groups, Threshold
# 30	Spatial Sketch	KEY, minX, maxX, minY, maxY	Count in spatial range	Count	KeyField, ValueField, OperationMode, BasicSketchParameters, BasicSketchSynopsisID, minX, maxX, minY, maxY, maxResolution
# 31	OmniSketch	Attr1, Attr1Value, Attr2, Attr2Value, ...	Count with multi-dimensional predicates	Count	KeyField, ValueField, OperationMode, #Attributes, delta, epsilon, B, b, seed

        self.synMap["CountMin"] = {"synID": 1,
                                   "name": "CountMin",
                                   "parameters": ["keyField", "valueField", "operationMode", "epsilon",
                                                  "confidence", "seed"],
                                   "basicSketch": True}
        self.synMap["BloomFilter"] = {"synID": 2,
                                        "name": "BloomFilter",
                                        "parameters": ["keyField", "valueField", "operationMode", "numberOfElements",
                                                         "FalsePositive"],
                                        "basicSketch": True}
        self.synMap["AMS"] = {"synID": 3,
                                        "name": "AMS",
                                        "parameters": ["keyField", "valueField", "operationMode", "Depth", "Buckets"],
                                        "basicSketch": True}
        self.synMap["DFT"] = {"synID": 4,
                                        "name": "DFT",
                                        "parameters": ["keyField", "valueField", "timeField", "operationMode",
                                                       "IntervalInSeconds",
                                                         "BasicWindowSizeInSeconds", "SlidingWindowSizeInSeconds", "#coefficients"],
                                        "basicSketch": True}
        self.synMap["LSH"] = {"synID": 5,
                                        "name": "LSH",
                                        "parameters": ["keyField", "valueField", "operationMode", "windowSize",
                                                       "Dimensions", "numberOfBuckets"],
                                        "basicSketch": True}
        self.synMap["Coresets"] = {"synID": 6,
                                        "name": "Coresets",
                                        "parameters": ["keyField", "valueField", "operationMode", "maxBucketSize",
                                                       "dimensions"],
                                        "basicSketch": True}
        self.synMap["FMSketch"] = {"synID": 7,
                                        "name": "FMSketch",
                                        "parameters": ["keyField", "valueField", "operationMode", "BitmapSize",
                                                       "epsilonRelativeError", "probabilityofFailure"],
                                        "basicSketch": True}
        self.synMap["HyperLogLog"] = {"synID": 8,
                                        "name": "HyperLogLog",
                                        "parameters": ["keyField", "valueField", "operationMode", "rsd"],
                                        "basicSketch": True}
        self.synMap["StickySampling"] = {"synID": 9,
                                        "name": "StickySampling",
                                        "parameters": ["keyField", "valueField", "operationMode", "support",
                                                       "epsilon", "probabilityofFailure"],
                                        "basicSketch": True}
        self.synMap["LossyCounting"] = {"synID": 10,
                                        "name": "LossyCounting",
                                        "parameters": ["keyField", "valueField", "operationMode", "epsilon"],
                                        "basicSketch": True}
        self.synMap["ChainSampler"] = {"synID": 11,
                                        "name": "ChainSampler",
                                        "parameters": ["keyField", "valueField", "operationMode", "sizeOfSample",
                                                       "sizeOfWindow"],
                                        "basicSketch": True}
        self.synMap["GKQuantiles"] = {"synID": 12,
                                        "name": "GKQuantiles",
                                        "parameters": ["keyField", "valueField", "operationMode", "epsilon"],
                                        "basicSketch": True}
        self.synMap["MarinetimeSKetch"] = {"synID": 13,
                                        "name": "MarinetimeSKetch",
                                        "parameters": ["keyField", "valueField", "operationMode", "minSamplingPeriod",
                                                       "minimumDistance", "speed", "corse"],
                                        "basicSketch": True}
        self.synMap["TopK"] = {"synID": 14,
                                        "name": "TopK",
                                        "parameters": ["keyField", "valueField", "operationMode", "numberOfK", "countDown"],
                                        "basicSketch": True}
        self.synMap["OptimalDistributedWindowSampling"] = {"synID": 15,
                                        "name": "OptimalDistributedWindowSampling",
                                        "parameters": ["keyField", "valueField", "operationMode", "windowSize"],
                                        "basicSketch": True}
        self.synMap["OptimalDistributedSampling"] = {"synID": 16,
                                        "name": "OptimalDistributedSampling",
                                        "parameters": ["keyField", "valueField", "operationMode"],
                                        "basicSketch": True}
        self.synMap["WindowedQuantiles"] = {"synID": 17,
                                        "name": "WindowedQuantiles",
                                        "parameters": ["keyField", "valueField", "operationMode", "epsilon", "windowSize"],
                                        "basicSketch": True}
        self.synMap["RadiusSketchFamily"] = {"synID": 18,
                                        "name": "RadiusSketchFamily",
                                        "parameters": ["keyField", "valueField", "operationMode", "groupSize",
                                                       "sketchSize", "windowSize", "numberOfGroups", "threshold"],
                                        "basicSketch": True}



        self.synMap["SpatialSketch"] = {"synID": 30,
                                        "name": "SpatialSketch",
                                        "parameters": ["keyField", "valueField", "operationMode",
                                                                      "BasicSketchParameters", "BasicSketchSynID",
                                                                     "minX", "maxX", "minY", "maxY", "maxResolution"],
                                        "basicSketch": False}
        self.synMap["OmniSketch"] = {"synID": 31,
        "name": "OmniSketch",
        "parameters": ["Attr1", "Attr1Value", "Attr2", "Attr2Value"],
        "basicSketch": False}

    def getSynName(self, synID):
        # find name of the synopsis by their synID
        for key in self.synMap:
            if self.synMap[key]["synID"] == synID:
                print("name of the synopsis: ", self.synMap[key]["name"])
                return self.synMap[key]["name"]
        Exception("Synopsis ID not found")


    def getSynMap(self):
        return self.synMap

    def getBasicSketches(self):
        basicSketches = {}
        for key in self.synMap:
            if self.synMap[key]["basicSketch"]:
                basicSketches[key] = self.synMap[key]
        return basicSketches
