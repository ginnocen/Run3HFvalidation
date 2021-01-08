#!/bin/bash

# Script to run AliPhysics tasks in jobs

LISTINPUT="$1"
JSON="$2"
SCRIPT="$3"
DEBUG=$4
NFILESPERJOB=$5
FILEOUT="AnalysisResults.root"

[ $DEBUG -eq 1 ] && echo "Running $0"

# This directory
DIR_THIS="$(dirname $(realpath $0))"

# Load utilities.
source "$DIR_THIS/utilities.sh" || { echo "Error: Failed to load utilities."; exit 1; }

CheckFile "$SCRIPT"
CheckFile "$JSON"
SCRIPT="$(realpath $SCRIPT)"
JSON="$(realpath $JSON)"

LogFile="log_ali.log"
ListIn="list_ali.txt"
FilesToMerge="ListOutToMergeAli.txt"
DirBase="$PWD"
IndexFile=0
ListRunScripts="$DirBase/ListRunScriptsAli.txt"
DirOutMain="output_ali"

# Clean before running.
rm -f $ListRunScripts && \
rm -f $FilesToMerge && \
rm -f $FILEOUT && \
rm -rf $DirOutMain || ErrExit "Failed to delete output files."

CheckFile "$LISTINPUT"
echo "Output directory: $DirOutMain (logfiles: $LogFile)"
# Loop over input files
while read FileIn; do
  CheckFile "$FileIn"
  FileIn="$(realpath $FileIn)"
  IndexJob=$((IndexFile / NFILESPERJOB))
  DirOut="$DirOutMain/$IndexJob"
  # New job
  if [ $((IndexFile % NFILESPERJOB)) -eq 0 ]; then
    mkdir -p $DirOut || ErrExit "Failed to mkdir $DirOut."
    FileOut="$DirOut/$FILEOUT"
    echo "$FileOut" >> "$DirBase/$FilesToMerge" || ErrExit "Failed to echo to $DirBase/$FilesToMerge."
    # Add this job in the list of commands.
    echo "cd \"$DirOut\" && bash \"$DIR_THIS/run_ali.sh\" \"$SCRIPT\" \"$ListIn\" \"$JSON\" \"$LogFile\"" >> "$ListRunScripts" || ErrExit "Failed to echo to $ListRunScripts."
  fi
  echo $FileIn >> "$DirOut/$ListIn" || ErrExit "Failed to echo to $DirOut/$ListIn."
  [ $DEBUG -eq 1 ] && echo "Input file ($IndexFile, job $IndexJob): $FileIn"
  ((IndexFile+=1))
done < "$LISTINPUT"

echo "Running AliPhysics jobs... ($(cat $ListRunScripts | wc -l) jobs)"
OPT_PARALLEL="--halt soon,fail=100%"
if [ $DEBUG -eq 0 ]; then
  parallel $OPT_PARALLEL < $ListRunScripts > $LogFile 2>&1
else
  parallel $OPT_PARALLEL --will-cite --progress < $ListRunScripts > $LogFile
fi
[ $? -ne 0 ] && ErrExit "\nCheck $(realpath $LogFile)"
[ "$(grep -e '^'W- -e '^'Warning "$LogFile")" ] && MsgWarn "There were warnings!\nCheck $(realpath $LogFile)"
[ "$(grep -e '^'E- -e '^'Error "$LogFile")" ] && MsgErr "There were errors!\nCheck $(realpath $LogFile)"
[ "$(grep -e '^'F- -e '^'Fatal "$LogFile")" ] && ErrExit "There were fatal errors!\nCheck $(realpath $LogFile)"
rm -f $ListRunScripts || ErrExit "Failed to rm $ListRunScripts."

echo "Merging output files... (output file: $FILEOUT, logfile: $LogFile)"
hadd $FILEOUT @"$FilesToMerge" >> $LogFile 2>&1 || \
{ MsgErr "Error\nCheck $(realpath $LogFile)"; tail -n 2 "$LogFile"; exit 1; }
rm -f $FilesToMerge || ErrExit "Failed to rm $FilesToMerge."

exit 0
