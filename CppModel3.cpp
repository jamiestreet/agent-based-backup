#include <vector>
#include <iostream>
#include <random>

using namespace std;

vector<int> iteration(const int nPop, float TransmProb, int meetAve, int work_meetAve, vector<int> states, vector<int> infTypes, vector<vector<int>> households1, vector<int> household_no, vector<vector<int>> workplaces1, vector<int> workplace_no, vector<int> selfIsolating, int LockdownBool, vector<int> workplace_critical, float TransmProbHouse, int SchoolsClosed, int WorkFromHomeBool){
    random_device randomDevice;
    mt19937 generator(randomDevice());
    poisson_distribution<int> distribution(meetAve);
    poisson_distribution<int> distribution10(work_meetAve);
    uniform_real_distribution<double> distribution2(0, 1);
    vector<int> infected(nPop);
    for (int i=0; i < nPop; i++){
        if (selfIsolating[i] == 0){
            const int meeting_no = distribution(generator);
            vector<int> meetings1;
            uniform_int_distribution<int> distribution3(0,nPop -1);
            int h = 0;
            for (int m=0; m < households1[household_no[i]].size(); m++){
                if (households1[household_no[i]][m] != i){
                    meetings1.push_back(households1[household_no[i]][m]);
                }
            }
            for (int j=0; j < meetings1.size(); j++){
                if (states[meetings1[j]] == 2 && selfIsolating[meetings1[j]] == 0){
                    if (states[i] == 0){
                        double p = distribution2(generator);
                        if (p < TransmProbHouse * infTypes[meetings1[j]]){
                            infected[i] = 1;
                        };
                    };
                };
            }
            vector<int> meetings;
            if (workplace_no[i] > -1){
                if (workplaces1[workplace_no[i]].size() > 1){
                    uniform_int_distribution<int> distribution11(0, workplaces1[workplace_no[i]].size()-1);
                    int b = 0;
                    int c = distribution10(generator);
                    if (workplace_critical[workplace_no[i]] < 3) {
                        if (LockdownBool == 1){
                            if (workplace_critical[workplace_no[i]] < 2){
                                c = 0;
                            }
                        } else if (WorkFromHomeBool == 1){
                            if (workplace_critical[workplace_no[i]] == 0){
                                c = 0;
                            }
                        }
                    } else if (workplace_critical[workplace_no[i]] == 3){
                        if (SchoolsClosed == 1){
                            c = 0;
                        }
                    }
                    while (b < c){
                        int y = distribution11(generator);
                        if (workplaces1[workplace_no[i]][y] != i){
                            meetings.push_back(workplaces1[workplace_no[i]][y]);
                            b++;
                        }
                    }
                }
            }
            for (int k=0; k < meeting_no; k++){
                int a = distribution3(generator);
                if (a >= i){
                    ++a;
                };
                meetings.push_back(a);
            };
            for (int j=0; j < meetings.size(); j++){
                if (states[meetings[j]] == 2 && selfIsolating[meetings[j]] == 0){
                    if (states[i] == 0){
                        double p = distribution2(generator);
                        if (p < TransmProb * infTypes[meetings[j]]){
                            infected[i] = 1;
                        };
                    };
                };
            };
        };
    };
    return infected;
};

vector<int> update_new_infs(int nPop, vector<int> states, vector<int> new_infs){
    for (int i=0; i < nPop; i++){
        if (new_infs[i] == 1){
            states[i] = 1;
        };
    };
    return states;
}

vector<int> update_inf_types(int nPop, vector<int> infTypes, vector<int> new_infs, vector<float> severities, vector<int> ages){
    for (int i=0; i < nPop; i++){
        if (new_infs[i] == 1){
            random_device randomDevice;
            mt19937 generator(randomDevice());
            uniform_real_distribution<double> distribution7(0, 1);
            float a = distribution7(generator);
            float sympProb = severities[ages[i]];
            if (a < sympProb){
                infTypes[i] = 2;
            } else{
                infTypes[i] = 1;
            }
        }
    } return infTypes;
}

