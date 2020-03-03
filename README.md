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

TO DO 28/12/2019
- Add linear and logarithmic regression to plot_patient_donning_all_s_1_5_10_14 
    and plot_patient_donning_p2_p5_p8_s_all. Include r^2 values and equations.
- perform Wicoxson signed rank test on NASA workload, stress, and
    satisfaction first training last training for patients and for carers
- For ROM, take the single maximum value of each patient initial (and final if exists) 
    for L and R and plot as histogram with extension being a negative bar, and flexion
    being a positive bar. Make initial and final assessment values for one patient 
    be clearly grouped together next to each other and other patients' values be further
    off on the same plot.
    
TO DO 02/03/2020
- Edit boxplot of plot_patient_donning_all_s_1_5_10_14 with log reg and wilcoxon to add OT 
    donning onto the same plot. Use colour coding and add legend to differentiate between 
    OT and patient
- Plot FES times across all patients for first 5 sessions as boxplot, i.e. first box =
    all trials from first session from all patients for whom the data is available
- When plotting the above print (not on plot) the number of data points which were used and from how many 
    patients for each box.

