"""
=============================================================================
File: tcx_file_splitter.py
Description: Splits TCX file into smaller files to upload to Garmin Connect, which
             accepts max 25MB files.
Author: Praful https://github.com/Praful/tcx_file_splitter
Licence: GPL v3

Notes:

=============================================================================
"""

from pydoc import resolve
import argparse
from pathlib import Path
import lxml.etree as ET2


class TcxFileSplitter:
    """
    Represents the data on a listing of episodes and the episode itself for a castaway.
    """

    def __init__(self, tcxfile, output, activities_count):
        self.tcxfile = tcxfile
        self.output_folder = output
        self.activities_per_file = activities_count

        if '..' in self.output_folder:
            self.output_path = (Path(__file__).parent /
                                self.output_folder).resolve()
        else:
            self.output_path = self.output_folder

    def __str__(self):
        return f'Name: {self.tcxfile}, Output: {self.output_path}, Activities per file: {self.activities_per_file}'

    def process(self):

        file_suffix = 0

        def save_split_file(output, author):
            nonlocal file_suffix
            file_suffix += 1
            output.append(author)
            tree = ET2.ElementTree(output)
            tree.write(f'{self.output_path}\split_{file_suffix}.tcx',
                       encoding="UTF-8", xml_declaration=True)

        # see https://stackoverflow.com/questions/46405690/how-to-include-the-namespaces-into-a-xml-file-using-lxml/46422793#46422793
        attr_qname = ET2.QName(
            "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        # ns_output={None: self.ns, "xsi": "http://www.w3.org/2001/XMLSchema-instance"}

        schema = 'http://www.garmin.com/xmlschemas/ActivityExtension/v2 http://www.garmin.com/xmlschemas/ActivityExtensionv2.xsd http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd'

        tree = ET2.parse(self.tcxfile)
        root = tree.getroot()
        ns_input = {'training_centre': root.nsmap[None]}
        ns_output = root.nsmap

        author = root.find('.//training_centre:Author', ns_input)

        output = None
        write_count = 0

        for activity in root.findall('.//training_centre:Activity', ns_input):
            if output is None:
                output = ET2.Element('TrainingCenterDatabase', {
                    attr_qname: schema}, nsmap=ns_output)
                activities = ET2.Element('Activities', nsmap=ns_output)
                output.append(activities)

            activities.append(activity)
            write_count += 1

            if write_count % self.activities_per_file == 0:
                save_split_file(output, author)
                output = None

        if output is not None:
            save_split_file(output, author)

# For help, see https://docs.python.org/3/library/argparse.html


def setup_command_line():
    """
    Define command line switches
    """
    # cmdline = argparse.ArgumentParser(prog='tcx_file_splitter.py')
    cmdline = argparse.ArgumentParser(description='Garmin TCX file splitter')
    cmdline.add_argument('--input', required=True,
                         type=str, help=f'TCX filename')
    cmdline.add_argument('--activities_per_file', type=int,
                         help=f'Activities for each split file. Affects size. Number should be set to ensure file size is less than 25MB, which is the max accepted by Garmin Connect', default=25)
    cmdline.add_argument('--output_folder', type=str,
                         help=f'Output folder for split TCX files', default='../output')
    # cmdline.add_argument('--ns', type = str, help = f'Namespace of TCX file', default = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
    return cmdline


def main():
    """
    Processing begins here if script run directly
    """
    args = setup_command_line().parse_args()

    splitter = TcxFileSplitter(
        args.input, args.output_folder, args.activities_per_file)
    splitter.process()


#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    main()
