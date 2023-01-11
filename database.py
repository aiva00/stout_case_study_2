import pandas as pd
import numpy as np

class Database:
    def __init__(self, csv_path : str) -> None:
        self.csv_path = csv_path
        self.df = self.load_data()
        self.lost_customers_count, self.lost_customers_df = self.get_lost_customers(self.df)
        self.new_customers_count, self.new_customers_df = self.get_new_customers(self.df)
    
    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)
        return df
    
    def query(self, df : pd.DataFrame) -> pd.DataFrame:
        
        data = 'some query'
        return data
    
    def get_lost_customers(self, df: pd.DataFrame):
        lost_customers_df = pd.DataFrame()
        lost_customers_count_df = pd.DataFrame()
        customers = set()

        for year in df['year'].unique():
            df_current_year = df[df['year'] == year].copy()
            
            # new_customers = set(df_current_year['customer_email'].unique()) - set(customers)
            # lost_customers_df = pd.concat([lost_customers_df, df_current_year[df_current_year['customer_email'].isin(new_customers)]])
            
            returning_customers = df_current_year[df_current_year['customer_email'].isin(customers)].copy()
            lost_customers = set(customers) - set(returning_customers)
            
            lost_customers_df = pd.concat([lost_customers_df, df_current_year[df_current_year['customer_email'].isin(lost_customers)]])
            lost_customers_count_df = pd.concat([lost_customers_count_df, pd.DataFrame({'year': [year], 'lost_customers' : [len(lost_customers)]})])
            
            customers.update(df_current_year['customer_email'].to_list())
        return lost_customers_count_df.reset_index(drop=True), lost_customers_df
    
    def get_new_customers(self, df: pd.DataFrame):
        new_customers_count_df = pd.DataFrame({'year' : [], 'customers' : []})
        customers = []

        for year in df['year'].unique():
            df_current_year = df[df['year'] == year]
            
            new_customers = set(df_current_year['customer_email'].unique()) - set(customers)
            new_customers_count_df = pd.concat([new_customers_count_df, pd.DataFrame({'year' : [year], 'customers' : [len(new_customers)]})], axis=0)
            
            customers = new_customers

        
        new_customers_df = pd.DataFrame()
        customers = []

        for year in df['year'].unique():
            df_current_year = df[df['year'] == year]
            
            new_customers = set(df_current_year['customer_email'].unique()) - set(customers)
            new_customers_df = pd.concat([new_customers_df, df_current_year[df_current_year['customer_email'].isin(new_customers)]])
            
            customers = new_customers

        return new_customers_count_df.reset_index(drop=True), new_customers_df.reset_index(drop=True)
    
    def query_revenue_over_years(self, df:pd.DataFrame) -> pd.DataFrame:
        df_plot = pd.DataFrame(df.groupby(['year'])['net_revenue'].agg('sum')).reset_index()
        df_plot['year'] = df_plot['year'].astype('int')
        
        return df_plot
    
    def query_revenue_lost_vs_gained(self, df:pd.DataFrame) -> pd.DataFrame:
        new_customer_revenue = pd.DataFrame(self.new_customers_df.groupby("year")["net_revenue"].agg("sum")).reset_index()
        revenue_lost_from_attrition = pd.DataFrame(self.lost_customers_df.groupby('year')['net_revenue'].agg('sum')).reset_index()

        df_plot = pd.merge(new_customer_revenue, revenue_lost_from_attrition, on='year')
        df_plot.columns=['Year', 'New Customer Revenue', 'Revenue Lost from Attrition']
        return df_plot
    
    def query_new_vs_lost_customers(self, df:pd.DataFrame) -> pd.DataFrame:
        df_plot = pd.merge(self.new_customers_count, self.lost_customers_count, on='year')
        df_plot.columns = ['Year','New Customers','Lost Customers']
        
        return df_plot