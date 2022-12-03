# Creating custom class for  storing labels
# another option: we can use label encoder and use it for transforming

class TargetValueMapping:
    def __init__(self) -> None:
        self.neg: int = 0
        self.pos: int = 1
        
    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    
    
    
# write a code to train model and check the accuracy.