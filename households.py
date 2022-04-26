import numpy as np
import time
class households:

    def __init__(self,household_dist, ages, id):
        #household_type = ["singYA", "singA", "singOAP", "coupleYA", "coupleYA1C", "coupleYA2C", "coupleYA3C", "couple4YAC", "singPYA1C", "singPYA2C", "singPYA3C", "coupleA", "coupleA1C", "coupleA2C", "coupleA3C", "couple4AC", "singPA1C", "singPA2C", "singPA3C", "coupleA1YA", "coupleA2YA", "singPA1YA", "singPA2YA", "coupleOAP", "unrelYA"]
        self.household_dist = household_dist        # define proportion distribution of households
        self.ages = ages        # define ages
        self.id = id            # define ids
        self.household_type = np.arange(len(household_dist))

    def household_sort(self):

        working_id = self.id

        self.households = np.zeros([len(id), 6]) - 1

        children = np.where(self.ages < 18)[0]

        youngadults = np.where(abs(self.ages - 29.5) <= 11.5)[0]

        adults = np.where(abs(self.ages - 53) < 12)[0]

        oaps = np.where(self.ages >= 65)[0]

        n = 0
        c = 0
        ya = 0
        a = 0
        oa = 0

        while n < len(working_id):
            new_house = np.random.choice(self.household_type)

            i = np.argmin(self.households[:, 0])

            if a == len(adults) and ya == len(youngadults) and c < len(children):
                while c < len(children):
                    self.households[len(children) - c, np.argmin(self.households[len(children -c)])] = children[c]
                    c += 1
                    n += 1

            elif new_house == 2:
                if oa < len(oaps):
                    self.households[i, 0] = oaps[oa]
                    working_id[oaps[oa]] = -1
                    oa += 1
                    n += 1

            elif new_house == 11:
                if a + 1 < len(adults):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = adults[a + 1]
                    working_id[adults[a]] = -1
                    working_id[adults[a + 1]] = -1
                    a += 2
                    n += 2

            elif new_house == 23:
                if oa + 1 < len(oaps):
                    self.households[i , 0] = oaps[oa]
                    self.households[i, 1] = oaps[oa + 1]
                    working_id[oaps[oa]] = -1
                    working_id[oaps[oa + 1]] = -1
                    oa += 2
                    n += 2

            elif new_house == 3:
                if ya + 1 < len(youngadults):
                    self.households[i , 0] = youngadults[ya]
                    working_id[youngadults[ya]] = -1
                    working_id[youngadults[ya + 1]] = -1
                    ya += 2
                    n += 2

            elif new_house == 0:
                if ya < len(youngadults):
                    self.households[i, 0] = youngadults[ya]
                    working_id[youngadults[ya]] = -1
                    ya += 1
                    n += 1

            elif new_house == 1:
                if a < len(adults):
                    self.households[i, 0] = adults[a]
                    working_id[adults[a]] = -1
                    a += 1
                    n += 1

            elif new_house == 4:
                if ya + 1 < len(youngadults) and c < len(children):
                    self.households[i , 0] = youngadults[ya]
                    self.households[i, 1] = youngadults[ya + 1]
                    self.households[i, 2] = children[c]
                    working_id[youngadults[ya]] = -1
                    working_id[youngadults[ya + 1]] = -1
                    working_id[children[c]] = -1
                    ya += 2
                    c += 1
                    n += 3

            elif new_house == 12:
                if a + 1 < len(adults) and c < len(children):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = adults[a + 1]
                    self.households[i, 2] = children[c]
                    working_id[adults[a]] = -1
                    working_id[adults[a + 1]] = -1
                    working_id[children[c]] = -1
                    a += 2
                    c += 1
                    n += 3

            elif new_house == 13:
                if a + 1 < len(adults) and c + 1 < len(children):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = adults[a + 1]
                    self.households[i, 2] = children[c]
                    self.households[i, 3] = children[c + 1]
                    working_id[adults[a]] = -1
                    working_id[adults[a + 1]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    a += 2
                    c += 2
                    n += 4

            elif new_house == 19:
                if a + 1 < len(adults) and ya < len(youngadults):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = adults[a + 1]
                    self.households[i, 2] = youngadults[ya]
                    working_id[adults[a]] = -1
                    working_id[adults[a + 1]] = -1
                    working_id[youngadults[ya]] = -1
                    a += 2
                    ya += 1
                    n += 3

            elif new_house == 5:
                if ya + 1 < len(youngadults) and c + 1 < len(children):
                    self.households[i , 0] = youngadults[ya]
                    self.households[i, 1] = youngadults[ya + 1]
                    self.households[i, 2] = children[c]
                    self.households[i, 3] = children[c + 1]
                    working_id[youngadults[ya]] = -1
                    working_id[youngadults[ya + 1]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    ya += 2
                    c += 2
                    n += 4

            elif new_house == 24:
                size = np.random.choice([3, 4, 5])
                if ya + size <= len(youngadults):
                    self.households[i, :size] = youngadults[ya:(ya + size)]
                    for i in range(size):
                        working_id[youngadults[ya + i]] = -1
                    ya += size
                    n += size

            elif new_house == 20:
                if a + 1 < len(adults) and ya + 1 < len(youngadults):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = adults[a + 1]
                    self.households[i, 2] = youngadults[ya]
                    self.households[i, 3] = youngadults[ya + 1]
                    working_id[adults[a]] = -1
                    working_id[adults[a + 1]] = -1
                    working_id[youngadults[ya]] = -1
                    working_id[youngadults[ya + 1]] = -1
                    a += 2
                    ya += 2
                    n += 4

            elif new_house == 21:
                if a  < len(adults) and ya < len(youngadults):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = youngadults[ya]
                    working_id[adults[a]] = -1
                    working_id[youngadults[ya]] = -1
                    a += 1
                    ya += 1
                    n += 2

            elif new_house == 14:
                if a + 1 < len(adults) and c + 2 < len(children):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = adults[a + 1]
                    self.households[i, 2] = children[c]
                    self.households[i, 3] = children[c + 1]
                    self.households[i, 4] = children[c + 2]
                    working_id[adults[a]] = -1
                    working_id[adults[a + 1]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    working_id[children[c + 2]] = -1
                    a += 2
                    c += 3
                    n += 5

            elif new_house == 15: 
                if a + 1 < len(adults) and c + 3 < len(children):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = adults[a + 1]
                    self.households[i, 2] = children[c]
                    self.households[i, 3] = children[c + 1]
                    self.households[i, 4] = children[c + 2]
                    self.households[i, 5] = children[c + 3]
                    working_id[adults[a]] = -1
                    working_id[adults[a + 1]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    working_id[children[c + 2]] = -1
                    working_id[children[c + 3]] = -1
                    a += 2
                    c += 4
                    n += 6

            elif new_house == 16:
                if a < len(adults) and c < len(children):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = children[c]
                    working_id[adults[a]] = -1
                    working_id[children[c]] = -1
                    a += 1
                    c += 1
                    n += 2

            elif new_house == 17:
                if a < len(adults) and c + 1 < len(children):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = children[c]
                    self.households[i, 2] = children[c + 1]
                    working_id[adults[a]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    a += 1
                    c += 2
                    n += 3

            elif new_house == 18:
                if a < len(adults) and c + 2 < len(children):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = children[c]
                    self.households[i, 2] = children[c + 1]
                    self.households[i, 3] = children[c + 2]
                    working_id[adults[a]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    working_id[children[c + 2]] = -1
                    a += 1
                    c += 3
                    n += 4

            elif new_house == 22:
                if a < len(adults) and ya + 1 < len(youngadults):
                    self.households[i , 0] = adults[a]
                    self.households[i, 1] = youngadults[ya]
                    self.households[i, 2] = youngadults[ya + 1]
                    working_id[adults[a]] = -1
                    working_id[youngadults[ya]] = -1
                    working_id[youngadults[ya + 1]] = -1
                    a += 1
                    ya += 2
                    n += 3

            elif new_house == 6:
                if ya + 1 < len(youngadults) and c + 2 < len(children):
                    self.households[i , 0] = youngadults[ya]
                    self.households[i, 1] = youngadults[ya + 1]
                    self.households[i, 2] = children[c]
                    self.households[i, 3] = children[c + 1]
                    self.households[i, 4] = children[c + 2]
                    working_id[youngadults[ya]] = -1
                    working_id[youngadults[ya + 1]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    working_id[children[c + 2]] = -1
                    ya += 2
                    c += 3
                    n += 5

            elif new_house == 7:
                if ya + 1 < len(youngadults) and c + 3 < len(children):
                    self.households[i , 0] = youngadults[ya]
                    self.households[i, 1] = youngadults[ya + 1]
                    self.households[i, 2] = children[c]
                    self.households[i, 3] = children[c + 1]
                    self.households[i, 4] = children[c + 2]
                    self.households[i, 5] = children[c + 3]
                    working_id[youngadults[ya]] = -1
                    working_id[youngadults[ya + 1]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    working_id[children[c + 2]] = -1
                    working_id[children[c + 3]] = -1
                    ya += 2
                    c += 4
                    n += 6

            elif new_house == 8:
                if ya < len(youngadults) and c < len(children):
                    self.households[i , 0] = youngadults[ya]
                    self.households[i, 1] = children[c]
                    working_id[youngadults[ya]] = -1
                    working_id[children[c]] = -1
                    ya += 1
                    c += 1
                    n += 2

            elif new_house == 9:
                if ya < len(youngadults) and c + 1 < len(children):
                    self.households[i , 0] = youngadults[ya]
                    self.households[i, 1] = children[c]
                    self.households[i, 2] = children[c + 1]
                    working_id[youngadults[ya]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    ya += 1
                    c += 2
                    n += 3

            elif new_house == 10:
                if ya < len(youngadults) and c + 2 < len(children):
                    self.households[i , 0] = youngadults[ya]
                    self.households[i, 1] = children[c]
                    self.households[i, 2] = children[c + 1]
                    self.households[i, 3] = children[c + 2]
                    working_id[youngadults[ya]] = -1
                    working_id[children[c]] = -1
                    working_id[children[c + 1]] = -1
                    working_id[children[c + 2]] = -1
                    ya += 1
                    c += 3
                    n += 4

        s = np.argmin(self.households[:, 0])
        return np.array(self.households[:s, :], dtype=np.int16)
