# Assignment 3
## Dataset 1
The code file is dataset1.py that could be run on terminal using the command `python3 dataset1.py` . It takes the text file `dataset1.txt` as input and prints the output as `The estimated equation is m x + c` where m is slope, c is y-intercept of estimated straight line. It also creates an image file `dataset1.png` which plots noisy line, estimated straight line and errorbar.
## Dataset 2
The code file is dataset2.py that could be run on terminal using the command `python3 dataset2.py` . It takes the text file `dataset2.txt` as input and prints the output as
`The time period is T
The estimated parameters are: a sin(t*ω1) +b sin(t*ω2) +c sin(t*ω3)
The standard deviation in using  is np.linalg.lstsq is std1
The estimated parameters are:  a sin(t*ω1) +b sin(t*ω2) +c sin(t*ω3)
The standard deviation in using scipy.optimize.curve_fit() is std2` where T is time period, std1 is standard deviation from lstsq and std2 is that from curvefit, a,b,c are amplitudes of sine waves of frequencies ω1,ω2,ω3 respectively. It also creates 2 image files `dataset2_curvefit.png` and `dataset2_lstsq.png`
## Dataset 3
### First solution
The code file is dataset3_1.py that could be run on terminal using the command `python3 dataset3_1.py`.  It creates an image file `dataset3_1.png` which plots estimated and original curves. It also prints estimated temperature on terminal.
### Second solution
The code file is dataset3_2.py that could be run on terminal using the command `python3 dataset3_2.py`.  It creates an image file `dataset3_2.png` which plots estimated and original curves. It also prints estimated values of h,c,T,kB on terminal.
## Documentation
`Documentation.pdf` contains code snippets with the explanations. It also provides additional codes to verify dataset2 solutions through `fourier transformation`. In dataset3_1, it shows logically why only a `certain range of guesses` work.  In dataset3_2, it goes through various methods and shows the best possible way to `get constants even without exact initial guess`. It gives explanation of how `lstsq()` works by breaking down its algorithm in dataset_1.