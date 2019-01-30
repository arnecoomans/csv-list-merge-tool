#!/usr/bin/python
# import high-level functions
import os
import sys
from pprint import pprint

class merge:
    def __init__(self, core):
        self.core = core
        self.headers = []
        self.newline = {}
        self.contents = {}
        
        # First, merge headers
        self.mergeHeaders()
        
        # Then, merge line by line by file
        for file in self.core.filecontents:
            for line in self.core.filecontents[file].contents:
                self.mergeLine(line, self.core.filecontents[file].contents[line], file)
            #pprint(self.core.filecontents[file].contents)
        
    def mergeHeaders(self):
        # If headers can be merged from all files
        if self.core.arguments['column'] == None:
            self.headers.append(self.core.arguments['mergecolumn'].lower())
            for file in self.core.files:
                for header in self.core.filecontents[file].header:
                    if header not in self.headers:
                        self.headers.append(header)
        # If headers are defined
        else:
            for header in self.core.arguments['column']:
                self.headers.append(header.lower())
        # Add inFiles if active
        if self.core.arguments['includeorigin'].lower() == 'yes':
                for file in self.core.files:
                    self.headers.append('in' + file.replace('/','-').replace('.','_').lower())
        for item in self.headers:
            self.newline[item] = None
        self.core.log('Merging headers into: ' + ', '.join(self.headers))
        #print self.core.arguments
    
    def mergeLine(self, id, line, file):
        # Check if ID is already known in results.
        # If not, it should be added as an empty line
        if id not in self.contents:
            self.contents[id] = {}
            for header in self.headers:
                self.contents[id][header] = None
        # Now it is safe to assume the line exists in the result
        for key in line:
            if key in self.headers:
                if self.core.arguments['overwrite'] == True:
                    self.contents[id][key] = line[key]
                else:
                    if self.contents[id][key] == None:
                        self.contents[id][key] = line[key]
        if self.core.arguments['includeorigin'].lower() == 'yes':
            self.contents[id]['in' + file.replace('/','-').replace('.','_').lower()] = 'yes'
    
    def putOut(self):
        # Return header
        if self.core.arguments['output'] is None:
            print self.core.arguments['seperator'].join(self.headers)
        else:
            f = open(self.core.arguments['output'], 'w')
            f.write(self.core.arguments['seperator'].join(self.headers) + "\n")
            self.core.log('Writing outout to [' + self.core.arguments['output'].lower() + ']')      
        for line in self.contents:
            result = []
            for key in self.headers:
                if self.contents[line][key] == None:
                    result.append('')
                else:
                    result.append(str(self.contents[line][key]))
            if self.core.arguments['output'] is None:
                print self.core.arguments['seperator'].join(result)
            else:
                f.write(self.core.arguments['seperator'].join(result) + "\n")
        if self.core.arguments['output'] is not None:
            f.close()