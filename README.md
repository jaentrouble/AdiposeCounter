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

## How to use (v2.0.0)

1. Open folder

2. Press **Box**

  *- Click two diagonal Vertex of imaginary box around a cell*
 
3. Than the image is cut as the imaginary box around the cell.

4. click **AI mask**

   *- This may take some time*

5. Adjust cell-to-membrane ratio and press **Set** 

4. Use **Draw Border** and **Color White** to adjust mask image

5. Press **Enter** or press **Apply** button to apply the changes.

    *-Recommand to __Apply__ frequently as many layers slows down the app*

6. Use **Set Length** to modify pixel-to-area ratio. 

    *-The default value is empirical value when the image is 1600\*1200 with 50μm standard*
    
7. Use **Fill Cell** to fill the counting cells and calculated areas will show up on the list. You can still modify pixel-to-area ratio and it will immediately be applied to the list.
    
8. Press **Confirm**

    *- The image returns to the original image. A puple box is shown around the cell you just counted.*
    
    *- You can hide or show the box with **Hide Box / Show Box** button*
    
    *- The yellow cell mask will disappear, but the area is still in the list.*

9. You can select a value from the list and **Delete** it. It will also delete the box around the counted cell.

10. Press **Save** and select desired Excel(\*.xlsx) file to save the area list. This will also save mask images to *dir_to_image\\save\\*

10. Use **Next** and **Prev** button to change image. This will **RESET** masks and list of cell areas. So make sure you saved all before changing image.

    *-You need to save __PER__ image.*

## Key bindings

- Draw Border

  - Right click : Stop continuing line

  - z : Cancel last drawing (Similar to usual ctrl + z) \**Note: This will not work if modifications are already __Applied__*

  - Enter : **Apply**

- Color White

  - z : Same as **Draw Border**

- Fill Cell

  - z : Same behaviour, but will only cancel last cell layers, not Drawn layers.
  
## Cautions
  
  - Do not edit or open the excel file with Excel (or other programs) while saving. This might cause saving error.
 
