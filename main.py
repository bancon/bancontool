'''
Program name: Bancon Server Protection Tool
Authors: Indy and Monkey
Date Started: 2013-04-15
Description: Tool used to Administrate Call of Duty 1 Servers
'''
version = 'Beta 1.1B'
 
#import the models needed
import sys
import socket
import datetime
import time
import re
import thread
import threading
import string
import linecache
import ConfigParser
from threading import Thread
from itertools import izip
from ctypes import windll

#############################  
#### Color Code Function ####
#############################
def get_color(string):
    if string == '1':
        return 12
    if string == '2':
        return 10
    if string == '3':
        return 14
    if string == '4':
        return 9
    if string == '5':
        return 11
    if string == '6':
        return 13
    if string == '7':
        return 7
    return 7
def remove_double_color(string):
    color_count = { }
    if string[-1] == '^':
        string = string[:-1]
    for i in range(1, 8):
        s = ''.join((str(i),str(i)))
        color_count[i] = ''.join(('^^',s))
    x = 1
    for i in range(len(string)):
        replacer = ''.join(('^', str(x)))
        string = string.replace(color_count[x], replacer)
        x+=1
        if x == 8:
            break
    return string
def print_color(string):
    x = 0
    color_num = { }
    if string[-1] == '^':
        string = string[:-1]
    for i in range(len(string)):
        if string[x] == '^':
            windll.kernel32.SetConsoleTextAttribute(stdout_handle, int(get_color(string[x+1])))
            string = string.replace(string[x+1], ' ', 1)
        else:
            print string[x].strip(),; sys.stdout.softspace=False
        x += 1
def set_color(string):
    x = 0
    color_num = { }
    a = []
    if string[-1] == '^':
        string = string[:-1]
    for i in range(len(string)):
        if string[x] == '^' and string[x+1] != '^':
            windll.kernel32.SetConsoleTextAttribute(stdout_handle, int(get_color(string[x+1])))
            string = string.replace(string[x+1], ' ', 1)
        else:
            a.append(string[x])
        x += 1
    s = ''.join(a)
    s = s.replace(" ", " ")
    return s

STD_OUTPUT_HANDLE = -11

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
65.
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

#############################  
####  Startup Functions  ####
#############################
def error(error_msg):
  if error_msg:
    print("\nERROR: %s" % error_msg)
    time.sleep(5)
    sys.exit(1)
  else:
    print("\nERROR: Unexpected error.")
    print("Closing in five seconds...")
    time.sleep(5)
    sys.exit(1)
   
def checkVar(varName, varDesc):
  if not varName and varName != 0:
    error("%s is not set." % varDesc)
   
def checkServer(srv):
  for i in range(3):
    welcome = '^1[^7BanCon^1] ^6Tool ^7User:%s ^1Connected' % USERNAME
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.connect((HOST[srv], PORT[srv]))
        sock.send("\xFF\xFF\xFF\xFFrcon %s say %s" % (PWD[srv],welcome))
    except:
        error("Check your ip and port!!")
        break
    try:
      callback = sock.recv(1024)
      break
    except socket.error:
      if i == 2:
        error("Could not connect to server%s. Check your ports and ip!" % srv)
    else:
      if callback[10:27] == "Bad rconpassword.":
        error("Server%s's rcon password is incorrect." % srv)
      elif not callback:
        error(None)
      else:
          error("Unidentified error: make sure ip is correct")
    sock.close()
 
def setup_settings():
    default_username = '^1Admin'
    default_banmsg  = '^7was ^5banned ^7from the server ^7for '
    default_kickmsg = 'has been ^1KICKED from the server for:'
    default_warnmsg = '^7has been ^1WARNED ^7For:'
    config.add_section('Settings')
    config.set('Settings', 'Username', default_username)
    config.set('Settings', 'BanMessage', default_banmsg)
    config.set('Settings', 'KickMessage', default_kickmsg)
    config.set('Settings', 'WarnMessage', default_warnmsg)
    with open('settings.cfg', 'wb') as configfile:
        config.write(configfile)
 
def file_is_empty(filename):
  num_line = sum(1 for line in open(filename))
  if num_line == 0:
    return True
  else:
    return False

#####################
### Startup tasks ###
#####################
s = set_color('^3')
print s
print 'Welcome to BanCoN Server Protection Tool!'
print 'Created by: Indy and Monkey!'
print 'BanCon Version: %s' % version
HOST = { }
PORT = { }
PWD  = { }
config = ConfigParser.RawConfigParser()
 