vector<int> update_lats(int nPop, vector<int> states, vector<int> latLen){
    for (int i=0; i < nPop; i++){
        if (states[i] == 1){
            ++latLen[i];
        };
    };
    return latLen;
}

vector<int> update_infs(int nPop, vector<int> states, vector<int> infLen){
    for (int i=0; i < nPop; i++){
        if (states[i] == 2){
            ++infLen[i];
        };
    };
    return infLen;
}

vector<int> check_infs(int nPop, vector<int> infP, vector<int> infLen, vector<int> states){
    for (int i=0; i < nPop; i++){
        if (states[i] == 2){
            if (infLen[i] == infP[i]){
                states[i] = 3;
            };
        };
    };
    return states;
}

vector<int> check_lats(int nPop, vector<int> latP, vector<int> latLen, vector<int> states){
    for (int i=0; i < nPop; i++){
        if (states[i] == 1){
            if (latLen[i] == latP[i]){
                states[i] = 2;
            };
        };
    };
    return states;
}

vector<int> setLatP(int nPop){
    random_device randomDevice;
    mt19937 generator(randomDevice());
    lognormal_distribution<double> distribution4(1.501524205, 0.07145896398);
    vector<int> latP(nPop);
    for (int i=0; i < nPop; i++){
        latP[i] = ceil(distribution4(generator));
    };
    return latP;
}

vector<int> setInfP(int nPop){
    random_device randomDevice;
    mt19937 generator(randomDevice());
    lognormal_distribution<double> distribution5(2.064055712, 0.1754185243);
    vector<int> infP(nPop);
    for (int i=0; i < nPop; i++){
        infP[i] = ceil(distribution5(generator));
    };
    return infP;
}

vector<int> setAges(int nPop, vector<float> age_dist){
    vector<int> ages(nPop);
    for (int i=0; i < nPop; i++){
            random_device randomDevice;
            mt19937 generator(randomDevice());
            uniform_real_distribution<double> distributionA(0, 1);
            double a = distributionA(generator);
            float b = 0;
            int c = -1;
            while (b < 1){
                c++;
                b = b + age_dist[c];
                if (a < b){
                    ages[i] = c;
                    b = 1;
                }
            }
    } return ages;
}

