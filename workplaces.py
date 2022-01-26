import numpy as np
import time

class workplaces:
    def __init__(self, workplace_dist, ages, id):
        self.workplace_type = ["tiny", "small" ,"medium", "large"]
        #workplace_dist = [0.25, 0.25, 0.25, 0.25]
        self.workplace_dist = workplace_dist
        self.ages = ages
        self.id = id

    def workplace_sort(self):
        workplaces = []
        working_id = self.id.copy()
        children = [i for i in working_id if self.ages[i] <= 9 ]
        teens = [i for i in working_id if self.ages[i] <= 18 and self.ages[i] >= 10 ]
        adults = [i for i in working_id if self.ages[i] > 18 and self.ages[i] <= 65]
        oaps = [i for i in working_id if self.ages[i] > 65]

        while len(children) > 0:
            school_class = []
            if len(children) > 29:
                for i in range(30):
                    school_class.append(children[0])
                    children.remove(children[0])
            else:
                for i in range(len(children)):
                    school_class.append(children[0])
                    children.remove(children[0])
            school_class.append(adults[0])
            adults.remove(adults[0])
            workplaces.append(school_class)

        while len(teens) > 0:
            school_class = []
            if len(teens) > 29:
                for i in range(30):
                    school_class.append(teens[0])
                    teens.remove(teens[0])
            else:
                for i in range(len(teens)):
                    school_class.append(teens[0])
                    teens.remove(teens[0])
            school_class.append(adults[0])
            adults.remove(adults[0])
            workplaces.append(school_class)

        while len(adults) > 0:

            new_work = np.random.choice(self.workplace_type, 1, p=self.workplace_dist)

            if len(adults) == 1:
                workplaces[len(workplaces) - 1].append(adults[0])
                adults.remove(adults[0])

            elif new_work == "tiny":
                if len(adults) > 1:
                    workplace = []
                    for i in range(2):
                        workplace.append(adults[0])
                        adults.remove(adults[0])
                    workplaces.append(workplace)

            elif new_work == "small":
                l = np.random.choice(list(range(3, 11)))
                if len(adults) >= l:
                    workplace = []
                    for i in range(l):
                        workplace.append(adults[0])
                        adults.remove(adults[0])
                    workplaces.append(workplace)
            
            elif new_work == "medium":
                l = np.random.choice(list(range(11, 31)))
                if len(adults) >= l:
                    workplace = []
                    for i in range(l):
                        workplace.append(adults[0])
                        adults.remove(adults[0])
                    workplaces.append(workplace)

            elif new_work == "large":
                l = np.random.choice(list(range(31, 50)))
                if len(adults) >= l:
                    workplace = []
                    for i in range(l):
                        workplace.append(adults[0])
                        adults.remove(adults[0])
                    workplaces.append(workplace)

        return workplaces

"""nPop = 500
workplace_dist = [0.25, 0.25, 0.25, 0.25]
ages = np.random.choice(np.arange(101), nPop)
id = [i for i in range(nPop)]

m = workplaces(workplace_dist, ages, id)
start = time.time()
a = m.household_sort()
print(a)
print(sum([len(b) for b in a]))
end = time.time()
print(end - start)"""