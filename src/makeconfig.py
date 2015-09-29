#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Chris Earley <cw.earley@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# application specific import
from configuration import SystemConf


def main():
   
   config, description = SystemConf.build_config()

   print ('This wizard will walk you through generating a topic2twitter configuration file.\nJust enter the desired option value when prompted.')
   
   for section in config.sections():
      # https://wiki.python.org/moin/IfStatementWithValue#Accepted_Solution
      section_description = description[section] if section in description else None
      # since descriptions may not exist for all config sections, check.
      if section_description != None:
         print (section_description)
      for option in config.options(section):
         
         option_description = description[option] if option in description else ''
         
         default = config.get(section, option)
            
         value = raw_input('{0} - {1}(default: {2}): '.format(option, option_description, default))
         # only change the value if the user supplies something new
         # otherwise you'll overwrite any defaults
         if value != '':
            config.set(section, option, str(value))
               
   print('Config Settings - The last step.')
         
   confname = raw_input('Config file name (default: topic2twitter.conf): ')
   
   if confname == '':
      confname = 'topic2twitter.conf'
      
   # Writing our configuration file to 'example.cfg'
   with open(confname, 'wb') as configfile:
      config.write(configfile)
      
   print ('Done!\nNow launch the daemon with (####################)')
   
   return 0

if __name__ == '__main__':
	main()
