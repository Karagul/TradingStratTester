# Trading Simulator Tool

This code is still very broken but works on Python 3.7 and PyQT5. For a fully working version, use the code from the Master Branch.

UPCOMING CHANGES:

* Each simulation will become an object with different properties instead of just spitting out the data.
* A new simulator class will be implemented. Different types of simulators such as the error checking one will be simply be a subclass that that implements different abstract functions.
* The different modules will become their own classes.
* More documentation will be added overall.
* The GUI will be redone to use a grid instead of fixed points. This will allow the user to set the window to any size. Will also fix the annoying issue where text don't fit on buttons...
* Instead of a button for every strategy, a simple combo box will be used instead.
* A report function with detailed data will be added.
* Multithreaded approach, so that the GUI doesn't freeze all the time.
