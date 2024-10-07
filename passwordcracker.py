import hashlib
from argparse import ArgumentParser
import pyfiglet
import time

#pretty title
ascii_banner = pyfiglet.figlet_format("PASSWORD CRACKER")
print(ascii_banner)


parser = ArgumentParser(
  prog='Password Cracker',
  description='This is a password cracker that uses a wordlist.',
  epilog='Thanks for looking!'
)

#set up help menu
parser.add_argument('-w', "--wordlist", help="Use the syntax -w to specify what wordlist you want to use")
parser.add_argument('-p', "--passwordhash", help="Puth the hash here with -p to specify which hash you want to crack.")


#pareses command line arguements
args = parser.parse_args()
wordlist = args.wordlist

def readwordlist():
  try:
    with open(wordlist, "r") as wordlist_file:
      words = (line.strip() for line in wordlist_file)
  except Exception as e:
    print("There was an error:", e)
  return words

def hash(wordlistpassword):
  result = hashlib.sha1(wordlistpassword.encode())
  #Can change sha1 to other methods
  return result.hexdigest()

def bruteforcewords(words, actual_password_hash):
  for guess_password in words:
    stripped_guess_password = guess_password.strip()
    if hash(stripped_guess_password) == actual_password_hash:
      print("Your password is:", stripped_guess_password)
      time.sleep(5)
      #If the password is found, it terminates the script here
      exit()

#Obtain the words from the wordslist
words = readwordlist()

#Obtain the actual passaword hash from the command-line arguemtns
actual_password_hash = args.passwordhash

#Running the Brute Force attack
bruteforce(words, actual_passwword_hash)

#It would be executed if your password was not in the wordlist
print("Unable to find password, not in wordlist."
