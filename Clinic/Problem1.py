#Problem 1
#You are given a list of "duty" objects for a given week. A duty object represents 
#a responsibility assigned to a given physician for a given period of time and has 
#the following members:
#day, hour, duration, physician_id
#Here, day is one of the following strings: 'Mo', 'Tu', 'We', 'Th', 'Fr'; hour is 
#an integer representing the starting time of the duty (0 to 23); duration is a 
#integer representing the number of hours the physician is responsible for the 
#duty after the starting time; and physician_id is an integer uniquely identifying 
#a physician.
#You are also given a list of physician absence requests for the same week. The 
#absence request object represents a period of time that the physician requests 
#to be out of the office and has the following member variables:
#day, hour, duration, physician_id
#The day and physician_id are the same as above, the hour is an integer 
#representing the starting time of the absence (0 to 23), duration is an integer 
#representing the number of hours the physician will be out of the office after 
#the starting time.

#Duty booking or Absence request booking
class PhysicianBooking(object):
    def __init__(self, day=None, hour=None, duration=None, physician_id=None):
        self.day = day
        self.hour = hour
        self.duration = duration
        self.physician_id = physician_id
    
    @property
    def day(self):
        return self._day
        
    @day.setter
    def day(self, value):
        if value not in ['Mo', 'Tu', 'We', 'Th', 'Fr']:            
            raise ValueError('Day must be in this list (Mo, Tu, We, Th, Fr)!')
        self._day = value        
        
    @property
    def hour(self):
        return self._hour
        
    @hour.setter
    def hour(self, value):
        if value not in range(24):            
            raise ValueError('Hour must be between 0 and 23!')
        self._hour = value
        
    @property
    def duration(self):
        return self._duration
        
    @duration.setter
    def duration(self, value):
        if value < 0:            
            raise ValueError('Duration must not be negative!')
        self._duration = value
        
    @property
    def physician_id(self):
        return self._physician_id
        
    @physician_id.setter
    def physician_id(self, value):
        self._physician_id = value
        
########################################
#A. Write a function that takes as input an absence request object and returns 
#an error code (integer 1) if the duration of the absence extends into the next 
#day, and a success code (integer 0) otherwise.    
    
def AbsenceChecking(Absence):
    if Absence.hour + Absence.duration > 24:
       return 1
       
    return 0
 
########################################
#B. Write a function that takes as inputs both of the above lists and returns a 
#list of "conflicting" duty objects where the physician has requested to be 
#absent for any portion of an assigned duty.
     
def ConflictChecking(DutyList, AbsenceList):
    ConflictingDutyList = []
    Day = {}
    Day['Mo'] = 0 
    Day['Tu'] = 1
    Day['We'] = 2
    Day['Th'] = 3
    Day['Fr'] = 4
    
    for duty in DutyList:
        for absence in AbsenceList:
            if duty._physician_id == absence._physician_id:
                DutyStartTime = Day[duty.day]*24 + duty.hour
                DutyStopTime = DutyStartTime + duty.duration
                AbsenceStartTime = Day[absence.day]*24 + absence.hour
                AbsenceStopTime = AbsenceStartTime + absence.duration
                if DutyStopTime > AbsenceStartTime >= DutyStartTime:                   
                       ConflictingDutyList.append(duty)
                       continue
                if DutyStopTime >= AbsenceStopTime > DutyStartTime:                   
                       ConflictingDutyList.append(duty)
                       continue
                if AbsenceStartTime <= DutyStartTime and \
                   AbsenceStopTime >= DutyStopTime:
                       ConflictingDutyList.append(duty)
                       continue
                   
    return ConflictingDutyList
    
#######################################
#Create sample data and test
        
Duty = PhysicianBooking("Tu", 8, 4, 1234)
AbsenceRequest = PhysicianBooking("Tu", 12, 13, 1234)
print("Duty:\n", Duty.__dict__)    
print("Absence request:\n", AbsenceRequest.__dict__)  
print("Absence request is overday (Y=1, N=0):")  
print(AbsenceChecking(AbsenceRequest))

DutyList = [Duty]
DutyList.append(PhysicianBooking("Mo", 0, 24, 1235))
DutyList.append(PhysicianBooking("We", 9, 40, 1236))
DutyList.append(PhysicianBooking("Fr", 10, 20, 1237))
DutyList.append(PhysicianBooking("Th", 23, 4, 1238))

AbsenceList = [AbsenceRequest]
AbsenceList.append(PhysicianBooking("Tu", 0, 16, 1235))
AbsenceList.append(PhysicianBooking("We", 8, 1, 1236))
AbsenceList.append(PhysicianBooking("Fr", 13, 1, 1237))
AbsenceList.append(PhysicianBooking("Tu", 8, 160, 1238))
AbsenceList.append(PhysicianBooking("Mo", 8, 16, 1239))

ConflictingDutyList = ConflictChecking(DutyList, AbsenceList)
print("Physician IDs that have conflicting duty:")
for conflict in ConflictingDutyList:
    print(conflict.physician_id)