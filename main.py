from requests_html import HTMLSession
import pandas as pd
from datetime import datetime
from datetime import date
import Plotter
GAS_COLUMNS = ["Station", "City", "Price","Date","Time"]

def Get_Gas_Price(_City_Data):
    Session = HTMLSession()
    Html_Page = Session.get(_City_Data.iloc[0]) # URL
    List_Of_Div = Html_Page.html.find("div.rllt__details")
    List_Of_Info = pd.DataFrame(columns=["Station Name","City","Price"])    
    City_Phone = _City_Data.iloc[1:] # Store the phone numbers 

    for Station in List_Of_Div: # Loop through all gas stations found
        Station_String = Station.full_text # Get only the text
        # ID the Station Name
        Gas_Station_S_Idx = Station_String.find("Gas station") # Find the start of the string "Gas Station"
        Gas_Station_E_Idx = Gas_Station_S_Idx + len("Gas station") # Find the end of the string "Gas station"
        Station_Name = Station_String[0:Gas_Station_S_Idx] # Extract the station name

        # ID the address
        Station_String_Adr = Station_String[Gas_Station_E_Idx:] # Extract everything remaining after station name
        Dot_S_Idx = Station_String_Adr.find("·") # Find the first dot after the string "Gas station" This is the end of the address
        Station_Address = Station_String_Adr[:Dot_S_Idx] # Extract the address between the end of "Gas station" and first dot

        # ID the phone 
        Phone_S_Idx = Station_String_Adr.find(") ")+len(") ")
        Phone_E_Idx = Station_String_Adr.find("-")
        Station_Phone = Station_String_Adr[Phone_S_Idx:Phone_E_Idx]

        # ID the price
        Station_String_Price = Station_String_Adr[Dot_S_Idx:]  # Extract everything remaining after address
        Dollar_Post_Dot_Idx = Station_String_Price.find("$") # Find the start
        Slash_Post_Dollar_Idx = Station_String_Price.find("/Regular") # Find the end
        Station_Price = Station_String_Price[Dollar_Post_Dot_Idx+1:Slash_Post_Dollar_Idx] # Extract everything but the dollar sign

        # Validate results
        if (Station_Phone in list(City_Phone)): # Only store data for that town and has a price
            try:
                Station_Price_Flt = float(Station_Price) # Convert string to float
                if Station_Price_Flt > 0:
                    Temp_DF = pd.DataFrame( [[Station_Name,_City_Data.name,Station_Price_Flt]], columns=["Station Name","City","Price"])   
                    List_Of_Info = pd.concat([List_Of_Info,Temp_DF])
            except:
                next
        else:
            next

    List_Of_Info=List_Of_Info.sort_values("City")

    return(round(List_Of_Info["Price"].mean(),2)) # Return the average price

   
Store_Info = pd.read_csv("Store_Info.csv")
Price_Data = pd.DataFrame(columns = Store_Info.columns) 

for City in Store_Info.columns: # Loop through all of the columns (city names)
    Price_Data[City] = [Get_Gas_Price(Store_Info[City])] # Returns average and adds a column to the df
Price_Data["Date"] = [date.today().strftime("%m/%d/%Y")]
Filename = "Results.csv"
Price_Data.to_csv(Filename, mode='a', index=False, header=False)

Plotter.Plot()










