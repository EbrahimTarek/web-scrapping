import requests
from bs4 import BeautifulSoup
import pandas as pd 
import re

date = input('Please Enter a date in the following format yyyy-mm-dd: ').strip()
page = requests.get(f'https://www.filgoal.com/matches/?date={date}',verify=True) 
source = page.content
soup = BeautifulSoup(source,'lxml')

#Championship Name
new_list = [tag.a.get('href') for tag in soup.find_all('div','m')]
champion_name = [list[list.find("في")+2:].replace('-',' ').strip() for list in new_list]

#Teams
Team_A = [i.get_text().strip() for i in soup.select('.f strong')]
Team_B = [i.get_text().strip() for i in soup.select('.s strong')]

#Time of the Match
Time_of_match = [i.get_text().strip() for i in soup.select('.match-aux span')]
pattern = re.compile(r'\d{2}-\d{2}-\d{4} - \d{2}:\d{2}')
Date_Time_Match = [match.group() for item in Time_of_match for match in [re.search(r'\d{2}-\d{2}-\d{4} - \d{2}:\d{2}',item)] if match]  

#Results
Team_A_Result = [i.get_text().strip() for i in soup.select('.f b')]
Team_B_Result = [i.get_text().strip() for i in soup.select('.s b')]

match_details  = pd.DataFrame({
    'البطولة':champion_name,
    'الفريق الأول' : Team_A,
    'الفريق التانى' :Team_B,
    'ميعاد المباراة': Date_Time_Match ,
    'نتيجة المباراة' : [f'{i}-{x}'.strip() for i , x in zip(Team_A_Result,Team_B_Result)]})

match_details.to_excel(r'C:\Users\ebrahim.tarek\Desktop\Filgoal.xlsx',index=False)



