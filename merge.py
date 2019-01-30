#!/usr/bin/python
#
# ##############################################################
# List Merge Tool
# Combining several lists (csv) into a big one
# Arne Coomans / arne@true.nl
# ##############################################################
#
# Import high-level functions
import os
import sys
# Add /app/ as import directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/app/")
# Import app/ files
import app
import filereader
import filemerger


#
#
# ##############################################################
# App execution
# Only execute this if the script is accessed directly
# ##############################################################
if __name__ == "__main__":
    # Initialize core
    # Core is responsible for gathering the info required to run
    core = app.go()
    # At this moment it is safe to assume there are 2 or more files 
    # that need to be merged.
    
    # Read the files and store them in memory
    for file in core.files:
        core.filecontents[file] = filereader.read(core, file)

    # Merge the read content
    core.output = filemerger.merge(core)

    # Process output
    core.output.putOut()
    