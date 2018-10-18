from modules import Lookup, PortScan, Whois
import os, io

curDir = os.getcwd()

class Investigate:
    
    def __init__(self):
        self.host = Host()

    def changeIP(self):
        print('Please enter IP address of host: ')
        ip = input('(e.g. 10.80.1.1) > ')
        self.host.ip = ip
        print('Assigned host ip of {}'.format(self.host.ip))

    def changeDomain(self):
        print('Please enter Domain Name of host: ')
        domainName = input('(e.g. google.com) > ')    
        self.host.domainName = domainName
        print('Assigned host domain name of {}'.format(self.host.domainName))

    def hostInfo(self):
        print('----------------------------------------------------')

        print()
        print('Current host info: ')
        print('IP: {}'.format(self.host.ip))
        print('Domain Name: {}'.format(self.host.domainName))
        print()
        print('----------------------------------------------------')

    def printReport(self):
        print()
        print('----------------------------------------------------')
        for prop, val in vars(self.host).items():
            print('{} : {}'.format(prop, val))
        print('----------------------------------------------------')

    def exportReport(self):
        print('Exporting report...')

        reportDir = curDir + '/reports'
        if not os.path.isdir(reportDir):
              os.mkdir(reportDir)

        if not self.host.domainName:
            reportPath = reportDir + '/' + self.host.ip + '_report.txt'
        else:
            reportPath = reportDir + '/' + self.host.domainName + '_report.txt'

        with open(reportPath, 'w') as f:
            for prop, val in vars(self.host).items():
                f.write('{} : {}\n'.format(prop, val))
        print('Report Exported to {}!'.format(reportPath))

    def openInvestigation(self):
        valid = False

        while not valid:
            print('Opening investigation')
            print('What do you know about the host?')
            print('1: IP address')
            print('2: Domain Name')
            
            cmd = input('> ')

            if cmd == '1':
                valid = True
                self.changeIP()
            elif cmd == '2':
                valid = True
                self.changeDomain()

            else:
                print('Choose a valid option!')
                print()
           

    def displayInvestMenu(self):
        print()
        print('Choose an option: ')
        print('0: Display help')
        print('1: Print working host info')
        print('2: Print Investigation report')
        print('3: Lookup missing info')
        print('4: Nmap it')
        print('5: Get whois info')
        print('96: Export Investigation')
        print('97: Change IP')
        print('98: Change Domain Name')
        print('99: Back to main menu (destroys current investigation)')

    def investigation(self):
        
        self.openInvestigation()

        while True:
            self.displayInvestMenu()

            cmd = input('> ')
            if cmd == '0':
                print('Add help')

            elif cmd == '1':
               self.hostInfo()

            elif cmd == '2':
                self.printReport()

            elif cmd == '3':
                lookup = Lookup(self.host)
                self.host = lookup.doLookup(self.host)
                if self.host.ip and self.host.domainName:
                    self.hostInfo()

            elif cmd == '4':
                print('What type of scan do you want to do? (e.g. F (default), sS, sV, A)')
                sType = input('> ')
                scan = PortScan(self.host.ip, sType)
                self.host.ports = scan.runScan(self.host.ip, sType)

            elif cmd == '5':
                whoisLookup = ""
                if not self.host.domainName:
                    whoisLookup = Whois(ip=self.host.ip)
                else:
                    whoisLookup = Whois(hostName=self.host.domainName)
                self.host.whoisInfo = whoisLookup.getInfo(self.host.domainName)

            elif cmd == '96':
                self.exportReport()

            elif cmd == '97':
                self.changeIP()

            elif cmd == '98':
                self.changeDomain()

            elif cmd == '99':
                print('[!] Quitting!')
                break

            else:
                print('Please enter a valid option!')
            
    

class Host:
    def __init__(self, ip="", domainName=""):
        self.ip = ip
        self.domainName = domainName
        self.ports = []
        self.whoisInfo = {}

    

    