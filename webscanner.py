import rquests
import re
import ssl
import certifi
from argparse import ArgumentParser
from urllib.parse import url parse
import socket
import pyfiglet

#pretty title
ascii_banner = pyfiglet.figlet_format("WEB SCANNER")
print(ascii_banner)


parser = ArgumentParser(
  prog='WebScanner',
  description='This is a website scanner that uses web requests to search for vulnerablities',
  epilog='Thanks for looking, credit to stuffy24'
)
#Help menu setup
parser.add_argument('-t', "--target", help="Use -t syntax to specify your target. Must be in full format https://website.com", required=True)

#needed for parsing cmd line argument
args = parser.parse_args()



#scanner function
def web_scanner(urls, verify_ssl=True):
  info_pattern = r"(password|api_key|email)" #add more patterns as neeeded #Checks for sensitive info #email might show false postives
  white_list = ["https://example.com", "https://example.com"] #add to whitelist as needed  # Add to remove redirect expectations
  directory_patterns = ["Index of", "Parent Directory", "Directory Listing", "Directory Contents"] #checks if they list their directories

  for url in urls:
    try:
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.9'} 

      #Set verify_ssl parameter for the requests.get() method
      response = requests.get(url, allow_redirects=True, headers=headers, verify=verify_ssl)

      #Check for sensitive information
      if re.search(info_pattern, response.text, re.IGNORECASE):
        print(f"Potential sensitive information found in URL: {url}")

      #Check for white list
      if response.url not in white_list:
        print(f"Possible open redirect vulnerability found in URL: {url}")
        print(f"Redirect URL: {response.url}") #Line good for troubleshooting

      #Check SSL/TLS certificate validity if the response is using HTTPS
      if response.url.startswitch("https") and response.raw.conncetion:
        cert = response.raw.connection.getpeercert()
        if ssl.match_hostname(cert, urlparse(response.url).hostname):
          print(f"SSL/TLS for {response.url} is valid.")
        else:
          print(f"SSL/TLS for {response.url} is invalid or could not be verified.") 

      #Check for directory listings
      if response.status_code == 200 and any(pattern in response.text for patttern in directory_patterns):
        print(f"Directory Listing enabled for URL: {url}")
        
    except requests.exceptions.RequestException:
      print(f"Failed to fetch URL: {url}") #fails if not a real website or using http

    #handle SSL/tls certificate verificaiton failures
    except ssl.SSLError:
      print(f"SSl/TLS certificate for {url} is invalid or could not be verified.")

if __name__ == "__main__":
  urls = [args.target]
  
  #Check if the url starts with 'https://' or 'http://' and set verify_ssl accordingly
  if urls[0].startswith(https://):
    web_scanner(urls, verify_ssl=True)
  elif urls[0].startswith(http://):
    web_scanner(urls, verify_ssl=False)
  else:
    print("Invalid URL. Please provide valid URL starting with 'https://' or 'http://'.")


        
