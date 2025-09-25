import os
import magic
from pathlib import Path
from filecmp import cmp
from PIL import Image
import cv2

# Open images in the application of choice 
def show_images(dups,data_directory):
    for d in dups:
        file = data_directory / d
        file_type=magic.from_file(file)
        if 'image' in file_type:
            im = Image.open(file)
            im.show()
        else:
            print("This is the metadata for the file.",file,"Looks like a video file.")
            video = cv2.VideoCapture(file)
            if not video.isOpened():
                print("Error: Could not open video file.")
            else:
                fps = video.get(cv2.CAP_PROP_FPS)
                width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                duration_seconds = frame_count / fps if fps > 0 else 0

                print(f"Frame Rate (FPS): {fps}")
                print(f"Width: {width} pixels")
                print(f"Height: {height} pixels")
                print(f"Total Frames: {frame_count}")
                print(f"Duration: {duration_seconds:.2f} seconds")

                video.release()
            
# Review and move the duplicates
def do_review(data_directory,dup_set):
    for dup in dup_set:
        if len(dup)==1:
            continue
        show_images(dup,data_directory)
        confirmation=input("Are these duplicates?")
        if confirmation.lower()=='y':
            choice=input("Do you want to move duplicates to duplicate directory?")
            if choice.lower()=='y':
                print(dup)
                file_to_retain=input("Which of the files do you want to retain?")
                duplicate_folder = "duplicate_"+file_to_retain
                os.makedirs(data_directory / duplicate_folder,exist_ok=True)
                for d in dup:
                    if d==file_to_retain:
                        continue
                    print("Trying to move",d,"to",duplicate_folder)
                    try:
                        os.rename(data_directory / d, data_directory/duplicate_folder/d)
                    except:
                        print("Unable to move file -",d)

def do_dry_run(data_directory,dups):
   handle_without_review(data_directory,dups,True) 

def do_silent_operation(data_directory,dups):
   handle_without_review(data_directory,dups,False) 

# Move without review
def handle_without_review(data_directory,dup_set,dry_run):
    for dup in dup_set: 
        dup.sort(reverse=True)
        file_to_retain=dup[0]
        duplicate_folder = "duplicate_set_"+file_to_retain
        if dry_run:
            print("Creating new directory",duplicate_folder,"will be created under data_directory")
        else:
             os.makedirs(data_directory / duplicate_folder,exist_ok=True)
        for d in dup:
            if d==file_to_retain:
                continue
            print("Moving",d,"to",duplicate_folder)
            if not dry_run:
                try:
                    os.rename(data_directory / d, data_directory/duplicate_folder/d)
                except:
                    print("Unable to move file -",d)
        
#Sub routine to identify duplicates
def identify_duplicates(files):
    duplicateSets = []
    for file in files:
#If this is the first itearation, simply add the file to the duplicateSets and continue
        if len(duplicateSets)==0:
            duplicateSets.append([file])
            continue

        is_duplicate = False

        if os.path.isdir(data_directory/file):
            continue

#Each element of duplicate sets is an array. This array contains the files that are duplicates of each other
        for dup in duplicateSets:
# For each element, it is enough to compare it against the first element of the set
            is_duplicate = cmp(
                data_directory / file,
                data_directory / dup[0],
                shallow=False
            )
# if duplicate, add to the same set.
            if is_duplicate:
                dup.append(file)
                break

#if not a duplicate, add it the main set
        if not is_duplicate:
            duplicateSets.append([file])
    return duplicateSets


description='''This program identifies the duplicates of images in a directory. You can run the program in the following
modes. 
1. Output duplicates
2. Review mode
3. Dry run for unprompted moves
4. Unprompted moves.

In the first mode, it simply print out which files are duplicate sets.
In the second, you can chose to review the duplicates, set by set. This will open each set one by one, and wait for you
to confirm. This operation is recommended for the first time. You can also chose which file to retain. The preview is
available only for photos and not videos.
Third is more like what would happen if you opt for 4. It will tell which files will be moved where but wont actually
move until select 4
Fourth does the move without your inputs.'''
print(description)
str_input = input("Enter the choice from above as number between 1 and 4: ")
mode = int(str_input)
directory = input("Enter the directory: ")
data_directory = Path(directory)
#Get the list of files in the directory
files = sorted(os.listdir(data_directory))
duplicateSets = identify_duplicates(files)
match mode:
    case 1:
        for dup in duplicateSets:
            if len(dup) == 1:
                continue
            dup.sort(reverse=True)
            print(dup)
    case 2:
        do_review(data_directory,duplicateSets)
    case 3:
        do_dry_run(data_directory,duplicateSets)
    case 4:
        do_silent_operation(data_directory,duplicateSets) 
