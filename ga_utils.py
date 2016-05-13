import json
import pandas as pd
import auth

service = auth.main()

def list_accounts():
	service = auth.main()
	accounts = service.management().accounts().list().execute()
	df = pd.read_json(json.dumps(accounts.get('items')))
	return df[['id','name']]

def list_properties(account):
	properties = service.management().webproperties().list(
        accountId=account).execute()
	df = pd.read_json(json.dumps(properties.get('items')))
	return df[['accountId', 'id' , 'name']]

def list_profiles(account, property):
	profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()
	df = pd.read_json(json.dumps(profiles.get('items')))
	return df

def get_example(profile_id):
	return ga_to_df(service.data().ga().get(
		ids='ga:' + profile_id,
		start_date='7daysAgo',
		end_date='today',
		metrics='ga:sessions,ga:bounceRate',
		dimensions='ga:date'
	).execute())

def ga_to_df(d):
	columns = [x['name'] for x in d['columnHeaders']]
	rows = [x for x in d['rows']]
	return pd.DataFrame(rows, columns=columns)
