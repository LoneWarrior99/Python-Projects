from argparse import ArgumentParser
import requests
import sys
from urllib.parse import urljoin
import pyfiglet

parser = ArgumentParser(
  prog='Robots.txt crawler',
  description='This tools searches for a website\'s robot.txt file and then pulls words from those sites.', 
  epilog= 'Thanks for looking, base code is from Stuffy24'
)

parser.add_argument('-t', "--target", help="Use the syntax -t to specify your target.", required=True)

args = parser.parse_args()

ascii_banner = pyfiglet.figlet_format("ROBOT CRAWLER")
print(ascii_banner)


def robots_text():
  #this adds /robots.txt to the end of the URL we specified.
  #this is going to get rid of all the extra things like spaces, periods, etc. Then it will take the url we gave and join with the robot url
  robots_url = urljoin(args.target.rstrip("/"), "robots.txt")

  #Send a Get request to get the contents of the robots.txt file
  #See the robot.txt
  response = requests.get(robots_url)

  #Make sure the request was successful
  #returns as a txt format
  if response.status_code == 200:
    return response.text
  else:
    return None

def format_urls(disallowed_paths):
  base_url = args.target.rstrip("/")
  formatted_urls = []
  for path in disallowed_paths:
    url = urljoin(base_url, path)
    formatted_urls.append(url)
  return formatted_urls

def main():
  robots_txt = robots_text()
  if robots_txt:
    disallowed_paths = []
    lines = robots_txt.splitlines()
    for line in lines:
      if line.startswith("Disallow:"):
        path = line.split(":", 1)[1].strip()
        disallowed_paths.append(path)
    formatted_urls = format_urls(disallowed_paths)
    for url in formatted_urls:
      print(url)
  else:
    print("Failed to retrieve robots.txt file.")

if __name__ == "__main__":
  main()

"""
BASH SCRIPT FOR FILE

#!/bin/bash

# use syntax(./cewlforloop file)
# we remove the / so that linux doesn't think we are changing dir
# We are going to search for unique words that have 8 characters and saving it to a api.txt for a wordlist
# then meta file will look at the files and get the meta data then writes it out to api-meta.txt
# then email_file will look for any unique emails and write it out to api-email.txt
# finally it will go back and do it again for each line
  
while read line
  do
    defanged=$(echo "$line" | tr -d '/')
    mkdir "$defanged"
    cd "$defanged"
    cewl -m 8 -w $defanged"api.txt" -a --meta_file $defanged"api-meta.txt" -e --email_file $defanged"api-email.txt" $line
    cd ..

  done < $1
  


"""

  
