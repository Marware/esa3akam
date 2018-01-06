# -*- coding: utf-8 -*-
import datetime
import pytz
from pytz import timezone

spec = ['و','دقائق','دقيقة']
sa3at = ['الواحدة' ,'الثانية' ,'الثالثة','الرابعة','الخامسة', 'السادسة', 'السابعة','الثامنة','التاسعة','العاشرة','الحادية عشر','الثانية عشر']
dq3shr = ['تماماً' ,'دقيقة','دقيقتان','عشر','عشرون','ثلاثون','أربعون','خمسون']
a7ad = ['احدى','اثنى','ثلاث','أربعة','خمسة','ستة','سبعة','ثمانية','تسعة','عشرة'] 
wqtyom = ['ظهراً','عصراً','مساءً','صباحاً','ليلاً','فجراً']

def get_d2e2a(tm):

    mn = int(tm.minute)
    dq = ""
    if mn < 3:
        dq = dq3shr[mn]
    
    if mn >= 3 and mn < 11:
        dq = a7ad[mn-1] + " " + spec[1]
    
    if mn >= 11 and mn < 20:
        dq = a7ad[mn-11] + " " + dq3shr[3] + " " + spec[0]
    
    if mn >= 21 and mn < 30:
        dq = a7ad[mn-21] + " " + spec[0] + dq3shr[4] + " " + spec[2]
        
    if mn >= 31 and mn < 40:
        dq = a7ad[mn-31] + " " + spec[0] + dq3shr[5] + " " + spec[2]
        
    if mn >= 41 and mn < 50:
        dq = a7ad[mn-41] + " " + spec[0] + dq3shr[6] + " " + spec[2]
                        
    if mn >= 51 and mn < 60:
        dq = a7ad[mn-51] + " " +spec[0] + dq3shr[7] + " " + spec[2]
        
    if mn == 20:
        dq = dq3shr[4] + " " + spec[2]

    if mn == 30:
        dq = dq3shr[5] + " " +spec[2]

    if mn == 40:
        dq = dq3shr[6] + " " +spec[2]
        
    if mn == 50:
        dq = dq3shr[7] + " " +spec[2]
    
    #print dq
    return dq         

def get_daytime(hr):

    if hr >= 0 and hr < 5:
        dytm = wqtyom[5]
        
    if hr >= 5 and hr < 11:
        dytm = wqtyom[3]
        
    if hr >= 11 and hr < 14:
        dytm = wqtyom[0]
        
    if hr >= 14 and hr < 16:
        dytm = wqtyom[1]
        
    if hr >= 16 and hr < 20:
        dytm = wqtyom[2]
                        
    if hr >= 20 and hr < 24:
        dytm = wqtyom[4]
        
    return dytm        
                                                          
def main():

    clt = timezone('Africa/Cairo')
    utc_dt = datetime.datetime.now(clt)
    sidx = int(utc_dt.hour)
    sa3a = ""
    if sidx <= 12:
        sa3a = sa3at[sidx-1]
    if sidx > 12:
        sa3a = sa3at[sidx-13]
        
    hr = utc_dt.hour    
    mn = utc_dt.minute
    
    dytm = ""
    
    d2e2a = get_d2e2a(utc_dt)
    t1 = ""
    if mn == 0:
        t1 = sa3a + " " + d2e2a
    else:
        t1 = sa3a + " " + spec[0] + d2e2a
    
    dytm = get_daytime(hr)

        
    tim = t1 + " " + dytm
    
    ar = "الساعة الآن "
    time_in_arabic = str(ar).decode('utf-8') + tim.decode('utf-8') 

    print time_in_arabic


if __name__ == "__main__":
  main()