vector<vector<int>> households(int nPop, vector<int> ages, vector<float> household_dist){
    vector<vector<int>> h_holds;
    int c = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] < 2){
            c++;
        }
    }
    int ya = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] < 4 && ages[i] > 1){
            ya++;
        }
    }
    int a = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] < 7 && ages[i] > 3){
            a++;
        }
    }
    int oap = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] > 6){
            oap++;
        }
    }
    vector<int> children(c);
    vector<int> young_adults(ya);
    vector<int> adults(a);
    vector<int> oaps(oap);

    int c1 = 0;
    int ya1 = 0;
    int a1 = 0;
    int oap1 = 0;

    for (int i=0; i < nPop; i++){
        if (ages[i] < 2){
            children[c1] = i;
            c1++;
        } else if (ages[i] < 4 && ages[i] > 1)
        {
            young_adults[ya1] = i;
            ya1++;
        } else if (ages[i] < 7 && ages[i] > 3)
        {
           adults[a1] = i;
           a1++;
        } else{
            oaps[oap1] = i;
            oap1++;
        }
    } 

    int c2 = 0;
    int ya2 = 0;
    int a2 = 0;
    int oap2 = 0;

    int n = 0;

    while (n < nPop){
        random_device randomDevice;
        mt19937 generator(randomDevice());
        uniform_real_distribution<double> distributionB(0, 1);
        float t = 0;
        float s = distributionB(generator);
        float u = -1;
        while (t < 1){
            u++;
            t = t + household_dist[u];
            if (s < t){
                t = 1;
            }
        }
        if (ya2 > ya - 1 && a2 > a - 1 && c2 < c){
            int y = 0;
            while (c2 < c){
                h_holds[y].push_back(children[c2]);
                y++;
                c2++;
            }
        }
        else if (u == 0){
            if (ya2 < ya){
                vector<int> house = {young_adults[ya2]};
                ya2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 1)
        {   
            if (a2 < a){
                vector<int> house = {adults[a2]};
                a2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 2)
        {
            if (oap2 < oap){
                vector<int> house = {oaps[oap2]};
                oap2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 3)
        {
            if (ya2 < ya){
                vector<int> house = {young_adults[ya2], young_adults[ya2 + 1]};
                ya2 = ya2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 4)
        {
            if (ya2 < ya - 1 && c2 < c){
                vector<int> house = {young_adults[ya2], young_adults[ya2 + 1], children[c2]};
                ya2 = ya2 + 2;
                c2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 5)
        {
            if (ya2 < ya - 1 && c2 < c - 1){
                vector<int> house = {young_adults[ya2], young_adults[ya2 + 1], children[c2], children[c2 + 1]};
                ya2 = ya2 + 2;
                c2 = c2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 6)
        {
            if (ya2 < ya - 1 && c2 < c - 2){
                vector<int> house = {young_adults[ya2], young_adults[ya2 + 1], children[c2], children[c2 + 1], children[c2 + 2]};
                ya2 = ya2 + 2;
                c2 = c2 + 3;
                h_holds.push_back(house);
            }
        }
        else if (u == 7)
        {
            if (ya2 < ya - 1 && c2 < c - 3){
                vector<int> house = {young_adults[ya2], young_adults[ya2 + 1], children[c2], children[c2 + 1], children[c2 + 2], children[c2 + 3]};
                ya2 = ya2 + 2;
                c2 = c2 + 4;
                h_holds.push_back(house);
            }
        }
        else if (u == 8)
        {
            if (ya2 < ya && c2 < c){
                vector<int> house = {young_adults[ya2], children[c2]};
                ya2++;
                c2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 9)
        {
            if (ya2 < ya && c2 < c - 1){
                vector<int> house = {young_adults[ya2], children[c2], children[c2 + 1]};
                ya2++;
                c2 = c2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 10)
        {
            if (ya2 < ya && c2 < c - 2){
                vector<int> house = {young_adults[ya2], children[c2], children[c2 + 1], children[c2 + 2]};
                ya2++;
                c2 = c2 + 3;
                h_holds.push_back(house);
            }
        }

        else if (u == 11)
        {
            if (a2 < a - 1){
                vector<int> house = {adults[a2], adults[a2 + 1]};
                a2 = a2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 12)
        {
            if (a2 < a - 1 && c2 < c){
                vector<int> house = {adults[a2], adults[a2 + 1], children[c2]};
                a2 = a2 + 2;
                c2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 13)
        {
            if (a2 < a - 1 && c2 < c - 1){
                vector<int> house = {adults[a2], adults[a2 + 1], children[c2], children[c2 + 1]};
                a2 = a2 + 2;
                c2 = c2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 14)
        {
            if (a2 < a - 1 && c2 < c - 2){
                vector<int> house = {adults[a2], adults[a2 + 1], children[c2], children[c2 + 1], children[c2 + 2]};
                a2 = a2 + 2;
                c2 = c2 + 3;
                h_holds.push_back(house);
            }
        }
        else if (u == 15)
        {
            if (a2 < a - 1 && c2  < c - 3){
                vector<int> house = {adults[a2], adults[a2 + 1], children[c2], children[c2 + 1], children[c2 + 2], children[c2 + 3]};
                a2 = a2 + 2;
                c2 = c2 + 4;
                h_holds.push_back(house);
            }
        }
        else if (u == 16)
        {
            if (a2 < a && c2 < c){
                vector<int> house = {adults[a2], children[c2]};
                a2++;
                c2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 17)
        {
            if (a2 < a && c2 < c - 1){
                vector<int> house = {adults[ya2], children[c2], children[c2 + 1]};
                a2++;
                c2 = c2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 18)
        {
            if (a2 < a && c2 < c - 2){
                vector<int> house = {adults[a2], children[c2], children[c2 + 1], children[c2 + 2]};
                a2++;
                c2 = c2 + 3;
                h_holds.push_back(house);
            }
        }
        else if (u == 19)
        {
            if (a2 < a - 1 && ya2 < ya){
                vector<int> house = {adults[a2], adults[a2 + 1], young_adults[ya2]};
                a2 = a2 + 2;
                ya2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 20)
        {
            if (a2 < a - 1 && ya2 < ya - 1){
                vector<int> house = {adults[a2], adults[a2 + 1], young_adults[ya2], young_adults[ya2 + 1]};
                a2 = a2 + 2;
                ya2 = ya2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 21)
        {
            if (a2 < a && ya2 < ya){
                vector<int> house = {adults[a2], young_adults[ya2]};
                a2++;
                ya2++;
                h_holds.push_back(house);
            }
        }
        else if (u == 22)
        {
            if (a2 < a && ya2 < ya - 1){
                vector<int> house = {adults[ya2], young_adults[ya2], young_adults[ya2 + 1]};
                a2++;
                ya2 = ya2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 23)
        {
            if (oap2 < oap - 1){
                vector<int> house = {oaps[oap2], oaps[oap2 + 1]};
                oap2 = oap2 + 2;
                h_holds.push_back(house);
            }
        }
        else if (u == 24)
        {
            if (ya2 < ya - 3){
                vector<int> house = {young_adults[ya2], young_adults[ya2 + 1], young_adults[ya2 + 2], young_adults[ya2 + 3]};
                ya2 = ya2 + 4;
                h_holds.push_back(house);
            }
        }
        n = c2 + ya2 + a2 + oap2;
    }  
    return h_holds;
}

vector<int> households_numbering(int nPop, vector<vector<int>> households1){
    vector<int> household_no(nPop);
    for (int i=0; i < households1.size(); i++){
        for (int j=0; j < households1[i].size(); j++){
            household_no[households1[i][j]] = i;
        }
    }
    return household_no;
}

vector<vector<int>> workplaces(int nPop, vector<int> ages, vector<float> workplace_dist){
    vector<vector<int>> w_places;
    int k = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] == 0){
            k++;
        }
    }
    int t = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] == 1){
            t++;
        }
    }
    int a = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] < 7 && ages[i] > 1){
            a++;
        }
    }
    int oap = 0;
    for (int i=0; i < nPop; i++){
        if (ages[i] > 6){
            oap++;
        }
    }
    vector<int> kids(k);
    vector<int> teens(t);
    vector<int> adults(a);
    vector<int> oaps(oap);

    int k1 = 0;
    int t1 = 0;
    int a1 = 0;
    int oap1 = 0;

    for (int i=0; i < nPop; i++){
        if (ages[i] == 0){
            kids[k1] = i;
            k1++;
        } else if (ages[i] == 1){
            teens[t1] = i;
            t1++;
        } else if (ages[i] < 7 && ages[i] > 1)
        {
           adults[a1] = i;
           a1++;
        } else{
            oaps[oap1] = i;
            oap1++;
        }
    }

    int k2 = 0;
    int t2 = 0;
    int a2 = 0;
    int oap2 = 0;

    while (k2 < k){
        vector<int> school;
        if (k - k2 > 29){
            for (int i=0; i < 30; i++){
                school.push_back(kids[k2]);
                k2++;
            }
        } else{
            while (k2 < k){
                school.push_back(kids[k2]);
                k2++;
            }
        }
        school.push_back(adults[a2]);
        a2++;
        w_places.push_back(school);
    }

    while (t2 < t){
        vector<int> school;
        if (t - t2 > 29){
            for (int i=0; i < 30; i++){
                school.push_back(teens[t2]);
                t2++;
            }
        } else{
            while (t2 < t){
                school.push_back(teens[t2]);
                t2++;
            }
        }
        school.push_back(adults[a2]);
        a2++;
        w_places.push_back(school);
    }
    random_device randomDevice;
    mt19937 generator(randomDevice());
    uniform_real_distribution<double> distributionC(0, 1);
    uniform_int_distribution<int> distributionD(3, 10);
    uniform_int_distribution<int> distributionE(11, 30);
    uniform_int_distribution<int> distributionF(31, 50);
    
    while (a2 < a){
        float x = 0;
        float s = distributionC(generator);
        float u = -1;
        while (x < 1){
            u++;
            x = x + workplace_dist[u];
            if (s < x){
                x = 1;
            }
        }
        if (a2 == a - 1){
            vector<int> workplace;
            workplace.push_back(adults[a2]);
            a2++;
            w_places.push_back(workplace);
        } else if (u == 0){
            if (a2 < a - 1){
                vector<int> workplace;
                for (int i=0; i < 2 ; i++){
                    workplace.push_back(adults[a2]);
                    a2++;
                }
                w_places.push_back(workplace);
            }
        } else if (u == 1){
            int workplace_size = distributionD(generator);
            if (a2 < a - workplace_size){
                vector<int> workplace;
                for (int i=0; i < workplace_size; i++){
                    workplace.push_back(adults[a2]);
                    a2++;
                }
                w_places.push_back(workplace);
            }
        } else if (u == 2){
            int workplace_size = distributionE(generator);
            if (a2 < a - workplace_size){
                vector<int> workplace;
                for (int i=0; i < workplace_size; i++){
                    workplace.push_back(adults[a2]);
                    a2++;
                }
                w_places.push_back(workplace);
            }
        } else if (u == 3){
            int workplace_size = distributionF(generator);
            if (a2 < a - workplace_size){
                vector<int> workplace;
                for (int i=0; i < workplace_size; i++){
                    workplace.push_back(adults[a2]);
                    a2++;
                }
                w_places.push_back(workplace);
            }
        }
    } 
    return w_places;
}

vector<int> workplace_numbering(int nPop, vector<vector<int>> workplaces1){
    vector<int> workplace_no(nPop, -1);
    for (int i=0; i < workplaces1.size(); i++){
        for (int j=0; j < workplaces1[i].size(); j++){
            workplace_no[workplaces1[i][j]] = i;
        }
    }
    return workplace_no;
}

vector<int> workplace_critical_assign(int nPop, vector<vector<int>> workplaces1, vector<int> ages){
    random_device randomDevice;
    mt19937 generator(randomDevice());
    uniform_real_distribution<double> distributionC(0, 1);
    vector<int> workplace_critical(workplaces1.size());
    for (int i=0; i < workplaces1.size(); i++){
        if (ages[workplaces1[i][0]] > 1 && ages[workplaces1[i][0]] < 7){
            float m = distributionC(generator);
            if (m < 0.3){
                workplace_critical[i] = 2;
            }
            else if (m < 0.7){
                workplace_critical[i] = 1;
            }
        }
        else if (ages[workplaces1[i][2]] < 2){
            workplace_critical[i] = 3;
        }
    }
    return workplace_critical;
}

vector<int> check_selfIsolating(int nPop, vector<int> states, vector<int> infTypes, vector<int> selfIsolating, vector<int> infLen){
    for (int i=0; i < nPop; i++){
        if (infTypes[i] == 2 && infLen[i] > 2 && states[i] == 2){
            selfIsolating[i] = 1;
        }
        if (states[i] == 3){
            selfIsolating[i] = 0;
        }
    } return selfIsolating;
}

vector<int> random_testing(int nPop, vector<int> states, vector<int> selfIsolating, vector<int> infTypes, float testingProb){
    random_device randomDevice;
    mt19937 generator(randomDevice());
    uniform_real_distribution<double> distributionX(0, 1);
    for (int i = 0; i < nPop; i++){
        if (selfIsolating[i] == 0){
            if (states[i] == 2){
                if (infTypes[i] == 1){
                    float d = distributionX(generator);
                    if (d < testingProb){
                        selfIsolating[i] = 1;
                    }
                }
            }
        } else if (selfIsolating[i] == 1){
            if (states[i] == 3){
                selfIsolating[i] = 0;
            }
        }
    }
    return selfIsolating;
}

int main() {
    int nPop = 202626;
    int inf0 = 4;
    float TransmProbOrg = 0.016;
    float TransmProb = 0.016;
    int meetAveOrg = 10;
    int work_meetAveOrg = 9;
    int meetAve = 10;
    int work_meetAve = 9;
    int days = 365;
    vector<float> age_dist = {0.11, 0.1, 0.12, 0.12, 0.12, 0.13, 0.1, 0.08, 0.04, 0.08};
    vector<float> severities = {0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.9};
    vector<float> household_dist = {0.075, 0.075, 0.14, 0.09, 0.05, 0.04, 0.0075, 0.0075, 0.0075, 0.0075, 0.0075, 0.1, 0.05, 0.05, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.05, 0.02, 0.02, 0.01, 0.1, 0.03};
    vector<float> workplace_dist = {0.2, 0.4, 0.3, 0.1};
    vector<int> latP = setLatP(nPop);
    vector<int> infP = setInfP(nPop);
    int time = 0;
    vector<int> states(nPop);
    vector<int> infTypes(nPop);
    vector<int> latLen(nPop, -1);
    vector<int> infLen(nPop, -1);
    vector<int>susc(days);
    vector<int>exp(days);
    vector<int>inf(days);
    vector<int>rec(days);
    int LockdownBool = 0;
    int SchoolClosureBool = 0;
    int WorkFromHomeBool = 0;
    int T1 = 12;
    int T1i = 30;
    int T1ii = 57;
    int T2 = 78;
    int T3 = 92;
    int T4 = 100;
    int T5 = 111;
    int T6 = 126;
    int T7 = 152;
    int T8 = 174;
    int T9 = 183;
    int T10 = 191;
    int T11 = 234;
    int T12 = 261;
    int T12i = 244;
    int T13 = 277;
    int T14 = 294;
    int T15 = 295;
    float SocialDEffect = 0.25;
    float LockdownEffect = 0.15;
    for (int i=0; i < inf0; i++){
       states[i] = 2;
       infTypes[i] = 2;
    };
    vector<int> ages = setAges(nPop, age_dist);
    vector<vector<int>> households1 = households(nPop, ages, household_dist);
    vector<int> household_no = households_numbering(nPop, households1);
    vector<vector<int>> workplaces1 = workplaces(nPop, ages, workplace_dist);
    vector<int> workplace_no = workplace_numbering(nPop, workplaces1);
    vector<int> workplace_critical = workplace_critical_assign(nPop, workplaces1, ages);
    vector<int> selfIsolating(nPop);
    int selfIsolatingBool = 0;
    vector<int> newInfections;
    while(time < days){
        if (time == 0){
            TransmProb = TransmProbOrg * 0.9;
        }
        if (time == T1){
            meetAve = ceil(meetAve * LockdownEffect*2);
            LockdownBool = 1;
            TransmProb = TransmProbOrg * SocialDEffect * 1.2;
        }
        if (time == T1i){
            selfIsolatingBool = 1;
            meetAve = ceil(meetAveOrg * LockdownEffect * 4);
        }
        if (time == T1ii){
            WorkFromHomeBool = 1;
            LockdownBool = 0;
            meetAve = ceil(meetAveOrg / 3);
            TransmProb = TransmProbOrg * SocialDEffect * 2;
        }
        if (time == T2){
            meetAve = ceil(meetAveOrg * 0.4);
        }
        if (time == T3){
            meetAve = ceil(meetAveOrg * 0.5);
        }
        if (time == T4){
            TransmProb = TransmProbOrg * 0.6;
        }
        if (time == T5){
            meetAve = ceil(meetAveOrg * 0.6);
        }
        if (time == T6){
            WorkFromHomeBool = 0;
            TransmProb = TransmProb * 0.75;
        }
        if (time == T7){
            meetAve = meetAveOrg * 0.8;
        }
        if (time == T8){
            SchoolClosureBool = 0;
        }
        if (time == T9){
            TransmProb = TransmProbOrg * SocialDEffect * 1.8;
            meetAve = ceil(meetAveOrg * 0.7);
        }
        if (time == T10){
            WorkFromHomeBool = 1;
        }
        if (time == T11){
            LockdownBool = 1;
            meetAve = ceil(meetAveOrg * 0.6);
            WorkFromHomeBool = 0;
        }
        if (time == T12){
            LockdownBool = 0;
            meetAve = ceil(meetAveOrg);
            WorkFromHomeBool = 1;
        }
        if (time == T12i){
            TransmProbOrg = TransmProbOrg * 1.05;
            TransmProb = TransmProbOrg * 0.6;
        }
        if (time == T13){
            SchoolClosureBool = 1;
        }
        if (time == T14){
            SchoolClosureBool = 0;
        }
        if (time == T15){
            SchoolClosureBool = 1;
            LockdownBool = 1;
            meetAve = ceil(meetAveOrg * LockdownEffect * 3);
        }
        states = check_infs(nPop, infP, infLen, states);
        states = check_lats(nPop, latP, latLen, states);
        if (selfIsolatingBool == 1){
            selfIsolating = check_selfIsolating(nPop, states, infTypes, selfIsolating, infLen);
        }
        /*if (testingFact == 1){
            selfIsolating = random_testing(nPop, states, selfIsolating, infTypes, testingProb);
        } */
        vector<int> new_infs = iteration(nPop, TransmProb, meetAve, work_meetAve, states, infTypes, households1, household_no, workplaces1, workplace_no, selfIsolating, LockdownBool, workplace_critical, TransmProbOrg, SchoolClosureBool, WorkFromHomeBool);
        int o2 = 0;
        for (int i=0; i < new_infs.size(); i++){
            if (new_infs[i] == 1){
                o2++;
            }
        }
        newInfections.push_back(o2);
        states = update_new_infs(nPop, states, new_infs);
        infTypes = update_inf_types(nPop, infTypes, new_infs, severities, ages);
        infLen = update_infs(nPop, states, infLen);
        latLen = update_lats(nPop, states, latLen);
        int s=0;
        int e=0;
        int f=0;
        int r=0;
        for (int i=0; i < nPop; i++){
            if (states[i] == 0){
                ++s;
            } else if (states[i] == 1){
                ++e;
            } else if (states[i] == 2){
                ++f;
            } else if (states[i] == 3){
                ++r;
            }
        };
        susc[time] = s;
        exp[time] = e;
        inf[time] = f;
        rec[time] = r;
        ++time;
        cout << time << ": " << f;
        cout << "\n ";
    };
    /*
    cout << "\n";
    cout << "susc = [";
    for (int i=0; i < days-1; i++){
        cout << susc[i] << ", ";
    }
    cout << susc[days - 1] << "]";
    cout << "\n";
    cout << "exp = [";
    for (int i=0; i < days-1; i++){
        cout << exp[i] << ", ";
    }
    cout << exp[days - 1] << "]";
    cout << "\n";
    cout << "inf = [";
    for (int i=0; i < days-1; i++){
        cout << inf[i] << ", ";
    }
    cout << inf[days - 1] << "]"; */
    cout << "\n";
    cout << "rec = [";
    for (int i=0; i < days-1; i++){
        cout << rec[i] << ", ";
    }
    cout << rec[days - 1] << "]";
    cout << "\n";
    cout << "cum = [";
    for (int i=0; i<days-1; i++){
        cout << newInfections[i] << ", ";
    }
    cout << newInfections[days - 1] << "]";
    return 0;
}