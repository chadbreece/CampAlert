import datetime
import logging
from typing import List
import pandas as pd

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchRecreationDotGov
import threading
import yaml

from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Open and load the YAML file
with open('email_info.yaml', 'r') as file:
    email_info = yaml.safe_load(file)


def initiateCampFinder(user,user_email,search_window,recreation_area,weekends_only,nights):
    camping_finder = SearchRecreationDotGov(search_window=search_window,
                                            recreation_area=recreation_area,  # Glacier Ntl Park
                                            weekends_only=weekends_only,
                                            nights=nights,
                                            # offline_search=Tue,
                                            # offline_search_path=f'./offline_searches/{user}.json',
                                            )
    matches: List[AvailableCampsite] = camping_finder.get_matching_campsites(log=False, 
                                                                             verbose=False,
                                                                             continuous=True,
                                                                             polling_interval=5,
                                                                             search_forever=False,
                                                                             notify_first_try=False)

    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = "CampAlert: Campsite Found!"

    # Body of the email
    body = "This is where we will put the campsite info"
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with SMTP_SSL(email_info['email_server_smtp_server'], email_info['email_server_smtp_server_port']) as server:
            server.ehlo()  # Secure the connection
            server.login(email_info['email_server_user'], email_info['email_server_password'])  # Log in to the SMTP server
            text = msg.as_string()  # Convert the email to string format
            server.sendmail(email_info['email_server_user'], user_email, text)  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

    

AreaCSV = pd.read_csv('data/RecAreaId.csv')
print(AreaCSV.head())




user_df = pd.read_csv('data/UserInfo2.csv')
print(user_df.head())
uniq_users = user_df['Name'].unique()

threads = []
for user in uniq_users:
    uniq_recs = user_df[user_df['Name'] == user]['Rec Area'].unique()
    user_email = user_df[user_df['Name'] == user]['Email'].unique()[0]

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
    threads.append(threading.Thread(target=initiateCampFinder,args = (user,user_email,date_range,2782,weekend_only_bool[0],num_nights[0])))
    threads[-1].start()
    print(user)
    

for i in range(len(threads)):
    threads[i].join()
    
