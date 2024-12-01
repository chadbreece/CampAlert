from datetime import datetime
import logging
from typing import List
import pandas as pd
from datetime import datetime

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchRecreationDotGov


logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)

month_of_december = SearchWindow(start_date=datetime(year=2024, month=12, day=1),
                             end_date=datetime(year=2024, month=12, day=8))

camping_finder = SearchRecreationDotGov(search_window=month_of_december,
                                        recreation_area=2782,  # Glacier Ntl Park
                                        weekends_only=False,
                                        nights=1)

camping_finder.get_matching_campsites(log=True, verbose=True,
                                  continuous=True,
                                  polling_interval=5,
                                  search_forever=True,
                                  notify_first_try=False)
    

#print(matches)

'''

AreaCSV = pd.read_csv('RecAreaId.csv')
print(AreaCSV.head())




user_df = pd.read_csv('CampsiteInfo - Sheet1.csv')
print(user_df.head())
uniq_users = user_df['Name'].unique()
for user in uniq_users:
    uniq_recs = user_df[user_df['Name'] == user]['Rec Area'].unique()
    
    #get number of weeks of advanced notice
    adv_notice_weeks = user_df[user_df['Name'] == user]['Weeks in Advance'].unique()
    #calculate end date
    adv_notice_days = adv_notice_weeks * 7
    u = datetime.datetime.strptime("2011-01-01","%Y-%m-%d")
    d = datetime.timedelta(days=adv_notice_days)
    start = u
    end = u + d
    date_range = SearchWindow(start_date = start, end_date = end)
    weekend_only_bool = user_df[user_df['Name'] == user]['Weekends Only'].unique()
    num_nights = user_df[user_df['Name'] == user]['Number of Nights'].unique()
    
    #Need a seperate thread for each user
    camping_finder = SearchRecreationDotGov(search_window=date_range,
                                            recreation_area=2782,  # Glacier Ntl Park
                                            weekends_only=weekend_only_bool[0],
                                            nights=num_nights[0],
                                            )
    
    matches: List[AvailableCampsite] = camping_finder.get_matching_campsites(log=True, verbose=True,
                                      continuous=True,
                                      polling_interval=5,
                                      search_forever=True,
                                      notify_first_try=False)
    
print(datetime.today())
    
print(user, uniq_recs)
'''
