#!/usr/bin/env python

'''
This script will load IGV in a virtual X window, load all supplied input files
as tracks, and take snapshots at the coorindates listed in the BED formatted
region file.
If you don't have a copy of IGV, get it here:
http://data.broadinstitute.org/igv/projects/downloads/IGV_2.3.81.zip
example IGV batch script:
new
snapshotDirectory IGV_Snapshots
load test_alignments.bam
genome hg19
maxPanelHeight 500
goto chr1:713167-714758
snapshot chr1_713167_714758_h500.png
goto chr1:713500-714900
snapshot chr1_713500_714900_h500.png
exit
'''

# ~~~~ LOAD PACKAGES ~~~~~~ #
import sys
import os
import errno
import subprocess as sp
import argparse

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
default_igv_jar = os.path.join(THIS_DIR, 'igv.jar')
default_output_dir = os.path.join(THIS_DIR, "IGV_Snapshots")
default_regions_bed = os.path.join(THIS_DIR, 'regions.bed')
# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
def file_exists(myfile, kill = False):
    '''
    Checks to make sure a file exists, optionally kills the script
    '''
    import os
    import sys
    if not os.path.isfile(myfile):
        print("ERROR: File '{}' does not exist!".format(myfile))
        if kill == True:
            print("Exiting...")
            sys.exit()

def subprocess_cmd(command):
    '''
    Runs a terminal command with stdout piping enabled
    '''
    import subprocess as sp
    process = sp.Popen(command,stdout=sp.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)








def get_open_X_server():
    '''
    Search for an open Xvfb port to render into
    '''
    x_serv_command= '''
for serv_num in $(seq 1 1000); do
    if ! (xdpyinfo -display :${serv_num})&>/dev/null; then
        echo "$serv_num" && break
    fi
done
'''
    import subprocess as sp
    # run the command, capture the output
    process = sp.Popen(x_serv_command,stdout=sp.PIPE, shell=True)
    x_serv_port = int(process.communicate()[0].strip())
    return(x_serv_port)




def run_IGV_script(igv_script, igv_jar, memMB):
    '''
    Run an IGV batch script
    '''
    import datetime
    # get the X11 Xvfb port number
    x_serv_port = get_open_X_server()
    print('\nOpen Xvfb port found on:\n{}\n'.format(x_serv_port))
    # build the system command to run IGV
    # igv_command = "(Xvfb :{} &) && DISPLAY=:{} java -Xmx{}m -jar {} -b {} && killall Xvfb".format(x_serv_port, x_serv_port, memMB, igv_jar, igv_script)
    igv_command = "xvfb-run --auto-servernum --server-num=1 java -Xmx{}m -jar {} -b {}".format(memMB, igv_jar, igv_script)
    print('\nIGV command is:\n{}\n'.format(igv_command))
    # get current time; command can take a while to finish
    startTime = datetime.datetime.now()
    print("\nCurrent time is:\n{}\n".format(startTime))
    # run the IGV command
    print("\nRunning the IGV command...")
    subprocess_cmd(igv_command)
    elapsed_time = datetime.datetime.now() - startTime
    print("\nIGV finished; elapsed time is:\n{}\n".format(elapsed_time))



def main(onlysnap, genome = 'hg19', image_height = '500', outdir = 'IGV_Snapshots',
         igv_jar_bin = "bin/IGV_2.3.81/igv.jar", igv_mem = "4000"):
    '''
    Main control function for the script
    '''
    batchscript_file = str(onlysnap)
    file_exists(batchscript_file, kill = True)
    run_IGV_script(igv_script = batchscript_file, igv_jar = igv_jar_bin, memMB = igv_mem)


def run():
    '''
    Parse script args to run the script
    '''
    # ~~~~ GET SCRIPT ARGS ~~~~~~ #
    parser = argparse.ArgumentParser(description='IGV snapshot automator')

    # optional flags
    parser.add_argument("-bin", default = default_igv_jar, type = str, dest = 'igv_jar_bin', metavar = 'IGV bin path', help="Path to the IGV jar binary to run")
    parser.add_argument("-mem", default = "4000", type = str, dest = 'igv_mem', metavar = 'IGV memory (MB)', help="Amount of memory to allocate to IGV, in Megabytes (MB)")
    parser.add_argument("-onlysnap", default = False, dest = 'onlysnap', help="Path to batchscript file to run in IGV. Performs no error checking or other input evaluation, only runs IGV on the batchscript and exits.")


    args = parser.parse_args()

    igv_jar_bin = args.igv_jar_bin
    igv_mem = args.igv_mem
    onlysnap = args.onlysnap

    main(onlysnap = onlysnap, igv_jar_bin = igv_jar_bin,
         igv_mem = igv_mem)



if __name__ == "__main__":
    run()