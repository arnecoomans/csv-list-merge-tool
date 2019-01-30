#!/usr/bin/python
# import high-level functions
import os
import sys
from pprint import pprint

class read:
    def __init__(self, core, filename):
        self.supportedseperators = ['";"', '\';\'', 
                                    '","', '\',\'', 
                                    '"|"', '\'|\'',
                                    "\"\t\"", "'\t'",
                                    ';',
                                    ',',
                                    '|',
                                    "\t",
                                    ]
        
        self.filename = filename
        self.core = core
        self.header = []
        self.headerLine = 0
        self.contents = {}
        
        # Open file
        self.f = open(filename, 'r')
        # Read line by line
        linenum = 0
        self.header = self.readHeader()
        
        self.contents = self.readContents()
            
    def readHeader(self):
        result = []
        # Detect Header
        # Header should be the first non-empty line not starting with a #
        #
        # Store linenumbers - they can be skipped later
        self.headerLine = 0
        for line in self.f:
            # Increase linenumber
            self.headerLine  += 1
            # Remove spacing around line
            line = line.strip()
            # If line is not empty and it doesn't start with a #-comment
            if self.lineNotEmpty(line) and self.lineNotComment(line):
                # This line is the header
                # Detect Seperator character
                self.seperator = self.detectSeperator(line)
                # Split header line with seperator. Can be stored as header
                keys = 0
                for item in line.split(self.seperator):
                    keys = keys + 1
                    # If column header is not empty,
                    # Store the srtipped version
                    if self.lineNotEmpty(item):
                        if self.seperator is not None:
                            if self.seperator[0] is '"' or self.seperator[0] is '\'':
                                if item[0] == '"' or item[0] == '\'':
                                    item = item[1:]
                                if item[-1:] is '"' or item[-1] is '\'':
                                    item = item[:-1]
                        result.append(item.strip().lower())
                    # If column header is empty, 
                    # Name the column
                    else:
                        result.append('column' + str(keys))
                # Verify that merge-column is in header
                self.core.log(self.filename + ': Headers detected on line ' + str(self.headerLine) + ': ' + ', '.join(result))
                # Since we've found the header, we can now stop going through the file
                break
        # Verify that the required merge header is in the headers,
        # if not; exit the program - this file cannot be merged
        self.core.arguments['mergecolumn'] = self.core.arguments['mergecolumn'].lower()
        if self.core.arguments['mergecolumn'] not in result:
            print ''
            print '  Fatal error! Column required for merging not found in header of ' + self.filename + '.'
            print '  Did not find ' + self.core.arguments['mergecolumn'] + ' in ' + line + '.'
            print ''
            print '  Please verify file and try again.'
            print ''
            print '  Exiting...'
            exit()
        # Else: return the result
        return result


    # Check if a seperator can be detected in the header
    def detectSeperator(self, line):
        for seperator in self.supportedseperators:
            if seperator in line:
                self.core.log(self.filename + ': Seperator ' + seperator + ' detected in header')
                return seperator
            
            
    def readContents(self):
        # Store linenumber
        # Is used for skipping the header
        linenumber = 0
        # Prepare result
        # Contains a dict with all content
        result = {}
        # Loop through all file lines
        # This function continues where the readHeader stopped
        for row in self.f:
            line = {}
            row = row.strip()
            if self.lineNotEmpty(row) and self.lineNotComment(row):
                #line = line.split(self.seperator)
                index = 0
                for column in row.split(self.seperator):
                    if index < len(self.header) and len(column.strip()) >= 1:
                        if self.seperator[0] is '"' or self.seperator[0] is '\'':
                            if column[0] == '"' or column[0] == '\'':
                                column = column[1:]
                            if column[-1:] is '"' or column[-1] is '\'':
                                column = column[:-1]
                        line[self.header[index]] = column
                    index += 1
                # Since a row has been read into a line,
                # add it to the result
                # using mergecolumn as index
                # mergecolumn in lowercase for easier matching
                if self.core.arguments['mergecolumn'] in line:
                    result[line[self.core.arguments['mergecolumn']].lower()] = line
        return result
    
    # Return True if inputted Line is not empty
    def lineNotEmpty(self, line):
        line = line.strip()
        if len(line) > 0:
            return True
        else:
            return False

    # Return True if the first non whitespace character of this line
    # is not # of ; - indicating a comment
    def lineNotComment(self, line):
        line = line.strip()
        if line[0] is '#' or line[0] is ';':
            return False
        else:
            return True