# HuskyLens-MicroPython

Designed for both XRP BETA and XRP V1. On the V1 Board use QWIIC port 0.

Once your XRP has the files, run qwiic_huskylens_jacob_classify_objs.py

Upload these files to your XRP robot with the following structure:
```
.
├── XRPExamples/
│
├── lib/
│   ├── XRPLib/
│   ├── ble/
│   ├── phew/
│   ├── qwiic_huskylens.py
│   └── qwiic_i2c/
│       ├── __init__.py
│       ├── i2c_driver.py
│       └── micropython_i2c.py
│
└── qwiic_huskylens_jacob_classify_objs.py
```
