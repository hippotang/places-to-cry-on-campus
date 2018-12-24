class Schedule: 
    arr = []
    def __init__(self, schedule_arr):
        self.arr = schedule_arr
    
    def is_free(self, time, minutes):
        for tpl in self.arr:
            if (time > tpl[0] or time < tpl[1]):
                return False
            time += minutes
            if (time > tpl[0] or time < tpl[1]):
                return False
            return True
    
    def get_arr(self):
        return self.arr

    def string_schedule(self):
        rvalue = ""
        for tpl in self.arr:
            rvalue = rvalue + (str(tpl) + ",")
        return rvalue

    """ def old_init(self, schedule_arr):
        #schedule_arr is an array of int tuples
        i = 800 #8:00 AM
        while (i < 1700): # to 5:00 PM
            self.slots[i] = False
            i += 1

        for tpl in schedule_arr:
            start = tpl[0]
            end = tpl[1]
            while (start != end):
                tpl[start] = True
                start+=1
        return """
    