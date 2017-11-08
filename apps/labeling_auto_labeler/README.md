Auto Labeler

This application performs an iterative auto-labeling with integrated quality control (QC). Labeling is based on classification using a high-accuracy model. The model is re-trained 
after each QC.


To Run:

```
python main.py
```

For cloud-integration, make sure to add a file called .setenv.py and include these lines:

```
import os
