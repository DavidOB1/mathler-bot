# Mathler Bot

Mathler is an online Worlde-style puzzle game that involves writing an equation that equates to 
a specified number. It can be played here: https://www.mathler.com/

If you want to run the code, make sure the included Chrome driver matches the version of your
Google Chrome. If not, install the correct version from here: https://chromedriver.storage.googleapis.com/index.html

This bot takes a rather brute force approach to solving the Mathler puzzles by going through the possible characters
and seeing if it equals the desired number, then guessing the equation. It of course makes corrections based on information
it gathers from guesses, but it avoids more complication logical deductions (ex: one yellow and one gray mean that a certain character
can only be guessed once) in order to guess faster. It will also avoid guesses at the start that repeat characters in order to gather
more information. 
While this strategy usually works pretty well, there are likely more optomized approaches out there that potentially use more complicated
algorithms. If you have any suggestions, feel free to shoot me an email: davidob323@gmail.com. Feel free to also let me know if the code
doesn't work or throws exceptions; this happens often since they usually change the source code of the Mathler website every once in a while.
