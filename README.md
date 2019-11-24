PyCharm -> Open

Open terminal (Alt+F12)

pip install -r requirements.txt


To get latest changes from original repository (to update my fork)
git fetch upstream
git merge upstream/master


Box plots

https://matplotlib.org/3.1.1/gallery/pyplots/boxplot_demo_pyplot.html#sphx-glr-gallery-pyplots-boxplot-demo-pyplot-py
https://matplotlib.org/examples/pylab_examples/boxplot_demo2.html


Scatter plots

marker size
https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size
marker shape
https://stackoverflow.com/questions/47684652/how-to-customize-marker-colors-and-shapes-in-scatter-plot


TO DO
- Fix times for activation so there are two versions: one
    with ascending sessions on x axis, the other with sessions
    sorted according to number trials in each session
- Add error bars to TPR histogram (+/- 1 standard deviation)
- Make TPR plot as box plot
- Make FDR plot (FP/(FP+TP)) also as histogram with error bars
    and box plot
- Fix title for Patient donning p2 p5 p8 s all 


TO DO 24.11.2019

- Make scatter plot of threshold values vs session for 
    each patient and all patients on one plot
- Make boxplots for patients and separate for carers as follows
    1. stress at first and last training session for all users
        (one for patients and one for carers)
    2. stress at first, last training, first independent,
        last independent for p2 p5 p8 and seperate for c2 c5 c8
    3. satisfaction same way as 1 for all patients and all carers. 
    4. satisfaction same way as 2. for p2 p5 p8 and c2 c5 c8