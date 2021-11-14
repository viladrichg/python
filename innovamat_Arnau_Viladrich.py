
import time

class Itinerary:
    activities_list = []
    def __init__(self):
       self.activities_list.append(Activity("Activity 1", "A1", ["1+2=","3-4=","2*3=","5-2*5="],["3","-1","6","-5"],1,30))
       self.activities_list.append(Activity("Activity 2", "A2", ["32*4=","5*21="],["128","105"],1,20))
       self.activities_list.append(Activity("Activity 3", "A3", ["123*45=","2355/15="],["5535","157"],2,60))
       self.activities_list.append(Activity("Activity 4", "A4", ["123*45=","2355/15="],["5535","157"],2,60))
       self.activities_list.append(Activity("Activity 5", "A5", ["123*45=","2355/15="],["5535","157"],3,60))
       self.activities_list.append(Activity("Activity 6", "A6", ["1212*321*0=","4321/149="],["0","29"],4,70))
       self.activities_list.append(Activity("Activity 7", "A7", ["1212*321*0=","4321/149="],["0","29"],5,50))
       self.activities_list.append(Activity("Activity 8", "A8", ["123*45=","2355/15="],["5535","157"],6,60))
       self.activities_list.append(Activity("Activity 9", "A9", ["123*45=","2355/15="],["5535","157"],6,60))
       self.activities_list.append(Activity("Activity 10", "A10", ["1212*321*0=","4321/149="],["0","29"],7,70))
       self.activities_list.append(Activity("Activity 11", "A11", ["1212*321*0=","4321/149="],["0","29"],8,50))
       self.activities_list.append(Activity("Activity 12", "A12", ["1212*321*0=","4321/149="],["0","29"],9,70))
       self.activities_list.append(Activity("Activity 13", "A13", ["1212*321*0=","4321/149="],["0","29"],10,50))
             
class Student:
    def __init__(self, id):
        self.id = id
        self.available_activity = 1
        self.latest_activity_done = 0
        self.latest_difficulty = 1

class Activity:
    def __init__(self, name, id, exercises, solutions, difficulty, time):
        self.id = id
        self.name = name
        self.exercises = exercises
        self.solutions = solutions
        self.difficulty = difficulty
        self.time = time

#-------------------

def startActivity(activity):
    num_exercises = len(activity.exercises)
    time_start = time.time()
    solutions = []

    for i in range(num_exercises):
        solutions.append(input(activity.exercises[i]))
        print("Your answer has been stored.")

    time_end = time.time()
    time_in_s = time_end - time_start

    return solutions, time_in_s

#-------------------

def validate_results(solutions, activity):
    num_exercises = len(activity.exercises)
    correct_answers = 0
    
    for i in range(num_exercises):
        if(solutions[i] == activity.solutions[i]): 
            correct_answers+=1

    score = correct_answers / num_exercises*100

    return score

#-------------------

def validate_time(time_in_s, activity):

    if(time_in_s < activity.time/2):
        return True  
    else:
        return False

#-------------------

def send_results_to_API(act, student_id, time, score, nextAct): 
    print("----------------------- RESULTS -----------------")
    print("Student_id: "+student_id+", LastActivity: "+act+" in "+str(round(time,2))+"s with "+str(score)+" % -> NextActivity: "+nextAct+"\n")

#-------------------

def next_activity_v1(score, act):
    nextAct = act

    if(score >= 75):
        nextAct = act+1
        print("Congratulations. You have passed the activity correctly.\n")

    else:
        print("You have NOT passed the activity, you must repeat it.\n") 

    return nextAct
   
#-------------------

def next_activity_v2(score, timing, act, student, it): #act = number of the activity, not the position

    if(score >= 75):
        student.latest_activity_done = act #that's the last activity the student has passed

        if(timing):
            if(student.latest_difficulty <= 10):
                student.latest_difficulty = student.latest_difficulty + 1 #difficulty increases 1 level

            for i in range(len(it.activities_list)):
                if(it.activities_list[i].difficulty == student.latest_difficulty):
                    
                    student.available_activity = i+1 #taking into account the offset of the positions
                    break #takes position of the fisrt activity with the achieved difficulty 

            print("Congratulations. You have passed to the next level of difficulty.\n")

        else:
            student.available_activity+=1
            print("Congratulations. You have passed to the next activity.\n")

        
    else:
        if(score <= 20):
            if(student.latest_difficulty >= 2):
                student.latest_difficulty = student.latest_difficulty - 1

            student.available_activity = student.latest_activity_done+1
            print("You have NOT passed the activity, you are going back to the previous level of difficulty.\n") 

    return student
   
## ----------------------- MAIN ------------------------

#create itinerary
it = Itinerary()

#ask id to the student
student_id = input("Please, enter your id name:")
student = Student(student_id)

while(student.available_activity <= len(it.activities_list)):
    
    #ask number activity
    act = input("\nPlease, introduce the number of the activity you would like to do (1 to 13): ")
    act = int(act)-1   #position in the activities list

    #option 1
    #while(act+1 > student.latest_activity): 
    #   print("You haven't arrived to this activity yet.")
    #   act = input("Please, introduce the number of the activity you would like to do (1 to 13): ")
    #   act = int(act)-1   

    #option 2
    while(act+1 > student.available_activity and it.activities_list[act].difficulty > student.latest_difficulty):
        print("You haven't arrived to this level of difficulty yet..\n")
        act = input("Please, introduce the number of the activity you would like to do (1 to 13): ")
        act = int(act)-1   

    solutions, mytime = startActivity(it.activities_list[act])

    score = validate_results(solutions, it.activities_list[act])
    timing = validate_time(mytime, it.activities_list[act]) 

    #nextAct = next_activity_v1(score, act) #option1
    student = next_activity_v2(score, timing, act+1, student, it) #option2

    send_results_to_API(it.activities_list[act].name, student_id, mytime, score, it.activities_list[student.available_activity-1].name)


# the user can choose all the activities whose difficulty is <= student difficulty parameter
# if the student fails, its difficulty parameter decreases. However, the activities that have already been unlocked are still available.  
