# tcx_file_splitter readme

Garmin Connect will let you import TCX files. You can export all data from Garmin Training Center on Windows. However, if the exported TCX file is larger than 25MB, it can't be imported into Garmin Connect.

This program splits a large TCX file exported from Garmin Training Center into smaller files. 


## Installation

The program was tested with Python 3.10 on Windows 10. However, there is nothing intentionally specific to Windows in the program.

You will need to [install Python](https://www.python.org/downloads) for your computer. After that, install the following library using `pip`:

```
pip install lxml
```

## Running the program

The help is shown below:

```
> python .\tcx_file_splitter.py --help
usage: tcx_file_splitter.py [-h] --input INPUT [--activities_per_file ACTIVITIES_PER_FILE]
                            [--output_folder OUTPUT_FOLDER]

Garmin TCX file splitter

options:
  -h, --help            show this help message and exit
  --input INPUT         TCX filename
  --activities_per_file ACTIVITIES_PER_FILE
                        Activities for each split file. Affects size. Number should be set to ensure file size
                        is less than 25MB, which is the max accepted by Garmin Connect
  --output_folder OUTPUT_FOLDER
                        Output folder for split TCX files
```

For example, to split a TCX file called `myruns.tcx` in smaller files with 10 activities in each file, type the following at the command prompt (shell) from the `src` folder:

```
> python .\tcx_file_splitter.py --input 'c:\documents\myruns.tcx' --activities_per_file=10
```

This will output files in the `output` folder, named `split_1.tcx`, `split_2,tcx`, `split_3.tcx`, etc. If a file exists with the same name as a newly created split file, eg if `split_3.tcx` exists, that file will be *overwritten without warning*. Therefore, if you have any files in the output folder that you want to keep, move them to another folder.

Before attempting to upload the files to Garmin Connect, check that all the split files are less than 25MB. If any is bigger than 25MB, re-run the program and specify a smaller `activities_per_file` value. Remember to delete the previously created split files.

## Sample input and output

The `data` folder contains a small sample input file with three activities that was exported from Garmin Training Center. The `output` folder contains the output of processing the sample file when the `activities_per_file` to `1`. Three split files were created.
## Disclaimer

I wrote this program to solve my problem. I don't know if it will do what you want it to do. Therefore, this program is provided "as-is". Use at your own risk! 