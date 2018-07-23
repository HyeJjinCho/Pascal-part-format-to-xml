# Pascal-part-format-to-xml
change Pascal part dataset format(.mat) to Pascal VOC dataset format(.xml)

this code is only for license plate part (but you can also use it in other cases)


## Download Pascal Part Dataset
Download Pascal part dataset from [Pascal part dataset](http://www.stat.ucla.edu/~xianjie.chen/pascal_part_dataset/pascal_part.html).

move 'mat_to_xml.py' to '/trainval' which is Pascal part dataset unzipped folder.

and make 'xml_annotations' folder under '/trainval'.

```
trainval
+--Annotations_Part
+--examples
+--xml_annotations   #like this
+--mat_to_xml.py  # like this
+--...
```


## Modify 'mat_to_xml.py'
### In def read_mat_file(filepath, _filename)
If mat_to_xml.py and Pascal part dataset directory isn't same, you have to change below path
```python
ROOT = os.getcwd()

pascal_part_path = 'Annotations_Part'
xml_file_path = 'xml_annotations'
```


Change object name you want to detech
```python
        if objs_name == 'car' or objs_name == 'bus':  # change here
            objs_part = np.ndarray.tolist(anno_object[i][3])
            if len(objs_part) == 0:
                continue
```


Change part name you want to detech
```python
                if objs_part_name == 'bliplate' or objs_part_name == 'fliplate':  # change here
                    if objs_name == 'car': count_car += 1
                    if objs_name == 'bus': count_bus += 1
                    is_car = True
```

### In def make_xml_file(_mat_list, _filename)

below line is just for recoding which file has which parts (you can remove, it has no effect on performance.)
```python
ElementTree(root).write(os.path.join(xml_file_path, _filename + '.xml'))
    f = open(os.path.join(ROOT, 'file_info.txt'), 'a')                         # this line
    text = '%s, %d, %d, %d \n' %(_filename, count_car, count_bus, count_file)  # this line
```