#Writes default setting file and default servers file
if file_is_empty('servers.txt'):
  s1 = set_color ('\n^2Starting first time setup...')
  print s1.replace(' ', '', 1)
  time.sleep(2)
  SERVERNUM = int(input("Enter the number of servers to monitor: "))
  for i in range(1, SERVERNUM + 1):
    HOST[i] = raw_input('Ip of server(%s)? ' % i)
    PORT[i] = int(input('Port of server(%s)? '% i))
    PWD[i] = raw_input('Rcon password of server(%s)? ' % i)
    f = open('servers.txt', 'a')
    f.write('%s,%s,%s\n' % (HOST[i], PORT[i], PWD[i]))
    f.close()
if file_is_empty('settings.cfg'):
  setup_settings()
if file_is_empty('servers.txt') == False:
  print 'Checking servers. Please wait...'
  f = open('servers.txt', 'r')
  SERVERNUM = sum(1 for line in open('servers.txt'))
  x = 1
  for i in iter(f):
    data = i.strip().split(',')
    HOST[x] = data[0]
    PORT[x] = int(data[1])
    PWD[x] = data[2]
    x += 1
if file_is_empty('settings.cfg') == False:
    global USERNAME
    global BANMSG
    global KICKMSG
    global WARNMSG
    config.read('settings.cfg')
    USERNAME = config.get('Settings', 'Username')
    BANMSG   = config.get('Settings', 'BanMessage')
    KICKMSG  = config.get('Settings', 'KickMessage')
    WARNMSG  = config.get('Settings', 'WarnMessage')
   
for i in range(1, SERVERNUM + 1):
  checkVar(HOST[i], "Hostname/IP")
  checkVar(PORT[i], "Port")
  checkVar(PWD[i], "Rcon password")
  checkServer(i)
 
#Start of Player class used to classify each part of the packets received about players on the server
class Player:
      def __init__(self, name, frags, ping, num=None, address=None, bot=-1):
              self.name = name
              self.frags = frags
              self.ping = ping
              self.address = address
              self.id = num
              self.bot = bot
      def __str__(self):
              return self.name
      def __repr__(self):
              return str(self)
      def is_admin(self):
          return self.address
#Start of PyQuake3 class used to explode the packets so we can use the name , id, and ip for the ban tool
class PyQuake3:
      packet_prefix = '\xff' * 4
      player_reo = re.compile(r'^(\d+) (\d+) "(.*)"')
      def __init__(self, serverip, serverport, rcon_password=''):
              self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
              self.set_server(serverip, serverport)
              self.set_rcon_password(rcon_password)
      def set_server(self, serverip, serverport):
              try:
                      self.address = serverip
                      self.port = serverport
              except:
                      raise Exception('Server address must be in the format of \
                                  "address:port"')
              self.port = int(self.port)
              self.s.connect((self.address, self.port))
      def get_address(self):
              return '%s:%s' % (self.address, self.port)
      def set_rcon_password(self, rcon_password):
              self.rcon_password = rcon_password
      def send_packet(self, data):
              self.s.send('%s%s\n' % (self.packet_prefix, data))
      def recv(self, timeout=20):
              self.s.settimeout(timeout)
              try:
                      return self.s.recv(4096)
              except socket.error, e:
                      raise Exception('Error receiving the packet: %s' % \
                                      e[1])
      def command(self, cmd, timeout=20, retries=3):
              while retries:
                      self.send_packet(cmd)
                      try:
                              data = self.recv(timeout)
                      except:
                              data = None
                      if data:
                              return self.parse_packet(data)
                      retries -= 1
              raise Exception('Server response timed out')
      def rcon(self, cmd):
              r = self.command('rcon "%s" %s' % (self.rcon_password, cmd))
              if r[1] == 'No rconpassword set on the server.\n' or r[1] == \
                              'Bad rconpassword.\n':
                      raise Exception(r[1][:-1])
              return r
      def parse_packet(self, data):
              if data.find(self.packet_prefix)!= 0:
                      raise Exception('Malformed packet')
              first_line_length = data.find('\n')
              if first_line_length == -1:
                      raise Exception('Malformed packet')
              response_type = data[len(self.packet_prefix):first_line_length]
              response_data = data[first_line_length+1:]
              return response_type, response_data
      def parse_status(self, data):
              split = data[1:].split('\\')
              values = dict(zip(split[::2], split[1::2]))
              # if there are \n's in one of the values, it's the list of players
              for var, val in values.items():
                      pos = val.find('\n')
                      if pos == -1:
                              continue
                      split = val.split('\n', 1)
                      values[var] = split[0]
                      self.parse_players(split[1])
              return values
     
      def parse_players(self, data):
              self.players = []
              for player in data.split('\n'):
                      if not player:
                              continue
                      match = self.player_reo.match(player)
                      if not match:
                              print 'couldnt match', player
                              continue
                      frags, ping, name = match.groups()
                      self.players.append(Player(name, frags, ping))
 
      #Function to just displayer players on the server and their id              
      def update(self):
              cmd, data = self.command('getstatus')
              self.vars = self.parse_status(data)
             
      #Function to get the status of the server includes players ip etc
      def rcon_update(self):
                    cmd, data = self.rcon('status')
                    lines = data.split('\n')
                    players = lines[3:]
                    self.players = []
                    for p in players:
                            while p.find('  ') != -1:
                                    p = p.replace('  ', ' ')
                            while p.find(' ') == 0:
                                    p = p[1:]
                            if p == '':
                                    continue
                            p = p.split(' ')
                            self.players.append(Player(p[3], p[1], p[2], p[0], p[5]))

 
