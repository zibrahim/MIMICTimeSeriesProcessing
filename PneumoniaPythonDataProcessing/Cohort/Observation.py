class Observation :

    def __init__(self, type, name, datetime, value, unit, text):
        self.Type = type
        self.Name = name
        self.OrdinalTime = datetime
        self.Value = value
        self.Unit = unit
        self.Text = text

    def printObservation( self ):
        print(" Observation type: ", self.Type,
              "\n Observation name: ", self.Name,
              "\n Observation Ordinal Time Since admission: ", self.OrdinalTime,
              "\n Observation Value: ", self.Value, "\n--------\n")

    def as_dict(self, pid):
        observation_row = {'PatientID' : pid,
                       'ObservationType' : self.Type,
                        'ObservationName' : self.Name,
                       'ObservationOrdinalTime' : self.OrdinalTime,
                       'ObservationValue' : self.Value,
                       'ObservationUnit' : self.Unit,
                       'ObservationText' : self.Text
                       }
        return observation_row

    def printObservationdelta( self ):
        print("\t", self.OrdinalTime, " Since admission")