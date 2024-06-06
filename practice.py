import datetime


def current_date():
    date_now=datetime.datetime.now()
    
    correct_format_date=date_now.strftime("%B %d, %Y")    
    
       
    return correct_format_date

print(current_date())