#Function that removes color codes of players on serveers
def filter_name(name):
  result = ""
  i = 0
  while i < len(name):
    if name[i] == "^":
      i += 2
    else:
      result += name[i]
      i += 1
  return result
 
#############################  
####    Misc Functions   ####
#############################
 
#Function that deletes lines from text files
def removeLine(filename, lineno):
  with open(filename, 'r') as file:
      data = file.readlines()
  # need - 1 for the array ( 1st line = 0 in array)
  data[lineno-1] = ''
  with open(filename, 'w') as file:
      file.writelines( data )
  file.close()
 
#Function that replaces a line with new info
def replaceLine(filename, lineno, info):
  with open(filename, 'r') as file:
      data = file.readlines()
  data[lineno-1] = info
  with open(filename, 'w') as file:
      file.writelines( data )
  file.close()
 
#Function that splits up strings
def split_string_from_file(filename, delimiter):
  f = open(filename)
  for data in iter(f):
    line = data.rstrip('\n')
    arr = re.split(delimiter, line.strip())
  return arr
 
def split_string(s, delimiter):
  tempS = re.split(delimiter, s)
  return tempS
 
#Function to get the current time
def get_timeString():
  now = datetime.datetime.now()
  return now.strftime("%H-%M %d-%m-%y")
 
#Function to Kick Client from Server
def kick_client(client, kickmessage, servernum):
  retrieved_line = linecache.getline('servers.txt', servernum)
  info =  re.split(',', retrieved_line.strip())
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.settimeout(1)
  sock.connect((info[0],int(info[1])))
  sock.send("\xFF\xFF\xFF\xFFrcon %s \x20clientkick\x20 %s" % (info[2], client.id))
  sock.send("\xFF\xFF\xFF\xFFrcon %s say %s %s" % (info[2], client.name, kickmessage))
  sock.close()
 
def sock_send(cmd, info, server):
  info = re.split(':', server.strip())
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.settimeout(1)
  sock.connect((info[0],info[1]))
  sock.send("\xFF\xFF\xFF\xFFrcon %s %s %s" % (info[2], cmd, info))
  sock.close()  
 
#Function used to check the bans file
def check_bans():
  svr = { }
  server = { }
  while(True):
    for i in range(1,SERVERNUM+1):
      svr[i] = PyQuake3(HOST[i], int(PORT[i]), PWD[i])
      svr[i].rcon_update()
      f = open('bans.txt', 'r')
      for x in iter(f):
        line = x.rstrip('\n')
        arr = re.split(',', line.strip())
        for x in svr[i].players:
          address_ip = re.split(':', x.address.strip())
          if arr[1] == address_ip[0]:
            print 'Kicking player'
            banmessage = '%s %s On: ^3%s By: %s' % (BANMSG, arr[2], get_timeString(), USERNAME)
            svr[i].rcon('clientkick %s' % x.id)
      f.close()
    time.sleep(0)
 
#Function used to add a ban to the bans.txt file  
def write_ban(client, reason):
  banfile = open('bans.txt', 'a')
  address = re.split(":", client.address.strip())
  try:
    banfile.write('%s,%s,%s\n' % (filter_name(client.name), address[0], reason))
  finally:
    banfile.close()
 
