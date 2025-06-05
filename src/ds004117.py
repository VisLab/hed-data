import os
import re


def rename_coordsystem_files(root_dir):
    # Pattern to match run-1 coordsystem files for renaming
    pattern = re.compile(
        r"^(sub-[^_]+_ses-[^_]+)_task-WorkingMemory_run-1_coordsystem\.json$"
    )
    # Pattern to match all coordsystem files with run number
    delete_pattern = re.compile(
        r"^(sub-[^_]+_ses-[^_]+)_task-WorkingMemory_run-(\d+)_coordsystem\.json$"
    )
    # Pattern for electrodes.tsv files with _task-WorkingMemory
    electrodes_pattern = re.compile(
        r"^(sub-[^_]+_ses-[^_]+)_task-WorkingMemory_run-(\d+)_electrodes\.tsv$"
    )
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Rename run-1 coordsystem files
            match = pattern.match(filename)
            if match:
                new_filename = f"{match.group(1)}_coordsystem.json"
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                else:
                    print(f"Skipped (target exists): {new_path}")
                continue
            # Delete coordsystem files with run > 1
            del_match = delete_pattern.match(filename)
            if del_match and int(del_match.group(2)) > 1:
                del_path = os.path.join(dirpath, filename)
                os.remove(del_path)
                print(f"Deleted: {del_path}")
                continue
            # Rename electrodes.tsv files to remove _task-WorkingMemory
            electrodes_match = electrodes_pattern.match(filename)
            if electrodes_match:
                new_filename = f"{electrodes_match.group(1)}_run-{electrodes_match.group(2)}_electrodes.tsv"
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                else:
                    print(f"Skipped (target exists): {new_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Rename and clean coordsystem files.")
    parser.add_argument("root_dir", help="Root directory to process")
    args = parser.parse_args()
    rename_coordsystem_files(args.root_dir)


if __name__ == "__main__":
    main()
