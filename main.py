import requests as rq
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

S_TIME = "1950-01-01"
E_TIME = "2026-03-20"
MIN_MAG = 1
FORMAT = "csv"

results_lock = Lock()
all_data = []

def getData(start_time, end_time, min_magnitude, format, timeout=120):
	BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
	PARAMS = {
		"format": format,
		"starttime": start_time,
		"endtime": end_time,
		"minmagnitude": min_magnitude
	}
	
	for attempt in range(3):
		try:
			data = rq.get(url=BASE_URL, params=PARAMS, timeout=timeout)
			if data.status_code == 200:
				return data
			elif data.status_code == 504 and attempt < 2:
				wait_time = 2 ** attempt
				time.sleep(wait_time)
				continue
			elif data.status_code == 400:
				raise Exception(f"400:{data.text}")
			else:
				raise Exception(f"API error: Status code {data.status_code}")
		except rq.exceptions.Timeout:
			if attempt < 2:
				wait_time = 2 ** attempt
				time.sleep(wait_time)
				continue
			raise Exception("Request timeout after retries")
	
	raise Exception("Failed after retries")

def fetch_chunk(start_time, end_time):
	"""Fetch data for a date range, with fallback to monthly chunks if needed"""
	global all_data
	
	start_str = start_time.strftime("%Y-%m-%d")
	end_str = end_time.strftime("%Y-%m-%d")
	
	try:
		response = getData(start_str, end_str, MIN_MAG, FORMAT)
		if response.text.strip():
			lines = response.text.split('\n')
			with results_lock:
				if all_data:
					lines = lines[1:]  # Skip header
				all_data.extend(lines)
		return (start_str, end_str, True, None)
	except Exception as e:
		error_str = str(e)
		# If range has too many events, recursively split by halves
		if error_str.startswith("400:") and "exceeds search limit" in error_str:
			mid = start_time + (end_time - start_time) / 2
			try:
				fetch_chunk(start_time, mid)
				fetch_chunk(mid + timedelta(days=1), end_time)
				return (start_str, end_str, True, None)
			except Exception as split_err:
				return (start_str, end_str, False, str(split_err)[:80])
		else:
			return (start_str, end_str, False, error_str[:80])

def getDataParallel(start_time, end_time, min_magnitude, format, max_workers=10):
	"""Fetch data using parallel requests with adaptive chunking"""
	global all_data
	all_data = []
	
	start_date = datetime.strptime(start_time, "%Y-%m-%d")
	end_date = datetime.strptime(end_time, "%Y-%m-%d")
	
	# Create list of date ranges (by month for faster initial fetching)
	date_ranges = []
	current = start_date
	while current < end_date:
		# Get last day of month
		if current.month == 12:
			month_end = current.replace(year=current.year + 1, month=1, day=1) - timedelta(days=1)
		else:
			month_end = current.replace(month=current.month + 1, day=1) - timedelta(days=1)
		
		if month_end > end_date:
			month_end = end_date
		
		date_ranges.append((current, month_end))
		current = month_end + timedelta(days=1)
	
	print(f"Fetching {len(date_ranges)} months of data using {max_workers} threads...")
	
	completed = 0
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		futures = {executor.submit(fetch_chunk, start, end): (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")) for start, end in date_ranges}
		
		for future in as_completed(futures):
			completed += 1
			start_str, end_str, success, error = future.result()
			if success:
				if completed % 50 == 0:
					print(f"  Progress: {completed}/{len(date_ranges)} months fetched")
			else:
				print(f"  ✗ {start_str} to {end_str}: {error}")
	
	print(f"Completed fetching {completed} month(s)")
	return '\n'.join(all_data).encode()

try:
	data = getDataParallel(S_TIME, E_TIME, MIN_MAG, FORMAT, max_workers=10)
	if data and len(data) > 0:
		with open("earthquakes.csv", "wb") as f:
			f.write(data)
		print("Data downloaded successfully!")
	else:
		print("Failed to retrieve data")
except Exception as e:
	print(f"Error: {e}")
