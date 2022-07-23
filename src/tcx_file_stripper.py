"""
=============================================================================
File: tcx_file_stripper.py
Description: Splits TCX file into smaller files to upload to Garmin Connect, which
             accepts max 25MB files.
Author: Praful https://github.com/Praful/tcx_file_stripper
Licence: GPL v3

Notes:

=============================================================================
"""

# from posixpath import split
from pydoc import resolve
import string
import re
import sys
import traceback
import collections
import argparse
import contextlib
import io
import time

from pathlib import Path

# import xml.etree.ElementTree as ET
import lxml.etree as ET2
import copy


def print_error(msg, error):
    print(f'{msg}: {str(error)}')
    traceback.print_exc(file=sys.stdout)


class TcxFileSplitter:
    """
    Represents the data on a listing of episodes and the episode itself for a castaway.
    """

    def __init__(self, tcxfile, namespace, output, activities_count):
        self.tcxfile = tcxfile
        self.ns = namespace
        self.output_folder = output
        self.activities_per_file = activities_count

    def __str__(self):
        return f'Name: {self.tcxfile}, Namespace: {self.ns}'

    def process(self):
        # print('process2 using lxml')
        ns_input = {'training_centre': self.ns}
        # see https://stackoverflow.com/questions/46405690/how-to-include-the-namespaces-into-a-xml-file-using-lxml/46422793#46422793
        attr_qname = ET2.QName(
            "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        ns_output = {None: self.ns,
                     "xsi": "http://www.w3.org/2001/XMLSchema-instance"}

        schema = 'http://www.garmin.com/xmlschemas/ActivityExtension/v2 http://www.garmin.com/xmlschemas/ActivityExtensionv2.xsd http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd'

        tree = ET2.parse(self.tcxfile)
        root = tree.getroot()
        author = root.find('.//training_centre:Author', ns_input)

        activity1 = "test"
        output = None

        write_count = 0
        file_suffix = 0
        if '..' in self.output_folder:
            output_path = (Path(__file__).parent /
                           self.output_folder).resolve()
        else:
            output_path = self.output_folder

        for activity in root.findall('.//training_centre:Activity', ns_input):
            # print(activity.tag)
            # activity1 = activity
            if output is None:
                output = ET2.Element('TrainingCenterDatabase', {
                    attr_qname: schema}, nsmap=ns_output)
                activities = ET2.Element('Activities', nsmap=ns_output)
                output.append(activities)

            activities.append(activity)
            write_count += 1

            if write_count >= self.activities_per_file:
                file_suffix += 1
                output.append(author)
                f = open(f'{output_path}\output_{write_count}.tcx', 'x')
                try:
                    f.write(ET2.tounicode(output))
                finally:
                    f.close()

                output = None


def setup_command_line():
    """
    Define command line switches
    """
    cmdline = argparse.ArgumentParser(prog='Garmin TCX file splitter')
    cmdline.add_argument('--input', type=str, help=f'TCX filename')
    cmdline.add_argument('--activities_per_file', type=int,
                         help=f'Activities for each split file. Affects size. Number should be set to ensure file size is less than 25MB (max accepted by Garmin Connect', default=5)
    cmdline.add_argument('--output_folder', type=str,
                         help=f'Output folder for split TCX files', default='..\output')
    cmdline.add_argument('--ns', type=str, help=f'Namespace of TCX file',
                         default='http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
    return cmdline


def main():
    """
    Processing begins here if script run directly
    """
    args = setup_command_line().parse_args()

    splitter = TcxFileSplitter(
        args.input, args.ns, args.output_folder, args.activities_per_file)
    splitter.process()

    # print('Creating output:')
    # outputter = CastawayOutputter()
    # outputter.as_csv(parser.castaways, args.output)


#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    main()
