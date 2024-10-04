from argparse import ArgumentParser
import secrets
import random
import string
#import pyfiglet

#Pretty banner
#  ascii_banner = pyfiglet.figlet_format("Password Generator")
#  print(ascii_banner)
#  print("-" * 50)


#Help Menu
parser = ArgumentParser(
  prog= 'Password Generator.',
  description= 'Generate passwords with this tool.',
  epilog= 'Thanks for checking this out!'
)


#Adding arguments to the help menu
parser.add_argument("-n", "--numbers", default=0, help="Adds amount of numbers to your password", type=int)
parser.add_argument("-l", "--lowercase", default=0, help="Adds amount of lowercase characters to your password", type=int)
parser.add_argument("-u", "--uppercase", default=0, help="Adds amount of uppercase characters to your password", type=int)
parser.add_argument("-s", "--special-chars", default=0, help="Adds amount of special characters to your password", type=int)
parser.add_argument("-t", "--total-length", type=int, help="This specifies length of password and will generate a completely random password, *Will ignore all other syntaxes*.")
parser.add_argument("-a", "--amount", default=1, help="Adds amount of passwords you want.", type=int)
parser.add_argument("-o", "--output-file", help="Outputs file")

#Parses the command line arguments
args = parser.parse_args()

#List
passwords = []

#loop
for _ in range(args.amount):
  if args.total_length:
    #generates random password with this length
    passwords.append("".join(
      [secrets.choice(string.digits + string.ascii_letters + string.punctuation)
       for _ in range(args.total_length)]))
    
  else:
    password = []

    for _ in range(args.numbers):
      password.append(secrets.choice(string.digits))
      
    for _ in range(args.uppercase):
      password.append(secrets.choice(string.ascii_uppercase))

    for _ in range(args.lowercase):
      password.append(secrets.choice(string.ascii_lowercase))

    for _ in range(args.special_chars):
      password.append(secrets.choice(string.punctuation))

    random.shuffle(password)

    password = ''.join(password)
  
    passwords.append(password)
    
if args.output_file:
  with open(args.output_file, 'w') as f:
    f.write('\n'.join(passwords))

print('\n'.join(passwords))
