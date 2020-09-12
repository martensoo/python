import pandas as pd
import io
import requests
import matplotlib.pyplot as plt

url="https://opendata.digilugu.ee/opendata_covid19_test_results.csv"
s=requests.get(url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))
#c = pd.read_csv("/Users/marten.soo/Downloads/opendata_covid19_test_results.csv")
c['datetrunc'] = pd.to_datetime(c.ResultTime, format='%Y-%m-%d %H:%M:%S').dt.floor('d')

#c = c[c['County'] == 'Harju maakond']
c = c.groupby(['datetrunc', 'AgeGroup', 'Gender', 'ResultValue']).size().reset_index(name='counts')
c = c[c['ResultValue'] == 'P']

fig, (ax, ax1, ax2) = plt.subplots(3)
ax1.plot(c[c.Gender=='M'].datetrunc,c[c.Gender=='M'].counts,label='M')
ax2.plot(c[c.Gender=='N'].datetrunc,c[c.Gender=='N'].counts,label='N')
ax1.set_title('Gender Male')
ax2.set_title('Gender Female')
ax1.set_ylim([0,20])
ax2.set_ylim([0,20])

for ageGroup in c['AgeGroup'].unique():
    ax.plot(c[c.AgeGroup==ageGroup].datetrunc,c[c.AgeGroup==ageGroup].counts,label=ageGroup)

ax.set_xlabel("dates")
ax.set_ylabel("positive tests")
ax.set_title("Age groups")
ax.legend(loc='best')