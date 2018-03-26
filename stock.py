# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 21:00:45 2018

@author: aptus
"""

import os 
import pandas as pd
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

#reading NameSheet.csv for metric_id
nameSheet = pd.read_csv(os.path.join(dir_path, 'NameSheet.csv'), header=None)

# get all marks id
marks = nameSheet[nameSheet.iloc[:,1].str.match('^marks')][[0,1]]
# get all percenage id
percntg = nameSheet[nameSheet.iloc[:,1].str.match('^percentage')][[0,1]]


#make a dict of marks
marksDict = dict(zip(marks[0], marks[1]))
#make a dict of percentage
percntgDict = dict(zip(percntg[0], percntg[1]))

print(marks)
print(percntg)
print(marksDict)
print(percntgDict)
# reading data from pd.csv
df = pd.read_csv(os.path.join(dir_path,'pd.csv'), names=['sid','mid','timestamp','value'])
df['flag'] = None
df['comment'] = None

I=0
def calcdf(key,count,foundDict):
    if key in marksDict:
        if "mean" in marksDict[key]:
            if(count>1):
                count=1;
                foundDict={}
            print("calculate mean")
            return 1;
        elif  "max" in marksDict[key]:
            count>2:
                count=2;
            print("calculate max")
            return 2;
        elif  "min" in marksDict[key]:
            print("calculate min")
            
        elif  "sdev" in marksDict[key]:
            print("calculate sdev")
            return 0;
        
    else:
        if "mean" in percntgDict[key]:
            print("calculate mean")
        elif  "max" in percntgDict[key]:
            print("calculate max")
        elif  "min" in percntgDict[key]:
            print("calculate min")
        elif  "sdev" in percntgDict[key]:
            print("calculate sdev")
        
    
while I < df.shape[0] :
    tmpMID = df.loc[I:I+3, 'mid']
    count=0
    foundDic=dict()
    for index, row in df.iterrows():
        print("Row[1]---------------->")
        print(row[1])
        print("Row---------------->")
        print(row)
        if row[1] in marksDict:
            print("Marks---------------->")
            print(marks)
            print("Marks[row[1]]---------------->")
            
            print(marksDict[row[1]])
            if row[1] in foundDic and  foundDic[row[1]]==1:
                #clean foundDic and count=0 
                    
                print("Count set 0 and foundDict={}")
                count=0
                foundDic={}
                foundDic[row[1]]=1
                count+=1
                print(marksDict[row[1]])
                count=calcdf(row[1],count);
                #print(row)
            else:
                
                print("Continue with marks finding"+str(count+1));
                count+=1;
                foundDic[row[1]]=1
                
                print(marksDict[row[1]])
                calcdf(row[1],count)
                #print(row)
                #in
        else:
            print("Percentage---------------->")
            print(percntg)
            print("Percentage[1]---------------->")
            
            print(percntgDict[row[1]])
            if row[1] in foundDic and  foundDic[row[1]]==1:
                #clean foundDic and count=0 
                print("Count set 0 and foundDict={}")
                count=0
                foundDic={}
                foundDic[row[1]]=1
                count+=1
                print(percntgDict[row[1]])
                #print(row)
                calcdf(row[1],count)
            else:
                print("Continue with percentage finding"+str(count+1));
                
                count+=1;
                foundDic[row[1]]=1
                
                print(percntgDict[row[1]])
                #print(row)
                calcdf(row[1],count)
            
               
    
    #print(tmpMID)
    break
