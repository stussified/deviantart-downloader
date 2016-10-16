import requests
from bs4 import BeautifulSoup
import argparse
import os

def deviant_downloader(account):
	s = requests.session()
	url = "http://backend.deviantart.com/rss.xml?q=gallery:{}".format(account)
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"}

	r = s.get(url, headers=headers)
	soup = BeautifulSoup(r.text, "html.parser")
	items = [item.get_text() for item in soup.find_all("link")]

	for item in items:
		r = s.get(item, headers=headers)
		soup = BeautifulSoup(r.text, "html.parser")
		find_link = soup.find_all("a", {"class": "dev-page-button dev-page-button-with-text dev-page-download"})
		if find_link:
			download = find_link[0].get("href")
			title = item.rsplit("/", 1)[-1]
			filename = download.rsplit("/", 1)[-1].rsplit("?",1)[0]
			print "trying to download {} by {}".format(title, account)
			d = s.get(download, stream=True)
			
			if not os.path.exists("download"):
				os.makedirs("download")

			with open("download/"+filename, 'wb') as f:
				for chunk in d.iter_content(chunk_size=1024):
					if chunk:
						f.write(chunk)
			print "{} by {} has finished downloading.".format(title, account)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("account", help="The account name you want to download from.")
	args = parser.parse_args()
	account = args.account
	deviant_downloader(account)

if __name__=="__main__":
	main()
