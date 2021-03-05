import pandas as pd
import numpy as np

# load data
ipums = pd.read_csv("data/ipums_FL_raw.csv")

# Map the lowering function to all column names
ipums.columns = map(str.lower, ipums.columns)

# recode sex
ipums['sex'] = ipums['sex'].map(lambda x: "male" if x == 1 else "female")
ipums['female'] = ipums['sex'].map(lambda x: 0 if x == "male" else 1)

# add age-squared
ipums = ipums.assign(age_sq = ipums['age']**2)

# rename hispand (detailed)
ipums = ipums.rename(columns={"hispand": "hispan_detailed"})

# dummy for hispan
ipums['hispan_d'] = ipums['hispan'].map(lambda x: 1 if x != 0 else 0)

# dummy for Black
ipums['black_d'] = ipums['race'].map(lambda x: 1 if x == 2 else 0)

# dummy for Asian
    #---
    #4: Chinese
    #5: Japanese
    #6: Other Asian or Pacific Islander
    #---
ipums['asian_d'] = ipums['race'].map(lambda x: 1 if x in [4, 5, 6] else 0)

# dummy for each educational attainment categories
    #---
    #(i) Completed less than 12 years of schooling
    #(ii) Completed exactly 12 years of schooling
    #(iii) Completed 1-2 years of college
    #(iv) Completed exactly 4 years of college
    #(v) Completed 5+ years of college
    #---

ipums['educ1_d'] = ipums['educ'].map(lambda x: 1 if x in range(0, 7) else 0)
ipums['educ2_d'] = ipums['educ'].map(lambda x: 1 if x == 6 else 0)
ipums['educ3_d'] = ipums['educ'].map(lambda x: 1 if x in range(7, 9) else 0)
ipums['educ4_d'] = ipums['educ'].map(lambda x: 1 if x == 10 else 0)
ipums['educ5_d'] = ipums['educ'].map(lambda x: 1 if x == 11 else 0)

# dummy for each of 12 major occupation categories
    # https://usa.ipums.org/usa/volii/occ2018.shtml

ipums['occ_manag'] = ipums['occ'].map(lambda x: 1 if x in range(10, 1000) else 0)
ipums['occ_comp_eng'] = ipums['occ'].map(lambda x: 1 if x in range(1000, 2000) else 0)
ipums['occ_edu_leg_art'] = ipums['occ'].map(lambda x: 1 if x in range(2000, 3000) else 0)
ipums['occ_health_tech'] = ipums['occ'].map(lambda x: 1 if x in range(3000, 3600) else 0)

ipums['occ_serv'] = ipums['occ'].map(lambda x: 1 if x in range(3600, 4700) else 0)
ipums['occ_sales'] = ipums['occ'].map(lambda x: 1 if x in range(4700, 5000) else 0)
ipums['occ_office'] = ipums['occ'].map(lambda x: 1 if x in range(5000, 6000) else 0)
ipums['occ_farm_fish'] = ipums['occ'].map(lambda x: 1 if x in range(6000, 6200) else 0)

ipums['occ_constr'] = ipums['occ'].map(lambda x: 1 if x in range(6200, 7000) else 0)
ipums['occ_maintn'] = ipums['occ'].map(lambda x: 1 if x in range(7000, 7700) else 0)
ipums['occ_prod'] = ipums['occ'].map(lambda x: 1 if x in range(7700, 9000) else 0)
ipums['occ_transport'] = ipums['occ'].map(lambda x: 1 if x in range(9000, 10000) else 0)

# dummy for 'public sector worker'
ipums['psw_d'] = ipums['classwkr'].map(lambda x: 1 if x == 1 else 0)

# dummy for 'wage worker last year'
    #---
    #Equals 1 if individual worked 1 or more weeks last year 
    #AND was not self-employed
    #AND was not an unpaid worker
    #
    #Equals 0 otherwise
    #---
    
ipums['wagework_lastyear'] = np.where( (ipums['wkswork2'] > 0) & (ipums['classwkr'] == 2), 1, 0)

# Annual hours worked
    #---
    #Computed as usual hours worked per week multiplied by the midpoint 
    #value of the interval for the individual’s weeks worked last year
    #---

def wkswork_mid(x):
    if x == 1:
        return(0.5*(1 + 13))
    elif x == 2:
        return(0.5*(14 + 26))
    elif x == 3:
        return(0.5*(27 + 39))
    elif x == 4:
        return(0.5*(40 + 47))
    elif x == 5:
        return(0.5*(48 + 49))
    elif x == 6:
        return(0.5*(50 + 52))
    else:
        return(None)  

ipums['annl_hrs_wrkd'] = ipums['uhrswork'] * ipums['wkswork2'].map(lambda x: wkswork_mid(x)) 

# Nonlabor income
    #---
    #Total family income minus own wage income
    #---
ipums['nonlabor_inc'] = ipums['ftotinc'] - ipums['incwage']

 # Hourly wage
    #---
    #Calculated as total family income last year divided by annual hours worked
    #---
ipums['hourly_wage'] = ipums['ftotinc'] / ipums['annl_hrs_wrkd'] 

# Natural logs of annual hours worked, nonlabor income, and hourly wage
with np.errstate(invalid='ignore'): 
    ipums['log_annl_hrs_wrkd'] = np.log(ipums['annl_hrs_wrkd'].replace(0, np.nan))
    ipums['log_nonlabor_inc'] = np.log(ipums['nonlabor_inc'].replace(0, np.nan))
    ipums['log_hourly_wage'] = np.log(ipums['hourly_wage'].replace(0, np.nan))
    
ipums.to_csv('data/ipums_FL.csv')  


