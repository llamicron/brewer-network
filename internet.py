import urllib2

# Would normally name this module "network", but given the circumstances,
# I'm calling it "internet". Kinda cheesy, but whatever

def check_connection():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False
