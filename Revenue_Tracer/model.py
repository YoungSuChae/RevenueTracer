import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

class SalesForecaster:
   
    def model(self):

        self.store_sales = pd.read_csv("Store.csv")

        self.store_sales = self.store_sales.drop(columns=['storeID', 'StoreName', 'StoreLocation', 'StoreNumber'])
        self.store_sales['Date'] = pd.to_datetime(self.store_sales['Date'], format="%Y-%m-%d")
        self.store_sales['Date'] = self.store_sales['Date'].dt.to_period("M")
        self.monthly_revenue = self.store_sales.groupby('Date').sum().reset_index()
        self.monthly_revenue['Date'] = self.monthly_revenue['Date'].dt.to_timestamp()
        self.monthly_revenue['Revenue_diff'] = self.monthly_revenue['MonthlyRevenue'].diff()
        self.monthly_revenue = self.monthly_revenue.dropna()

        supervised_data = self.monthly_revenue.drop(columns=['Date', 'MonthlyRevenue'])
        for i in range(1, 5):
            col_name = 'month_' + str(i)
            supervised_data[col_name] = supervised_data['Revenue_diff'].shift(i)
        self.supervised_data = supervised_data.dropna().reset_index(drop=True)

        train_data = self.supervised_data[:-12]
        test_data = self.supervised_data[-12:]

        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler.fit(train_data)
        train_data = scaler.transform(train_data)
        test_data = scaler.transform(test_data)

        self.X_train, self.y_train = train_data[:, 1:], train_data[:, 0:1]
        self.X_test, self.y_test = test_data[:, 1:], test_data[:, 0:1]
        self.y_train = self.y_train.ravel()
        self.y_test = self.y_test.ravel()

    
        lr_model = LinearRegression()
        lr_model.fit(self.X_train, self.y_train)
        self.lr_model = lr_model

    
        rev_dates = self.monthly_revenue['Date'][-12:].reset_index(drop=True)
        predict_df = pd.DataFrame(rev_dates)
        act_rev = self.monthly_revenue['MonthlyRevenue'][-13:].to_list()

        lr_predict = self.lr_model.predict(self.X_test)
        lr_predict = lr_predict.reshape(-1, 1)
        lr_pre_test_set = np.concatenate([lr_predict, self.X_test], axis=1)
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler.fit(self.supervised_data)
        lr_pre_test_set = scaler.inverse_transform(lr_pre_test_set)

        result_list = []
        for index in range(0, len(lr_predict)):
            result_list.append(lr_pre_test_set[index][0] + act_rev[index])
        lr_pre_series = pd.Series(result_list, name="Linear Prediction")
        predict_df = predict_df.merge(lr_pre_series, left_index=True, right_index=True)

        self.predict_df = predict_df

    
        lr_mse = np.sqrt(mean_squared_error(self.predict_df['Linear Prediction'], self.monthly_revenue['MonthlyRevenue'][-12:]))
        lr_mae = mean_absolute_error(self.predict_df['Linear Prediction'], self.monthly_revenue['MonthlyRevenue'][-12:])

    def plot_forecast(self):
        # Assuming self.monthly_revenue and self.predict_df are available here
        plt.figure(figsize=(7, 5))
        plt.plot(self.monthly_revenue['Date'], self.monthly_revenue['MonthlyRevenue'])
        plt.plot(self.predict_df['Date'], self.predict_df['Linear Prediction'])
        plt.title("Sales Forecasting")
        plt.xlabel("Date")
        plt.ylabel("Revenue")
        plt.legend(['Actual Revenue', 'Predicted Revenue'])
        return plt.gcf()
    
    @staticmethod
    def fourth_last_quarter_revenue():
        
        store_sales = pd.read_csv("Store.csv")
        store_sales = store_sales.drop(columns=['storeID', 'StoreName', 'StoreLocation', 'StoreNumber'])
        store_sales['Date'] = pd.to_datetime(store_sales['Date'])
        
        df = store_sales.groupby(pd.PeriodIndex(store_sales['Date'], freq="Q"))['MonthlyRevenue'].mean()

        # Sort the quarters and get the revenue of the fourth last and third last quarters
        fourth_last_quarter_revenue = df.sort_index().iloc[-4]
        fifth_last_quarter_revenue = df.sort_index().iloc[-5]

        # Calculate the percentage profit revenue change
        percentage_profit_revenue = ((fourth_last_quarter_revenue - fifth_last_quarter_revenue)  / fourth_last_quarter_revenue) * 100

        return round(percentage_profit_revenue)

    @staticmethod
    def third_last_quarter_revenue():
        
        store_sales = pd.read_csv("Store.csv")
        store_sales = store_sales.drop(columns=['storeID', 'StoreName', 'StoreLocation', 'StoreNumber'])
        store_sales['Date'] = pd.to_datetime(store_sales['Date'])
        
        df = store_sales.groupby(pd.PeriodIndex(store_sales['Date'], freq="Q"))['MonthlyRevenue'].mean()

        # Sort the quarters and get the revenue of the fourth last and third last quarters
        third_last_quarter_revenue = df.sort_index().iloc[-3]
        fourth_last_quarter_revenue = df.sort_index().iloc[-4]

        # Calculate the percentage profit revenue change
        percentage_profit_revenue = ((third_last_quarter_revenue - fourth_last_quarter_revenue) / third_last_quarter_revenue) * 100

        return round(percentage_profit_revenue)
    
    @staticmethod
    def second_last_quarter_revenue():
        
        store_sales = pd.read_csv("Store.csv")
        store_sales = store_sales.drop(columns=['storeID', 'StoreName', 'StoreLocation', 'StoreNumber'])
        store_sales['Date'] = pd.to_datetime(store_sales['Date'])
        
        df = store_sales.groupby(pd.PeriodIndex(store_sales['Date'], freq="Q"))['MonthlyRevenue'].mean()

        # Sort the quarters and get the revenue of the fourth last and third last quarters
        second_last_quarter_revenue = df.sort_index().iloc[-2]
        third_last_quarter_revenue = df.sort_index().iloc[-3]

        # Calculate the percentage profit revenue change
        percentage_profit_revenue = ((second_last_quarter_revenue - third_last_quarter_revenue) / second_last_quarter_revenue) * 100

        return round(percentage_profit_revenue)
    
    @staticmethod
    def last_quarter_revenue():
        
        store_sales = pd.read_csv("Store.csv")
        store_sales = store_sales.drop(columns=['storeID', 'StoreName', 'StoreLocation', 'StoreNumber'])
        store_sales['Date'] = pd.to_datetime(store_sales['Date'])
        
        df = store_sales.groupby(pd.PeriodIndex(store_sales['Date'], freq="Q"))['MonthlyRevenue'].mean()

        # Sort the quarters and get the revenue of the fourth last and third last quarters
        latest_quarter_revenue = df.sort_index().iloc[-1]
        second_last_quarter_revenue = df.sort_index().iloc[-2]
        # Calculate the percentage profit revenue change
        percentage_profit_revenue = ((latest_quarter_revenue - second_last_quarter_revenue) / latest_quarter_revenue) * 100

        return round(percentage_profit_revenue)
