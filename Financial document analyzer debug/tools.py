## Importing libraries and files
from crewai_tools import FileReadTool

# Creating a single, reusable instance of the FileReadTool.
# This tool can read any file and is perfect for our PDF analysis needs.
file_read_tool = FileReadTool()