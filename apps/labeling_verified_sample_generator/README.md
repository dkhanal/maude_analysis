Verified Sample Generator

This application allows the User to perform manual labeling of records. The objective is to generate a carefully curated set of positive and negative records, that could be used as seeds to generate more training records to train the computer models.

The application runs in an infinite loop (until User selects to quit) prompting the User to label a randomly selected record from a set of input files (supplied through configuration -- see config.json).

To aid the user's decision making, the application makes suggestions based on classification from a set of models.


To Run:

```
python main.py
```

For cloud-integration, make sure to add a file called .setenv.py and include these lines:

```
import os
