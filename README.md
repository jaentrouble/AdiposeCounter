# AdiposeCounter

Counting adipose cells area

## Install
- .exe file
- .7z compressed folder

Both versions do not need extra installation steps and are portable.

.exe file is slower than .7z version, in terms of initial loading.

### Requires c++ redistributional

Install from the link below (Only tested with x64)
https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads

## How to use (v2.1.0)

1. Open folder

2. Press **Box** or keyboard shortcut **B**

    -*Click two diagonal Vertex of imaginary box around a cell*
 
3. Than the cell inside the box will be colored.

    -*It will recognize only one cell per a box*

    3-1. You can change filling strength by changing the ratio. Default is 50.
    
    3-2. The calculated areas are shown on the list.

4. Use **Set Length** to modify pixel-to-area ratio. 

    -*The default value is empirical value when the image is 1600\*1200 with 50μm standard*

5. You can hide or show the box with **Hide mask / Show mask** button.

6. You can select a value from the list and **Delete** it.

7. Press **Save** and select desired Excel(\*.xlsx) file to save the area list. This will also save .json data to *dir_to_image\\save\\*

    -*This JSON data holds information about the box and the filled cells. If you do not need it, it's safe to delete them*

8. Use **Next** and **Prev** button to change image. This will **RESET** masks and list of cell areas. So make sure you saved all before changing image.

    -*You need to save __PER__ image.*

## Key bindings

- **Box** button = b

- Delete one last cell = z

## Cautions
  
  - Do not edit or open the excel file you are trying to save to while saving. This might cause saving error.
 
## Reference
[1] HRNet-Semantic-Segmentation https://github.com/HRNet/HRNet-Semantic-Segmentation
