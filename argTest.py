import argparse

parser = argparse.ArgumentParser(description='simulation of sniffy data')
parser.add_argument('-c', '--clientID', help='clientID number', default=10) 
parser.add_argument('-l', '--location', help='geohash for location', default='gcncxgvu5rb7')

args = parser.parse_args()

print(args.clientID)
print(args.location)