#Function to delete a ban in the bans.txt file  
def delete_ban(clientnum, lastline):
    for x in range(1, lastline+1):
      if x == clientnum:
        retrieved_line = linecache.getline('bans.txt', x)
        output =  split_string(retrieved_line, ',')
        removeLine('bans.txt', x)
        print('%s successfully unbanned!' % output[0])
        
def add_admin(client):
    adminfile = open('admins.txt', 'a')
    address = re.split(":", client.address.strip())
    try:
        adminfile.write('%s,%s\n' % (filter_name(client.name), address[0]))
    finally:
        adminfile.close()
def delete_admin(clientnum, lastline):
    for x in range(1, lastline+1):
      if x == clientnum:
        retrieved_line = linecache.getline('admins.txt', x)
        output =  split_string(retrieved_line, ',')
        removeLine('admins.txt', x)
        print('%s successfully unbanned!' % output[0])    
#############################  
#### Rcon Tool Functions ####
#############################
 
#Function to send a message to the server as console
def send_message(message, num):
  if num == 'srvs':
    lines = sum(1 for line in open('servers.txt'))
    for i in range(1,lines+1):
      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      sock.settimeout(1)
      sock.connect((HOST[i],int(PORT[i])))
      sock.send("\xFF\xFF\xFF\xFFrcon %s say %s" % (PWD[i], message))
      sock.close()
  else:
      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      sock.settimeout(1)
      sock.connect((HOST[num],int(PORT[num])))
      sock.send("\xFF\xFF\xFF\xFFrcon %s say %s" % (PWD[num], message))
      sock.close()
 
#Function to restart a map
def map_restart():
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.settimeout(1)
  sock.connect((HOST[GLOBAL_NUM],int(PORT[GLOBAL_NUM])))
  sock.send("\xFF\xFF\xFF\xFFrcon %s map_restart" % (PWD[GLOBAL_NUM]))
  sock.close()
 
def change_map(new_map, GLOBAL_NUM):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.settimeout(1)
  sock.connect((HOST[GLOBAL_NUM], int(PORT[GLOBAL_NUM])))
  sock.send("\xFF\xFF\xFF\xFFrcon %s map %s" % (PWD[GLOBAL_NUM], new_map))
  sock.close()
 
#############################
###### Rcon Tool Menus ######
#############################
   
def select_server():
  f = open('servers.txt')
  i = 1
  srv = { }
  s = set_color('^3')
  print s
  server_num = sum(1 for line in open('servers.txt'))
  print '\n\n0) Add Server'
  for line in iter(f):
    data = re.split(',', line.strip())
    srv[i] = PyQuake3(data[0], data[1], data[2])
    srv[i].update()
    print ('%s)' % (i)),;
    print_color('^7'),;
    print_color(srv[i].vars['sv_hostname']),;
    print_color('^3'),;
    s1 = set_color ('(^3%s:%s )' % (data[0], data[1]))
    print s1
    i += 1
  print '%s) Exit Program' % str(server_num + 1)
  f.close()
  server_input = int(input("\nSelect a server: "))
  for x in range(1, server_num + 1):
    if x == server_input and x != server_num + 1:
      return x
  if server_input == server_num + 1:
    print 'Disconnecting'
    gb = '^1[^7BanCon^1] ^7Tool User: %s ^3Disconnected' % USERNAME
    send_message(gb, 'srvs')
    sys.exit(1)    
  elif server_input == 0:
    server_num = sum(1 for line in open('servers.txt'))
    HOST[server_num+1] = raw_input("\nIp of server%s: " % (server_num+1))
    PORT[server_num+1] = int(input("Port of server%s: " % (server_num+1)))
    PWD[server_num+1]  = raw_input("Rcon of server%s: " % (server_num+1))
    if checkServer(server_num+1) == 0:
      print("Could not connect to server%s. Check your ports and ip!" % server_num+1)
      select_server()
    elif checkServer(server_num+1) == 1:
      print("Server%s's rcon password is incorrect." % server_num+1)
      select_server()
    else:
      f = open('servers.txt', 'a')
      f.write('%s,%s,%s\n' % (HOST[server_num+1], PORT[server_num+1], PWD[server_num+1]))
      f.close()
      print 'Server added. Please restart your ban tool to configure it.'
      time.sleep(3)
      sys.exit(1)
  else:                        
    print 'Server not listed!!'
  select_server()
  
