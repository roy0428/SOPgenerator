# Generator

## Requirements

One .bag corrsponding with these files:

- Raw: .bag
- Aligned Frames: 200 
- Coord: .npy
- Lable list: (file ID, label type, labeling, contributor, QC)
- Json file: .json
- Video: RGB Frame, .mp4 (youtube) 

### Run
```
.\grap_filename.bat
enter filename only
```
Generate following file:
- filenames.csv
- elements.csv
- sample.csv > result
- video

### Directory Layout

   ├── bag                 
      ├── labeled
        ├── 019-U_girder, 20210407-U_girder, 20210407-wall, 20210416-MRT_Station
          ├── all annotations file `.json`
      ├── labeled_csv_list   
      ├── tools
      ├── script_file
      
     .
    ├── build                   # Compiled files (alternatively `dist`)
    ├── docs                    # Documentation files (alternatively `doc`)
    ├── src                     # Source files (alternatively `lib` or `app`)
    ├── test                    # Automated tests (alternatively `spec` or `tests`)
    ├── tools                   # Tools and utilities
    ├── LICENSE
    └── README.md
