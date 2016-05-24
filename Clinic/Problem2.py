#Problem 2
#You are given a list of appointment tracking data for one day of appointments 
#in a medical clinic.
#Each datum is a time stamp object with the following member variables:
#physician_id, appointment_id, minutes, event_type
#Here, the physician_id is an integer uniquely identifying the physician whom 
#the patient is visiting, appointment_id is an integer unique for each patient 
#visit, minutes is an integer representing the number of minutes elapsed since  
#8:00 AM that day, and the event_type is one of the following:
#'IN' patient has signed in to the waiting room
#'RM' patient has been placed in an exam room
#'NF' the nurse has finished taking vitals
#'MD' the physician has finished examining the patient

import numpy as np
from collections import defaultdict

class AppointmentTracking(object):
    def __init__(self, physician_id=None, appointment_id=None, minutes=None, \
                 event_type=None):
        self.physician_id = physician_id
        self.appointment_id = appointment_id
        self.minutes = minutes
        self.event_type = event_type
    
    @property
    def physician_id(self):
        return self._physician_id
        
    @physician_id.setter
    def physician_id(self, value):
        self._physician_id = value
        
    @property
    def appointment_id(self):
        return self._appointment_id
        
    @appointment_id.setter
    def appointment_id(self, value):
        self._appointment_id = value        
        
    @property
    def minutes(self):
        return self._minutes
        
    @minutes.setter
    def minutes(self, value):
        self._minutes = value
        
    @property
    def event_type(self):
        return self._event_type
        
    @event_type.setter
    def event_type(self, value):
        self._event_type = value        
       
    def isDanglingVisit(self):        
        return (self.event_type is None) or \
               (self.minutes is None) or \
               (self.physician_id is None) or \
               (self.appointment_id is None) or \
               (self.event_type not in ['IN','RM','NF','MD'])
       
    def isDuplicate(self, AppointmentTracking):
        return (self.appointment_id == AppointmentTracking.appointment_id and \
               self.event_type == AppointmentTracking.event_type)

########################################
#A. Remove duplicate stamps from the list (having same appointment_id and 
#event_type), choose to keep the latest occurrence.

def RemoveDuplicateStamps(AppointmentList):
    Duplicate = [0]*len(AppointmentList)
    GoodList = []
    
    for i in range(len(AppointmentList)):
        if not Duplicate[i]:
            Max = AppointmentList[i].minutes
            for j in range(i+1, len(AppointmentList)):
                if AppointmentList[i].isDuplicate(AppointmentList[j]):
                    Duplicate[j] = 1
                    if AppointmentList[j].minutes is not None:
                        Max = np.max([Max, AppointmentList[j].minutes])
            AppointmentList[i].minutes = Max
            GoodList.append(AppointmentList[i])
    
    return GoodList    
    
########################################
#B. Remove dangling visits (a unique appointment_id missing any of the four 
#event types defined above)

def RemoveDanglingVisits(AppointmentList):
    return [x for x in AppointmentList if not x.isDanglingVisit()]

########################################
#C. The average appointment waiting time ('IN' to 'RM', ignoring negative 
#values)

def AvgWaitingTime(AppointmentList):
    total = 0
    count = 0
    
    for x in AppointmentList:
        if x.event_type == 'IN':
            for y in AppointmentList:    
                if (x.appointment_id == y.appointment_id) and \
                    y.event_type == 'RM':
                        time = y.minutes - x.minutes
                        if time >= 0:
                            total += time
                            count += 1
    if count > 0:
        total /= count
        
    return total

########################################
#D. For each physician id: the average appointment exam time ('NF' to 'MD', 
#ignoring negative values)

def AvgExamTime(AppointmentList):
    total = defaultdict(lambda: 0)
    count = defaultdict(lambda: 0)
    
    for x in AppointmentList:
        if x.event_type == 'NF':
            for y in AppointmentList:    
                if (x.physician_id == y.physician_id) and \
                    y.event_type == 'MD':
                        time = y.minutes - x.minutes
                        if time >= 0:
                            total[x.physician_id] += time
                            count[x.physician_id] += 1
    
    for key in count:
        if count[key] > 0:
            total[key] /= count[key]
    
    return total
        
########################################    
#Create sample data and test
        
Appoint = AppointmentTracking(1234, 1, 600, 'RM')
#print(Appoint.__dict__)

AppointmentList = [Appoint]
AppointmentList.append(AppointmentTracking(1234, 1, 100, 'IN'))
AppointmentList.append(AppointmentTracking())
AppointmentList.append(AppointmentTracking(1))
AppointmentList.append(AppointmentTracking(1236, 3, -800, 'RM'))
AppointmentList.append(AppointmentTracking(1236, 3, 800, 'IN'))
AppointmentList.append(AppointmentTracking(1238, 5))
AppointmentList.append(AppointmentTracking(1239, 6, 'MD'))
AppointmentList.append(AppointmentTracking(1238, 'MD', 24, 1))
AppointmentList.append(AppointmentTracking('MD', 24, 1, 1234))
AppointmentList.append(AppointmentTracking(1234, 1, 6000, 'MD'))
AppointmentList.append(AppointmentTracking(1238, 5, 'MD', 24))
AppointmentList.append(AppointmentTracking(1234, 1, 600, 'NF'))
AppointmentList.append(AppointmentTracking(1234, 1, 700, 'MD'))
AppointmentList.append(AppointmentTracking(1234, 10, 600, 'NF'))
AppointmentList.append(AppointmentTracking(1234, 10, 700, 'MD'))
AppointmentList.append(AppointmentTracking(1236, 3, 900, 'NF'))
AppointmentList.append(AppointmentTracking(1236, 3, 1000, 'MD'))

#Clean the data
AppointmentList = RemoveDuplicateStamps(AppointmentList) 
AppointmentList = RemoveDanglingVisits(AppointmentList)
       
print("\nAppointment list after cleanned up:")        
for appoint in AppointmentList:
    print(appoint.__dict__)    

print("\nAverage waiting time (minutes):", AvgWaitingTime(AppointmentList))    
print("\nAverage exam time of each physician (minutes):")
Physicsians = AvgExamTime(AppointmentList)
print("Physician ID\tAverage appointment exam time (minutes)")
for x in Physicsians:
    print(x, "\t\t\t", Physicsians[x])