def main_menu():
    serv[GLOBAL_NUM].update()
    print (" ")
    s1 = set_color ("^1Server selected: %s with currently %s player" % ( filter_name(serv[GLOBAL_NUM].vars['sv_hostname']),len(serv[GLOBAL_NUM].players)))
    print s1.strip()
    s1 = set_color ("^6What would you like to do?")
    print s1.strip()
    s1 = set_color ('^30: Go Back (Servers Menu)')
    print s1.strip()
    print ("1: Ban player")
    print ("2: Unban player")
    print ("3: Kick player")
    print ("4: Warn Player")
    print ("5: Talk as Console")
    print ("6: Restart Map")
    print ("7: Change map")
    print ("8: Bancon Information")
    print ("9: Settings")
    print ("10: Quit")
   
######################
#User Control Section#
######################
f = open('servers.txt')
i = 0
serv = { }
x = 1
for line in iter(f):
  data = line.strip().split(',')
  serv[x] = PyQuake3(data[0], data[1], data[2])
  serv[x].update()
  s1 = ('^4Loading server info for server(%s)...' % (i+1))
  time.sleep(2)
  print ('\nServer name:'),;
  print_color('^7'),;
  print_color(serv[x].vars['sv_hostname'])
  s1 = set_color ('\n^3Current map: %s' % (serv[x].vars['mapname']))
  print s1.replace(' ', '', 1)
  s1 = ('Current number of players: %s' %  len(serv[x].players))
  print s1.strip()
  i += 1
  x += 1
