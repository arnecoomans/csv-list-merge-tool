#!/usr/bin/python
# import high-level functions
import os
import sys
import argparse
from pprint import pprint




class go:
    def __init__(self):
        self.supportedExtentions = ['.txt', '.csv', '.list']
        self.logs = []
        self.filecontents = {}
        self.output = []
        
        self.arguments = self.parse_runtime_arguments()
        self.files = self.verify_files()
        
        
        #pprint(self.arguments)
                    
    def log(self, line):
        self.logs.append(line)
        if self.arguments['debug'] == True:
            print '  ' + str(line)
        
    def parse_runtime_arguments(self):
        parser = argparse.ArgumentParser(description='List Merge Tool by Arne Coomans', epilog='Any questions left? Contact arne@true.nl!')
        
        parser.add_argument('--version', action='version', version='%(prog)s Lists Merge Tool by Arne Coomans (0.2) (6 dec 2017)')
        
        parser.add_argument('files', nargs="*", default=None, help='the files that are to be merged')
        
        parser.add_argument('--output', nargs="?", default=None, help='optional. Defaults to screen. Use to specify a file for the output')
        parser.add_argument('--seperator', nargs="?", default=';', help='optional')
        parser.add_argument('--header', nargs="?", choices=['yes', 'no'], default='yes', help='optional. "yes" assumed')
        #parser.add_argument('--meta', nargs="?", choices=['yes', 'no'], default='yes', help='optional. "yes" assumed')
        parser.add_argument('--mergecolumn', nargs="?", default='email', help='optional. "email" assumed')
        parser.add_argument('--column', nargs='*', default=None, help='optional')
        parser.add_argument('--includeorigin', nargs='?', choices=['yes', 'no'], default='yes', help='optional. "yes" assumed')
        parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
        parser.add_argument('--overwrite', action='store_true', help='If set, overlapping values in later files are used. If not set, overlapping values from files are preserved in order of importing')
        #help=argparse.SUPPRESS
        # Actual Parsing is quite unimpressive
        return vars(parser.parse_args())
    
    def verify_files(self):
        # Check if files are supplied to App
        files = []
        if self.arguments['files'] == []:
            # No files were supplied
            # Assumed behavior: merge all .txt and .csv-files in current working directory
            self.log('No mergable files supplied. Assuming all .txt and .csv files in ' + os.getcwd())
            for file in os.listdir(os.getcwd()):
                if os.path.splitext(file)[1] in self.supportedExtentions:
                #if file[-4:] == '.txt' or file[-4:] == '.csv' or file[-5:] == '.list':
                    if file not in files:
                        files.append(file)
        else:
            # Files were supplied. Each files entry could be a file or a directory so it needs to be checked.
            for file in self.arguments['files']:
                if os.path.isfile(file):
                    # Absolute or relative file given:
                    # Add file to list if it doesn't already exist
                    if file not in files:
                        files.append(file)
                    #self.log("absolute or relative file: " + file)
                elif os.path.isdir(file):
                    # Absolute or relative directiry given
                    #self.log('absolute or relative dir: ' + str(file))
                    # Add trailing slash if it is not present
                    if file[-1:] is not '/':
                        file = file + '/'
                    # Check directory for files.
                    for dirfile in os.listdir(file):
                        # Only allow files that are supported, by extention
                        if os.path.splitext(dirfile)[1] in self.supportedExtentions:
                            if file + dirfile not in files:
                                files.append(file + dirfile)
        self.log('collected ' + str(len(files)) + ' files')
        if len(files) <= 1:
            print 'Oops! I\'ve found an issue.'
            print 'I do not have enough supported files to merge.'
            print '(' + str(len(files)) + ' supported file types found, minimum of 2 required)'
            print ''
            print 'Tip: specify each file in the command or specify the shared directory'
            print ''
            print 'quitting...'
            exit()
        self.log(str(self.arguments['files']) + ' results in ' + str(files))
        return files
    
