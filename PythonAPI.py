import datetime
import logging
from typing import List
import pandas as pd

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchRecreationDotGov
import threading



def initiateCampFinder(search_window,recreation_area,weekends_only,nights):
    camping_finder = SearchRecreationDotGov(search_window=search_window,
                                            recreation_area=recreation_area,  # Glacier Ntl Park
                                            weekends_only=weekends_only,
                                            nights=nights
                                            )
    matches: List[AvailableCampsite] = camping_finder.get_matching_campsites(log=False, 
                                                                             verbose=False,
                                                                             continuous=True,
                                                                             polling_interval=5,
                                                                             search_forever=True,
                                                                             notify_first_try=False)
    

AreaCSV = pd.read_csv('data/RecAreaId.csv')
print(AreaCSV.head())




user_df = pd.read_csv('data/UserInfo2.csv')
print(user_df.head())
uniq_users = user_df['Name'].unique()

threads = []
for user in uniq_users:
    uniq_recs = user_df[user_df['Name'] == user]['Rec Area'].unique()
    
    #get number of weeks of advanced notice
    adv_notice_weeks = user_df[user_df['Name'] == user]['Weeks in Advance'].unique()
    #calculate end date
    adv_notice_days = adv_notice_weeks[0] * 7
    print(adv_notice_days)
    u = datetime.datetime.today()
    d = datetime.timedelta(days=int(adv_notice_days))
    start = u
    end = u + d
    date_range = SearchWindow(start_date = start, end_date = end)
    weekend_only_bool = user_df[user_df['Name'] == user]['Weekends Only'].unique()
    num_nights = user_df[user_df['Name'] == user]['Number of Nights'].unique()
    
    #Need a seperate thread for each user
    threads.append(threading.Thread(target=initiateCampFinder,args = (date_range,2782,weekend_only_bool[0],num_nights[0])))
    threads[-1].start()
    print(user)
    

for i in range(len(threads)):
    threads[i].join()
    
