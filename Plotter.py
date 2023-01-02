import pandas as pd
import plotly.graph_objects as go

def Plot():
    All_Data = pd.read_csv("Results.csv") # Read in the csv to a dataframe
    City_Avg = pd.DataFrame()
    City_Info = pd.DataFrame(columns = ["Date","Price"])
    City_List = list(All_Data.drop(columns="Date").columns) # All data but date
    fig = go.Figure()

    for City in City_List: # Loop through the list of cities
        City_Info["Price"] = All_Data[City] # Store the particular data for that city
        City_Info["Date"] = All_Data["Date"]
        Dates = City_Info["Date"].unique().tolist() # Exctract a list of dates
        Date_Avg = []
        for Date in Dates:
            Date_Avg.append(round(City_Info[City_Info["Date"].str.contains(Date)]["Price"].mean(),2)) # Find the values that contain the specified date, and average them 

        # Wrap it all up
        City_Avg["Date"] = Dates 
        City_Avg[City] = Date_Avg

        fig.add_trace(go.Scatter(x= City_Avg["Date"], y=City_Avg[City],name = City))
        fig.update_xaxes(tickformat = '%B %d %Y')
    fig.update_layout(title="Local Gas Prices", xaxis_title="Date", yaxis_title="Price ($)")
    fig.write_html("Gas Prices"+".html")
    fig.show()

if __name__ == '__main__':
    Plot()