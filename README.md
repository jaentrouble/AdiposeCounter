# AdiposeCounter

Counting adipose cells area

## How to use

1. Open folder

2. Set membrane color and Cell color

3. Adjust cell-to-membrane ratio and press **Set** 

    *- This wil show a new mask image.*

4. Use **Draw Border** and **Color White** to adjust mask image

5. Press **Enter** or press **Apply** button to apply the changes.

    *-Recommand to __Apply__ frequently as many layers slows down the app*

6. Use **Set Length** to modify pixel-to-area ratio. 

    *-This is by default 50μm, 800\*600 image*

7. Use **Fill Cell** to fill the counting cells and calculated areas will show up on the list. You can still modify pixel-to-area ratio and will immediately applied to the list.

8. You can select a value from the list and **Delete** it. It will also delete the cell mark of the mask.

9. Press **Save** and select desired Excel(\*.xlsx) file to save the area list. This will also save mask images to *dir_to_image\\save\\*

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
  
  - Do not open the excel file while saving. This might cause saving error.
 
