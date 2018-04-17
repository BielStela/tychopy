import urllib.request
import pandas as pd
from tqdm import tqdm
from io import StringIO
import requests


class Tycho():

    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = "https://www.tycho.pitt.edu/api/"
        self.cities = self.get_listing('city')
        self.admin1 = self.get_listing('admin1')
        self.countries = self.get_listing('country')

    # ----------------
    # listing methods
    # ----------------

    def get_listing(self, listing: str)-> pd.DataFrame:
        '''
        Builts the API call with the apikey for listings
        '''
        base_url = self.base_url
        # builds the url
        url = base_url + f'{listing}' + '?' + f'apikey={self.apikey}'
        req = urllib.request.urlopen(url)
        content = req.read()
        return pd.read_csv(StringIO(content.decode('utf8')))

    # ----------------
    # Region listing methods
    # ----------------

    def admin1_listing(self):
        '''
        returns admin listing as a DataFrame

        columns:
        --------
        CountryISO, CountryName, Admin1ISO, Admin1Name
        '''
        return self.admin1

    def city_listing(self):
        '''
        Returns city listing

        columns:
        --------
        CountryISO, CountryName, Admin1ISO, Admin1Name, Admin2Name, CityName
        '''
        return self.cities

    def country_listing(self):

        return self.countries

    # ----------------
    # Listing methods
    # ----------------

    def pathogen_listing(self):
        '''
        Return listing of pathogens as DataFrame

        columns:
        --------
        PathogenName, PathogenTaxonID
        '''
        content = self.get_listing('pathogen')
        return content

    def condition_listing(self):
        '''
        Return listing of conditions as DataFrame

        columns:
        --------
        ConditionName, ConditionSNOMED
        '''
        content = self.get_listing('condition')
        return content

    # ----------------
    # Query methods
    # ----------------

    def _get_region_level(self, region):
        '''
        Returns the region category: Country, admin1, City
        '''
        try:
            if region in self.cities:
                mask = self.cities == region
                region_cat = self.cities[mask].dropna(
                    axis=1, how='all').columns[0]

            elif region in self.admin1:
                mask = self.admin1 == region
                region_cat = self.admin1[mask].dropna(
                    axis=1, how='all').columns[0]

            else:
                mask = self.countries == region
                region_cat = self.countries[mask].dropna(
                    axis=1, how='all').columns[0]

        except IndexError:
            print('Region not found!')
            region_cat = None
        
        finally:
            return region_cat
    
    def query(self, region, condition, infer=False, region_cat='CountryName'):

        '''
        Builds Query with params
        '''
        url = self.base_url + 'query'
        
        if infer:
            region_infered = self._get_region_level(region)
            region_cat=region_infered

        params = {'apikey': self.apikey,
                  'ConditionName': condition,
                  region_cat: region, }

        req_raw = requests.get(url, params=params)
        response = req_raw.content.decode('utf8')
        return pd.read_csv(StringIO(response))


    def query_allcountries(self, condition):
        '''
        Returns condition present in all countries
        '''

        countries_unique = self.countries.iloc[:,1].unique()
        df = pd.DataFrame()
        for country in countries_unique:
            df = df.append(self.query(country, condition))
        
        return df