y = set_color ('^4Servers are being checked for hackers')
print y.strip()
t = Thread(target=check_bans, args=())
t.start()
GLOBAL_NUM = select_server()
while True:
    main_menu()
    choose = int(input(""))
    all_srv = PyQuake3(HOST[GLOBAL_NUM],int(PORT[GLOBAL_NUM]),PWD[GLOBAL_NUM])
    if choose == 0:
      GLOBAL_NUM = select_server()
    elif choose == 1:
      print ("You can change the Ban message in Settings!")
      all_srv.update()
      if all_srv.players == 0:
          print 'Server is empty.'
          continue
      all_srv.rcon_update()
      for player in all_srv.players:
              print '%s: ' % (player.id),;
              s = remove_double_color(player.name)
              print_color(s)
              print ("")
      print ("-1: Go Back (Main Menu)")
      client = raw_input("Player id? ")
      if client == -1:
        continue
      else:
        s = set_color('^1')
        print s
        reason = raw_input("Reason? ")
      kickmsg = 'has been banned for %s by %s' % (reason, USERNAME)
      for player in all_srv.players:
        if player.id == client:
          print('Player '),;
          s = remove_double_color(player.name)
          print_color(s),;
          print(' has been banned')
          write_ban(player, reason)
          kick_client(player,kickmsg,GLOBAL_NUM)
    elif choose == 2:
      i = 0
      f = open('bans.txt')
      print("")
      print ("0: Go Back (Main Menu)")
      for line in iter(f):
        i += 1
        data = line.strip().split(',')
        print("%s:%s (%s)" %(i, data[0], data[1]))
      clientnum = int(input("\nNumber? "))
      if clientnum > i:
        print 'Player not found!!!'
      elif clientnum == 0:
        continue
      else:
        delete_ban(clientnum, i)
      f.close()
    elif choose == 3:
          s = set_color('^4')
          print s
          print ("You can change the Kick message in Settings!")
          all_srv = PyQuake3(HOST[GLOBAL_NUM],int(PORT[GLOBAL_NUM]),PWD[GLOBAL_NUM])
          all_srv.update()
          if all_srv.players == 0:
              print 'Server is empty.'
              continue
          all_srv.rcon_update()
          for player in all_srv.players:
              print '%s: ' % (player.id),;
              s = remove_double_color(player.name)
              print_color(s)
              print ("")
          print ("-1: Go Back (Main Menu)")
          client = raw_input("Player id? ")
          if client == -1:
            continue
          else:
            reason = raw_input("Reason? ")
          kickmsg = '%s %s By: %s' %(KICKMSG, reason, USERNAME)
          all_srv.update()
          all_srv.rcon_update()  
          for player in all_srv.players:            
            if player.id == client:
              print('Player'),;
              s = remove_double_color(player.name)
              print_color(s),;
              print(' was kicked from the server!!')
              kick_client(player,kickmsg, GLOBAL_NUM)          
    elif choose == 4:
          print ("You can change the Warn Message message in Settings!")
          all_srv = PyQuake3(HOST[GLOBAL_NUM],int(PORT[GLOBAL_NUM]),PWD[GLOBAL_NUM])
          all_srv.update()
          if all_srv.players == 0:
              print 'Server is empty.'
              continue
          all_srv.rcon_update()
          for player in all_srv.players:
              print '%s: ' % (player.id),;
              s = remove_double_color(player.name)
              print_color(s)
              print ("")
          print ("-1: Go Back (Main Menu)")
          client = raw_input("Player id? ")
          if client == -1:
            continue
          else:
            all_srv.update()
            all_srv.rcon_update()
            for player in all_srv.players:
              if player.id == client:
                reason = raw_input("Reason? ")
                warning = '%s %s' % (WARNMSG, reason)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                sock.connect((HOST[GLOBAL_NUM],int(PORT[GLOBAL_NUM])))
                sock.send("\xFF\xFF\xFF\xFFrcon %s say %s %s %s By:%s" % (PWD[GLOBAL_NUM],player.name, warning, reason, USERNAME))
                sock.close()
                print('Player'),;
                s = remove_double_color(player.name)
                print_color(s),;
                print(' has been warned')
    elif choose == 5:
          s = set_color('^1')
          print s
          message = raw_input("What would you like to say? (Type back to go back)")
          if message == 'back':
                continue
          else:
                  send_message(message, GLOBAL_NUM)
                  print("Message sent\n")
    elif choose == 6:
        s = set_color('^2')
        print s
        sure = raw_input("Are you sure you want to continue? [YES/NO]: ")
        if sure == 'YES' or sure == 'Yes' or sure == 'yes':
            map_restart()
            print("The map has been restarted!\n")
        print("Heading back in 3 seconds!")
        time.sleep(3)
        continue
    elif choose == 7:
          all_srv = PyQuake3(HOST[GLOBAL_NUM],int(PORT[GLOBAL_NUM]),PWD[GLOBAL_NUM])
          all_srv.update()
          s = set_color('^3')
          print s
          print 'Current Map: %s' % all_srv.vars['mapname']
          new_map = raw_input("What map would you like to change it to? (None to go back) ")
          if new_map == 'none' or new_map == 'None':
            continue
          else:
            print("The map has been changed\n")
            change_map(new_map, GLOBAL_NUM)
    elif choose == 8:
          s = set_color('^5')
          print s
          print ("Current Version: 1.0 Beta")
          print ("New Features: Colors, Permanent Ban Control, Map Restart, Kick, Messages and Settings")
          print ("Additions: No python needed compiled with py2")
          print ("Authors: Indy and Monkey")
          print ("Xfires: indianbullet and estampon")
          print ("Future plans: Gui (Graphical User Interface), More Commands, Temporary Ban")
          leave = int(input("Type 1 When you are done: "))
          if leave == 1:
            continue
    elif choose == 9:          
          s = set_color('^6')
          print s          
          print ("1: Change Username")
          print ("2: Change Banning Message")
          print ("3: Change Kicking Message")
          print ("4: Change Warning Message")
          print ("5: Go back")
          schoice = int(input("What would you like to do? "))
          config = ConfigParser.RawConfigParser()
          config.read('settings.cfg')
          s = set_color('^2')
          print s
          if schoice == 1:
            USERNAME = raw_input("Username you would like to use: ")
            config.set('Settings', 'Username', USERNAME)
          elif schoice == 2:
            BANMSG = raw_input("Ban message you would like to use: ")
            config.set('Settings', 'BanMessage', BANMSG)
          elif schoice == 3:
            KICKMSG = raw_input("Kick message you would like to use: ")
            config.set('Settings', 'KickMessage', KICKMSG)
          elif schoice == 4:
            WARNMSG = raw_input("Warn message you would like to use: ")
            config.set('Settings', 'WarnMessage', WARNMSG)
          if schoice == 5:
            continue
          else:
              with open('settings.cfg', 'wb') as configfile:
                config.write(configfile)  
    elif choose == 10:
            print 'Disconnected'
            gb = '^1[^7BanCon^1] ^7Tool User: %s ^3Disconnected' % USERNAME
            send_message(gb, GLOBAL_NUM)
            sys.exit(1)
