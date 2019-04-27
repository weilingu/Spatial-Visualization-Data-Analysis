# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:41:17 2019

@author: emily.gu
"""

import pandas as pd
import seaborn as sns
import os
os.environ["PROJ_LIB"]="C:\\Users\\emily.gu\\AppData\\Local\\Continuum\\anaconda3\\Library\\share"
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Polygonpatch
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from matplotlib import cm
import math
from sklearn import preprocessing
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
sns.set()

'''
# to impot the spreadsheet indivudually
data=pd.read_excel("C:\\Users\\emily.gu\\Desktop\\data visualization\\Income by Zipcode\\16zp14il.xls",header=[3,4])

# delete and clean rows to keep only value inputs  
index_type=list(map(type, data.index.tolist())) 
data=data.loc[map(lambda x:x is int, index_type)]

# clean column nanmes:
def rename_col(col):
    if "Unnamed" in col[1]:
        return col[0]
    else:
        return col[0]+"__"+col[1]
    
data.columns=map(rename_col,data.columns)

# create zipcode column and reset index
data=data.reset_index()
data=data.rename(columns={"index":"zipcode"})
'''

data=pd.read_csv("C:\\Users\\emily.gu\\Desktop\\data visualization\\Income by Zipcode\\16zpallagi.csv")
# drop the rows where zipcode==0, since it is the sum by state
data=data[data.zipcode!=0]
#data.STATE.unique()
#data.zipcode.unique()
#data[["A00100","A02650","A00300","A00600","A00700","A07100","A00900","A18425", "A04800","A10600","A06500"]].describe()
# aggregate data to zip code and state level
data_aggre_zip=data.groupby(by="zipcode",as_index=False, sort=False).sum()
data_aggre_state=data.groupby(by="STATE",as_index=False, sort=False).sum()
# convert the dollar amount into millions (already reported in thousands)
# calculate average for each dollar amount (N1:Number of returns)
# calculate percent of returns prepared by volunteers
for df in [data, data_aggre_zip, data_aggre_state]:
    for var in ["A00100","A02650","A00300","A00600","A00700",
                "A07100","A00900","A18425", "A04800","A10600","A06500"]:
        new_var="scaled_"+var
        df[new_var]=df[var]/1000
        new_var='avg_'+var
        df[new_var]=df[var]/df.N1
    df["pct_volunteer_prepare"]=df["TOTAL_VITA"]/df["N1"]

# make histogram: 
#1) historgram for Total tax payments amount
sns.distplot(data_aggre_zip.A10600,bins=20)
#2) historgram for average tax payment (Total tax payments amount/Number of returns with total income))
sns.distplot(data_aggre_zip.A10600/data_aggre_zip.N02650,bins=20)
#3)  historgram for Total tax payments amount, by tax payers category
category={1:"\$1 under \$25,000", 2 :"\$25,000 under \$50,000",3:"\$50,000 under \$75,000",
          4:"\$75,000 under \$100,000", 5:"\$100,000 under \$200,000", 6:"\$200,000 or more"}

figure=plt.figure(figsize=(6,7))
for num in list(category.keys()):
    payments_by_cat=sns.distplot(data[data.agi_stub==num].scaled_A10600,bins=20,label=category[num])
plt.legend()
plt.xlabel("Total tax payments amount (in millions)")
plt.title("Distribution of Tax Payments Amount \n by Annual Income Level \n",size=16,fontname='Times New Roman',verticalalignment='bottom',weight='normal' )
figure.savefig("C:\\Users\\emily.gu\\Desktop\\data visualization\\Tax Distribution Hist.jpg")


#4) histrogram for multiple selected columns to anlyze dataset:
var_plot={"scaled_A00100" : "Adjust gross income (in millions)" ,"scaled_A02650":"Total income amount (in millions)",
          "scaled_A00300":"Taxable interest amount (in millions)","scaled_A00600":"Ordinary dividends amount (in millions)",
          "scaled_A00700":"State and local income tax refunds amount (in millions)","scaled_A07100":"Total tax credits amount (in millions)",
          "scaled_A00900": "Business or professional net income (less loss) amount (in millions)","scaled_A18425":"State and local income taxes amount (in millions)",
          "scaled_A04800" : "Taxable income amount (in millions)","scaled_A10600" : "Total tax payments amount (in millions)","scaled_A06500":"Income tax amount (in millions)",
          "pct_volunteer_prepare" : "Percent of returns prepared by volunteer"}

ind=0
figure=plt.figure(figsize=(12,6*6))
while ind<12:
    plt.subplot(6,2,ind+1)
    sns.distplot(data_aggre_zip[list(var_plot.keys())[ind]],hist=True, bins=10)
    plt.xlabel(var_plot[list(var_plot.keys())[ind]])
    ind+=1
    
#5) histrogram for multiple selected columns to anlyze dataset, by tax payers category:
    # agi_stub: Size of adjusted gross income
ind=0
figure=plt.figure(figsize=(12,6*6))
while ind<12:
    plt.subplot(6,2,ind+1)
    for num in list(category.keys()):
        sub_data=data[data.agi_stub==num].dropna(subset=['pct_volunteer_prepare'])
        sns.distplot(sub_data[list(var_plot.keys())[ind]],hist=True, bins=10,label=category[num])
        plt.legend()
        plt.xlabel(var_plot[list(var_plot.keys())[ind]])
    ind+=1

# create boxplot by zipcode 
figure=plt.figure(figsize=(12,10))
data_boxplot=pd.melt(data, id_vars=['agi_stub'], value_vars=['A10600','A00900','A00700'])
sns.boxplot(x='variable',y='value',data=data_boxplot, hue='agi_stub')    

# plot contour
color=data["pct_volunteer_prepare"]
color_norm=(color-color.mean())/color.std()
plt.scatter(data['avg_A04800'],data['avg_A10600'],lw=0.1,c=color_norm, cmap=cm.get_cmap('Blues'))


'''
make maps: 
    
1) average tax payment amount by zipcode
2) total  tax payment amount by zipcode
3) average tax payment amount by state
4) percent of returns prepared by volunteers
5) relationship data between number of people who need help, average tax return, and..., use  sns.kdeplot
'''

# 1) average tax payment amount by zipcode

# draw the map, read the shape file by zip code 
fig,ax = plt.subplots()
fig.set_size_inches(17,11)
m=Basemap(llcrnrlon=-126,llcrnrlat=23,urcrnrlon=-66,urcrnrlat=52,projection='cyl',resolution='c')
m.fillcontinents(color='white',zorder=0)
m.readshapefile("C:\\Users\\Emily.Gu\\Desktop\\Python Challenge\\mapping code\\shape file\\USA_ZIP_Codes\\USA_ZIP_Codes",'zipcode',drawbounds=True,linewidth=0.1,color='lightgrey')
m.drawmapboundary(color='white')
zipcode_1=[]
for i in m.zipcode_info:
    zipcode_1+=[int(i['ZIP'])]

norm=Normalize()

## Plot the average tax paymen for each zip code area 
cmap =cm.get_cmap('Blues')
patches=[]
color=[]
for zipcode_2, geo in zip(zipcode_1, m.zipcode):
    target=data_aggre_zip[data_aggre_zip.zipcode==zipcode_2]
    color+=(target.avg_A10600).tolist()
    poly=Polygonpatch(geo,closed=True,zorder=2) 
    patches.append(poly)
collection=PatchCollection(patches)
collection.set_facecolor(cmap(norm(color)))
ax.add_collection(collection)

mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
mapper.set_array([0,1,0.2])
cbaxes = fig.add_axes([0.15,0.32,0.25,0.01])
cbar=plt.colorbar(mapper, orientation='horizontal', cax=cbaxes)
cbar.set_label('Dollar Amount (in millions)',fontname='Times New Roman',size=10)

ax.set_title("Average Tax Payments by Each Return",size=16,fontname='Times New Roman',verticalalignment='bottom',weight='normal')
fig.text( 0.15, 0.25,'$\\bf{Sources:}$ Internal Revenue Service', ha='left', va='center', 
         size=10, color='#555555',fontname='Times New Roman')
    
#2 total tax payment amount by zipcode

fig,ax = plt.subplots()
fig.set_size_inches(17,11)
m=Basemap(llcrnrlon=-126,llcrnrlat=20,urcrnrlon=-66,urcrnrlat=51,projection='cyl',resolution='c')

m.fillcontinents(color='white',zorder=0)
m.readshapefile("C:\\Users\\Emily.Gu\\Desktop\\Python Challenge\\mapping code\\shape file\\USA_ZIP_Codes\\USA_ZIP_Codes",'zipcode',drawbounds=True,linewidth=0,color='lightgrey')
m.drawmapboundary(color='white')

zipcode_1=[]
for i in m.zipcode_info:
    zipcode_1+=[int(i['ZIP'])]

norm=Normalize()

cmap =cm.get_cmap('Oranges')
patches=[]
color=[]
for zipcode_2, geo in zip(zipcode_1, m.zipcode):
    target=data_aggre_zip[data_aggre_zip.zipcode==zipcode_2]
    color+=(target.scaled_A02650).tolist()   
    poly=Polygonpatch(geo,closed=True,zorder=2) 
    patches.append(poly)
collection=PatchCollection(patches)
collection.set_facecolor(cmap(norm(color)))
ax.add_collection(collection)

mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
mapper.set_array([0,1,0.2])
cbaxes = fig.add_axes([0.15,0.32,0.25,0.01])
cbar=plt.colorbar(mapper, orientation='horizontal', cax=cbaxes)
cbar.set_label('Dollar Amount (in millions)',fontname='Times New Roman',size=14)

ax.set_title("2017 Income Reported by Each Return \n By Zip Code",size=20,fontname='Times New Roman',verticalalignment='bottom',weight='normal')
fig.text( 0.15, 0.25,'$\\bf{Sources:}$ Internal Revenue Service', ha='left', va='center', 
         size=14, color='#555555',fontname='Times New Roman')

# Add map inset
axins = zoomed_inset_axes(ax, 3.5, loc=4, axes_kwargs={"alpha":0.8})
axins.set_xlim(-104, -98)
axins.set_ylim(40, 44)

plt.xticks(visible=False)
plt.yticks(visible=False)

m2 = Basemap(llcrnrlon=-110,llcrnrlat=41,urcrnrlon=-106,urcrnrlat=45, ax=axins)
m2.fillcontinents(color='white',zorder=0)
m2.readshapefile("C:\\Users\\Emily.Gu\\Desktop\\Python Challenge\\mapping code\\shape file\\USA_ZIP_Codes\\USA_ZIP_Codes",'zipcode',drawbounds=True,linewidth=0.1,color='lightgrey')

m2.drawmapboundary(color='white')
zipcode_1=[]
for i in m.zipcode_info:
    zipcode_1+=[int(i['ZIP'])]

norm=Normalize()

cmap =cm.get_cmap('Oranges')
patches=[]
color=[]
for zipcode_2, geo in zip(zipcode_1, m2.zipcode):
    target=data_aggre_zip[data_aggre_zip.zipcode==zipcode_2]
    color+=(target.scaled_A02650).tolist()   
    poly=Polygonpatch(geo,closed=True,zorder=2) 
    patches.append(poly)
collection=PatchCollection(patches)
collection.set_facecolor(cmap(norm(color)))
axins.add_collection(collection)

mark_inset(ax, axins, loc1=1, loc2=3, fc="none", lw=0.7, ec='b')
fig.savefig("C:\\Users\\emily.gu\\Desktop\\data visualization\\Income by Zip Code.png",pad_inches=0)
#fig.savefig("P:\\Projects\\ANTITRUST\\ATDS SANGHVI (103461)\\KnowledgeBase\\Mapping\\Map Samples\\Inset Map Avg- EG.pdf",pad_inches=0)

# 3) average tax payment amount by state
fig,ax = plt.subplots()
fig.set_size_inches(17,11)
m=Basemap(llcrnrlon=-126,llcrnrlat=23,urcrnrlon=-66,urcrnrlat=52,projection='cyl',resolution='c')
m.fillcontinents(color='white',zorder=0)
#m.readshapefile("C:\\Users\\Emily.Gu\\Desktop\\Python Challenge\\mapping code\\shape file\\USA_ZIP_Codes\\USA_ZIP_Codes",'zipcode',drawbounds=True,linewidth=0.1,color='lightgrey')
m.readshapefile("C:\\Users\\emily.gu\\Desktop\\Python Challenge\\mapping code\\shape file\\cb_2017_us_state_500k\\cb_2017_us_state_500k",'state',drawbounds=True,linewidth=0.1,color='lightgrey')

m.drawmapboundary(color='white')
STATE_1=[]
for i in m.state_info:
    STATE_1+=[i['STUSPS']]

norm=Normalize()

cmap =cm.get_cmap('Purples')
patches=[]
color=[]
for STATE_2, geo in zip(STATE_1, m.state):
    target=data_aggre_state[data_aggre_state.STATE==STATE_2]
    #color+=(target.A10600/target.N02650).tolist() 
    color+=(target.A10600/target.N1).tolist() 
    poly=Polygonpatch(geo,closed=True,zorder=2) 
    patches.append(poly)
collection=PatchCollection(patches)
collection.set_facecolor(cmap(norm(color)))
ax.add_collection(collection)

mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
mapper.set_array([0,1,0.2])
cbaxes = fig.add_axes([0.15,0.32,0.25,0.01])
cbar=plt.colorbar(mapper, orientation='horizontal', cax=cbaxes)
cbar.set_label('Dollar Amount (in millions)',fontname='Times New Roman',size=10)

ax.set_title("Average Tax Payments by Each Return \ By State",size=16,fontname='Times New Roman',verticalalignment='bottom',weight='normal')
fig.text( 0.15, 0.25,'$\\bf{Sources:}$ Internal Revenue Service', ha='left', va='center', 
         size=10, color='#555555',fontname='Times New Roman')

#4) percent of returns prepared by volunteers
fig,ax = plt.subplots()
fig.set_size_inches(17,11)
m=Basemap(llcrnrlon=-126,llcrnrlat=23,urcrnrlon=-66,urcrnrlat=52,projection='cyl',resolution='c')
m.fillcontinents(color='white',zorder=0)
m.readshapefile("C:\\Users\\Emily.Gu\\Desktop\\Python Challenge\\mapping code\\shape file\\USA_ZIP_Codes\\USA_ZIP_Codes",'zipcode',drawbounds=True,linewidth=0.1,color='lightgrey')
m.drawmapboundary(color='white')
zipcode_1=[]
for i in m.zipcode_info:
    zipcode_1+=[int(i['ZIP'])]

norm=Normalize()

cmap =cm.get_cmap('Greens')
patches=[]
color=[]
for zipcode_2, geo in zip(zipcode_1, m.zipcode):
    target=data_aggre_zip[data_aggre_zip.zipcode==zipcode_2]
    color+=(target.TOTAL_VITA/target.N1).tolist()    #divide the number by million for readability
    poly=Polygonpatch(geo,closed=True,zorder=2) 
    patches.append(poly)
collection=PatchCollection(patches)
collection.set_facecolor(cmap(color))
ax.add_collection(collection)

mapper = cm.ScalarMappable( cmap=cmap)
mapper.set_array([0,1,0.2])
cbaxes = fig.add_axes([0.15,0.32,0.25,0.01])
plt.colorbar(mapper, orientation='horizontal', cax=cbaxes)
