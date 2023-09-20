{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Practice Lab: Linear Regression\n",
    "\n",
    "Welcome to your first practice lab! In this lab, you will implement linear regression with one variable to predict profits for a restaurant franchise.\n",
    "\n",
    "\n",
    "# Outline\n",
    "- [ 1 - Packages ](#1)\n",
    "- [ 2 - Linear regression with one variable ](#2)\n",
    "  - [ 2.1 Problem Statement](#2.1)\n",
    "  - [ 2.2  Dataset](#2.2)\n",
    "  - [ 2.3 Refresher on linear regression](#2.3)\n",
    "  - [ 2.4  Compute Cost](#2.4)\n",
    "    - [ Exercise 1](#ex01)\n",
    "  - [ 2.5 Gradient descent ](#2.5)\n",
    "    - [ Exercise 2](#ex02)\n",
    "  - [ 2.6 Learning parameters using batch gradient descent ](#2.6)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "_**NOTE:** To prevent errors from the autograder, you are not allowed to edit or delete non-graded cells in this notebook . Please also refrain from adding any new cells. \n",
    "**Once you have passed this assignment** and want to experiment with any of the non-graded code, you may follow the instructions at the bottom of this notebook._"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a name=\"1\"></a>\n",
    "## 1 - Packages \n",
    "\n",
    "First, let's run the cell below to import all the packages that you will need during this assignment.\n",
    "- [numpy](www.numpy.org) is the fundamental package for working with matrices in Python.\n",
    "- [matplotlib](http://matplotlib.org) is a famous library to plot graphs in Python.\n",
    "- ``utils.py`` contains helper functions for this assignment. You do not need to modify code in this file.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from utils import *\n",
    "import copy\n",
    "import math\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2 -  Problem Statement\n",
    "\n",
    "Suppose you are the CEO of a restaurant franchise and are considering different cities for opening a new outlet.\n",
    "- You would like to expand your business to cities that may give your restaurant higher profits.\n",
    "- The chain already has restaurants in various cities and you have data for profits and populations from the cities.\n",
    "- You also have data on cities that are candidates for a new restaurant. \n",
    "    - For these cities, you have the city population.\n",
    "    \n",
    "Can you use the data to help you identify which cities may potentially give your business higher profits?\n",
    "\n",
    "## 3 - Dataset\n",
    "\n",
    "You will start by loading the dataset for this task. \n",
    "- The `load_data()` function shown below loads the data into variables `x_train` and `y_train`\n",
    "  - `x_train` is the population of a city\n",
    "  - `y_train` is the profit of a restaurant in that city. A negative value for profit indicates a loss.   \n",
    "  - Both `X_train` and `y_train` are numpy arrays."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [],
   "source": [
    "# load the dataset\n",
    "x_train, y_train = load_data()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### View the variables\n",
    "Before starting on any task, it is useful to get more familiar with your dataset.  \n",
    "- A good place to start is to just print out each variable and see what it contains.\n",
    "\n",
    "The code below prints the variable `x_train` and the type of the variable."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Type of x_train: <class 'numpy.ndarray'>\n",
      "First five elements of x_train are:\n",
      " [6.1101 5.5277 8.5186 7.0032 5.8598]\n"
     ]
    }
   ],
   "source": [
    "# print x_train\n",
    "print(\"Type of x_train:\",type(x_train))\n",
    "print(\"First five elements of x_train are:\\n\", x_train[:5]) "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "`x_train` is a numpy array that contains decimal values that are all greater than zero.\n",
    "- These values represent the city population times 10,000\n",
    "- For example, 6.1101 means that the population for that city is 61,101\n",
    "  \n",
    "Now, let's print `y_train`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Type of y_train: <class 'numpy.ndarray'>\n",
      "First five elements of y_train are:\n",
      " [17.592   9.1302 13.662  11.854   6.8233]\n"
     ]
    }
   ],
   "source": [
    "# print y_train\n",
    "print(\"Type of y_train:\",type(y_train))\n",
    "print(\"First five elements of y_train are:\\n\", y_train[:5])  "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Similarly, `y_train` is a numpy array that has decimal values, some negative, some positive.\n",
    "- These represent your restaurant's average monthly profits in each city, in units of \\$10,000.\n",
    "  - For example, 17.592 represents \\$175,920 in average monthly profits for that city.\n",
    "  - -2.6807 represents -\\$26,807 in average monthly loss for that city."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Check the dimensions of your variables\n",
    "\n",
    "Another useful way to get familiar with your data is to view its dimensions.\n",
    "\n",
    "Please print the shape of `x_train` and `y_train` and see how many training examples you have in your dataset."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The shape of x_train is: (97,)\n",
      "The shape of y_train is:  (97,)\n",
      "Number of training examples (m): 97\n"
     ]
    }
   ],
   "source": [
    "print ('The shape of x_train is:', x_train.shape)\n",
    "print ('The shape of y_train is: ', y_train.shape)\n",
    "print ('Number of training examples (m):', len(x_train))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The city population array has 97 data points, and the monthly average profits also has 97 data points. These are NumPy 1D arrays."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Visualize your data\n",
    "\n",
    "It is often useful to understand the data by visualizing it. \n",
    "- For this dataset, you can use a scatter plot to visualize the data, since it has only two properties to plot (profit and population). \n",
    "- Many other problems that you will encounter in real life have more than two properties (for example, population, average household income, monthly profits, monthly sales).When you have more than two properties, you can still use a scatter plot to see the relationship between each pair of properties.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAYAAAAEWCAYAAABv+EDhAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+j8jraAAAgAElEQVR4nO2debheVXX/P98oOEICJMxDVNCKFq4kvwRwwuFRRAW1zlaxKtT6Izch2kq1kov2V4dqgGi1DwoOFBGtE1WcCgJiBUlCCENoQQsIQQhDAEdM7vr9sc/hnnvyzved3+/nec7zvmefYa/z3nP32nuttddWRGCMMWb0mNVrAYwxxvQGKwBjjBlRrACMMWZEsQIwxpgRxQrAGGNGFCsAY4wZUawATNNIeqakGyX9RtIrJH1P0rG9lqufkBSS9m/x2jdJ+mG7Zeolkq6TdESv5TDTkecBjAaSbgZ2A7YCvwUuAJZExG9auNeFwPkRcXqFY28F3hERz5qRwG0ia3QuAn4HBLAR+EhEfL7D9QZwQETcVOe8+cD/AttFxJZOytQvSJoA9o+Iv+y1LKOORwCjxcsj4vHAIcD/Af6hfIKkRzZwn/2A69osWyfZmD33jsB7gc9KOrDHMg00Db4nps+xAhhBIuJ24HvA0+Fhc8X/lXQjcGNWdpykmyTdK+l8SXtm5b8Angj8R2YCepSkiyW9Q9JTgX8FDsuObc6uOUrS9ZIelHS7pPeUZcrus1nS0wtl8yT9XtKukuZK+k52zr2SfiKpqfc3Et8C7gMOzOo8TdLGbDtN0qOyuo+QdJuk90m6W9LNkt5UkO1iSe8o7L9V0mWV6pX0UklXSXpA0q+yHnDOpdnn5uw3O6x8L0mHS7pS0v3Z5+ElOT4k6afZ7/tDSXOryFHvmR4l6eOSbpV0p6R/lfSY0rXvlfRroOIIKntvNmSyXC/pkKz8ZkkvlHQk8D7gddnzXi3pNZLWlO7zbknfqlSHaR9WACOIpH2Ao4CrCsWvABaTGsbnAx8GXgvsAdwCfAUgIp4E3Eo2moiIP+Y3iIgNwDuBn2XH5mSHzgT+OiJ2ICmdi8oyZff5BvCGQvFrgUsi4i7g3cBtwDySKet9JJNOM889S9IrgTnANcD7gUOBMeBgYBHTR0W7A3OBvYBjgTMkPaWZOjN+C7wlq/elwN9IekV27DnZ55zsN/tZSeadge8Cq4BdgJXAdyXtUjjtjcBfAbsC2wPbKNgGn+mjwJNJv8f+2Tknl67dmTQCPL58Y0mvASayZ90ROBq4p3hORHwf+CfgvOx5DwbOB56QdSBy/hI4u8ZzmDZgBTBafCvrlV8GXEL6R8z5cETcGxG/B94EnBURa7OG+e9Jvfr5Ldb7J5Ji2TEi7ouItVXO+zLTFcAbs7L8HnsA+0XEnyLiJ9G4A2vP7LnvBlYAb46I/yY95wcj4q6I2AScAry5dO0HIuKPEXEJqSF+bYN1PkxEXBwR10TEZESsB84Fntvg5S8FboyIsyNiS0ScC9wAvLxwzucj4n+yv91XSQ14LbZ5JkkCjgNOzN6DB0nvx+sL100CK7Jrf1/hvu8APhYRV2ajrZsi4pZ6D5i9Y+eRGn0kPQ2YD3yn3rVmZlgBjBaviIg5EbFfRLyr9E/8q8L3PUm9fgAyR/E9pB5hK/wFacRxi6RLJB1W5byLgMdIWixpP1JD9s3s2D8DNwE/lPRLSSc1Uf/G7Ll3joixiPhKVj7tObPvexb274uI39Y43hDZ8/xY0iZJ95NGSRXNNBUoy5jLUfxb/Lrw/XfA42vcr9ozzQMeC6zJzGybge9n5TmbIuIPNe69D/CLGsdr8UXgjZkiejPw1eLo0nQGKwCTU+xNbyQN8wGQ9DiS+eH2Ju+TClKP8BiSieJbpF7qthdGTGbH3kDq/X8n64kSEQ9GxLsj4omk3u9ySS9o5MFqMO05gX2zspydsmevdPy3pAYzZ/ca9XyZZObYJyJmk/wkyo7VG8WUZczlaORvUYlqz3Q38HvgaZmynBMRszPneU49WX8FPKkBGSq9I5cDDwHPJv3tbf7pAlYAphJfBv5K0ljmFP0n4IqIuLmBa+8E9pa0PYCk7ZXi2mdHxJ+AB0ihqLXqfh3JPJObf5D0Mkn7Zz3E/B617tMI5wL/kDmb55Ls3f9WOueU7BmeDbwM+FpWvg54laTHKsX7v71GPTsA90bEHyQtIjVwOZtIppUnVrn2AuDJkt4o6ZGSXgccyMzMI9s8U6Z8PwucKmlXAEl7SXpxE/f9HPAeSQuU2D8byZW5E5ivbZ34XwI+BWyJiIoOddNerADMNkTEhcAHgK8Dd5B6da+vedEUF5FCRH8t6e6s7M3AzZIeIJk/qsZ/R8QVpN71nqRIpZwDgP8EfgP8DPh0RFwMoDQR7X0NylfkH4HVwHqSU3htVpbza1LE0EbgHOCdEXFDduxUUo/1TpL54pwa9bwL+KCkB0lK5uERUET8Dvh/wE8z08uhxQsj4h5SI/1ukhnu74CXRcTdtEatZ3ovycx2efa3+k+gYad3RHwte5YvAw+SRns7Vzg1V6L3SCr6g84mBQm4998lPBHMmAooTSD7t4jYu9eytIt+f6Ys5PQu4JCIuLHX8owCHgEYY/qFvwGudOPfPTybzxjTc5RSlYg0H8V0CZuAjDFmRLEJyBhjRpSBMAHNnTs35s+f32sxjDFmoFizZs3dETGv2vGOKYAs38yXSBNkJoEzIuJ0pURYx5HinwHeFxEX1LrX/PnzWb16dadENcaYoURSzVQcnRwBbAHeHRFrJe1AmmL+o+zYqRHx8Q7WbYwxpg4dUwARcQdpEhER8aCkDbSeS8YYY0yb6YoTOMsi+QzgiqzoBEnrJZ0laacq1xwvabWk1Zs2bap0ijHGmBnQcQUg6fGklALLIuIB4DOk1AJjpBHCJypdFxFnRMTCiFg4b15VH4YxxpgW6agCkLQdqfE/JyK+ARARd0bE1kLyqUWdlMEYYwaS8hytDszZ6pgCyLI2nglsiIiVhfI9Cqe9Eri2UzIYY8xAMjEBJ5441ehHpP2JibZW08kRwDNJWSCfL2ldth0FfEzSNZLWA88DTuygDMYYM1hEwObNcPrpU0rgxBPT/ubNbR0JdDIK6DKmFr0oUjPm3xhjRhoJTj01fT/99LQBLF2aylWpWW2xqkHIBbRw4cLwRDBjzEgRAbMKRprJyaYbf0lrImJhtePOBWSMMf1GbvYpUvQJtAkrAGOM6SeKNv+lS1PPf+nS6T6BNjEQyeCMMWZkkGDOnOk2/9wnMGeOfQDGGDP0RExv7Mv7DWAfgDHGDCLlxr6NPf8cKwBjjBlRrACMMYNFF1IkjApWAMaYwaFLKRJGBSsAY8xg0MUUCaOCw0CNMYNBF1MkjAoOAzXGDBZtSJEwKjgM1BgzPHQpRcKoYAVgjBkMupgiYVSwD8AYMxh0I0VCG2bfDhL2ARhjBotONdITEymaKFcu+YhjzpyBDTO1D8AYM1x0IkXCiIaY2gRkjDEjGmJqE5AxxuQMWYipTUDGGNMItUJMB6Cj3Ao2ARljTNHmv3hx2iDt543/TjsNrDO4Gh4BGGNMHmI6Pp4a/1WrUvn4OFxxRdofQmewRwDGGAOpd5838NKUIxiG1hlsJ7AxxpQZEmewncDGGNMMI5RvyArAGGNyRizfkH0AxhiT0418Q32EfQDGGFNmSJLC9cwHIGkfST+WtEHSdZKWZuU7S/qRpBuzz506JYMxxrREJ/IN9SGd9AFsAd4dEU8FDgX+r6QDgZOACyPiAODCbN8YY0yX6ZgCiIg7ImJt9v1BYAOwF3AM8MXstC8Cr+iUDMYYY6rTlSggSfOBZwBXALtFxB2QlASwa5Vrjpe0WtLqTZs2dUNMY4wZKTquACQ9Hvg6sCwiHmj0uog4IyIWRsTCefPmdU5AY4wZUTqqACRtR2r8z4mIb2TFd0raIzu+B3BXJ2UwxhhTmU5GAQk4E9gQESsLh84Hjs2+Hwt8u1MyGGOMqU4nJ4I9E3gzcI2kdVnZ+4CPAF+V9HbgVuA1HZTBGGNMFTqmACLiMqBa8OwLOlWvMcaYxnAuIGOMGVGsAIwxZkSxAjDGmBHFCsAYY0YUKwBjjBlRrACMMabdlNPs92nafSsAY4xpJxMT01cPy1cZm5jopVQVsQIwxph2EQGbN09fQjJfYnLz5r4bCXhJyEYYktWBjDEdpriE5Omnpw2mLzHZR3gEUI8BGs4ZY/qAohLI6cPGH6wAajNgwzljTB+QtxNFip3IPsIKoBa5Jl+6NDX6s2alzz4dzhljekyxk7h0KUxOTrUffagErADqMUDDOWNGgn4OsZRgzpzpncS8EzlnTt+1G3YC16PacM5KwJjuMzGRzK/5/1/+/zlnTv/45SYmpgeK5EqgD9sLjwBqMWDDOWOGmkHyyZUb+z5s/MEjgNpUG85BXw7njBlqBizEchBQ9JPWrMLChQtj9erVvRPA8wCM6R8iUkBGzuSk/x+rIGlNRCysdtwmoEYYkOGcMUPPAIVYDgJWAMaYwcA+ubZjH4AxZjCwT67t2AdgjBks7JNrGPsAjDHDhX1ybaOuCUiSgEXAXkAAG4GfxyAMHYwxxlSlpgKQ9CLg08CNwO1Z8d7A/pLeFRE/7LB8xgw2NleYPqbeCOB04IURcXOxUNITgAuAp3ZILmMGn0FIW2BGmno+gEcCt1Uovx3Yrv3iGDMkDFLaAjOy1BsBnAVcKekrwK+ysn2A1wNndlIwYwYapy0wA0DdMFBJBwJHk5zAIo0Izo+I6+tcdxbwMuCuiHh6VjYBHAdsyk57X0RcUE9Ih4GagcVpC0wPqRcGWjcKKGvoazb2VfgC8CngS6XyUyPi4y3cz5jBwqnETZ9T0wcgabakj0i6QdI92bYhK5tT69qIuBS4t63SGtNNZrLwiNMWmAGgnhP4q8B9wBERsUtE7AI8D9gMfK3FOk+QtF7SWZJ2avEexnSWiYnpDXXeoDcavTNgK0OZ0aSeApgfER+NiF/nBRHx64j4CLBvC/V9BngSMAbcAXyi2omSjpe0WtLqTZs2VTvNmPbTrgieiYnp5p5cCTgE1PQJ9XwAt0j6O+CLEXEngKTdgLcyFRXUMPk9svt8FvhOjXPPAM6A5ARuti5jWqadETxOW2D6mHojgNcBuwCXSLpP0n3AxcDOwGubrUzSHoXdVwLXNnsPY7pCUQnk2HlrhoyaI4CIuA94b7Y1haRzgSOAuZJuA1YAR0gaI+UUuhn462bva0xXcASPGQEaSQb3Z8AxTE8Gd35EbKh1XUS8oUKxJ4+Z/qccwXPqqVP7YCVghoZ6yeDeC7wB+Arw86x4b+BcSV/JnMGmn3DysZnjhUfMiFBzJrCk/wGeFhF/KpVvD1wXEQd0WD7AM4EbxsnH2ouVqRlwZrogzCSwZ4XyPbJjpl9w8rHWqDXZyxE8Zsip5wNYBlwo6Uamwj73BfYHTuikYKZJnHyseTxiMiNOzRFARHwfeDJwCvAD4IfABPCU7JjpJxy62DgeMRnTUDK4SeDyLshiZopDFxvHIyZjWlsUPksIt0GSzUD9gpOPNY9HTGbEqTsCqEREPFXSLsChbZbHtIpDF5vHIyYz4jSsACTtDEQ2O5iIuAf4bqcEMy0wMTE9VDFXAm7MtsWTvYypOxFsX+BjwAtIKaAlaUfgIuCk8mLxpg9w6GJjeMRkTN2JYD8DTgP+PSK2ZmWPAF4DLIuIrpiAPBHMdAxP9jJDzEwngs2NiPPyxh8gIrZGxFdIWUKNGWw8YjIjTD0fwBpJnwa+yNREsH2AY4GrOimY6SLuBfcX/nuYLlFvBPAW4Bq2nQh2LfDmjkpmWqeZtWxnuvShaS/+e5guUm8m8EMR8ZmIODIi/jwinh4RL4mIT0fEH7sl5MAzk8XFm60jb0AmJ6fKqzUgng3bX/jvYbpMS/MAACSdHBEfbKcwQ0k38s3kdaxcOdWAXHIJHH003H//VKhj2ZTg2bD9hf8epttEREsbcGur1za7LViwIAaSycmIpUsjIH1W2m93HVu3RoyNpf18q1fX5OT089shl2kd/z1MmwBWR612vOZBeKDK9iCwpda17dwGVgFETG+gG22Q21FHow1IN+QzjeO/h2kjM1UAtwK7VTn2q1rXtnMbaAUQ0Z0eXbmORhqQboxQTOP472HaTD0FUM8H8CVgP+DOCse+PEPr02gQXcg3U6mOsTFYswaWL6+e3sCzYfsL/z1Mt6mlHfplG9gRQC98ACefPOUDyH0CS5dGrFhR+x619k138d/DtAlmOALYhiw/0GMj4ob2q6Mhoxs9ukp1rFiRev5z5sCsWfVHG54N21/472G6RM1cQACSPgycHRHXS/oLYCUpMdx3IuL9XZBx8HMBRRdmdnajDmPMQDHTXEAAL4mI67PvJwIvAg4BXtYG+UaDbvTo3Gs0xjRJvXTQK4A9JJ0CbA88CXgdIGC2pJOBiyPi0o5Laowxpq3UVAARcYqkA0mRQDsDX4qID0raHnhReCawMcYMLI04gd9GSgr3ECksFGBf4MOdEsoYY0znqasAIuK3wGdKZTcBN3VKKGO6ih3oZkRpxAncEpLOknSXpGsLZTtL+pGkG7PPnTpVvzEN4fTLZoTpmAIAvgAcWSo7CbgwIg4ALsz2jekN4fTLZrRpOR10PSLiUknzS8XHAEdk378IXAy8t1MyGFMTp182I07diWAAkuYBxwHzKSiNiHhbnevmkyaMPT3b3xwRcwrH74uIimYgSccDxwPsu+++C2655Za6chrTEhFpxnTO5KQbfzMUtGMiGMC3gdnAfwLfLWwdIyLOiIiFEbFw3rx5nazKjDLVkvXZ/GNGgEZNQI+NiHaYau6UtEdE3CFpD+CuNtzTmNYo2vxzs0++DzYDmaGnUQXwHUlHRcQFM6zvfOBY4CPZ57dneL+Z4fC/0aaZZH1+V8wQ0qgP4EHgccAfgT+RUkFEROxY45pzSQ7fuaT1BFYA3wK+SppIdivwmoi4t179HUkG1421es1gUK9x97tiBpR6PoCGRgARsUOzFUfEG6ocekGz92o7xfA/mD70r7R4uhluaiXS87tihpiaIwBJfxYRN0g6pNLxiFjbMckKdGQEULT/5jj8z1TC74oZUOqNAOopgDMi4nhJP65wOCLi+e0Qsh4dWw/A4X+mUfyumAFkRmGgEXF89vm8CltXGv+O4fA/0yh+V8yQ0slUEP1LOfxvcjJ9FlMCGAN+V8xQ07FUEH1NN9bqNcOB3xUzxDQUBtprOuoDcGz3YNGrv5nfFTOAtCUVhKQLGykbOLyO7mDRy9TNflfMEFJTAUh6tKSdgbmSdsry+e+cJXnbsxsCmgGhPJJs98jSqZuNaTv1fAB/DSwjNfbFmP8HgH/plFBmwOjGTFmnbjam7dQLAz09Ip4AvCcinlDYDo6IT3VJRtMPVOvhd7NnXlQCOW78jWmZmiMASc+PiIuA2yW9qnw8Ir7RMclM/1Cvh9+tnnm1eHwrAWNaop4T+DnZ58srbC/roFy9pdP27E7QKZkb6eF3o2fueHxj2k49H8B92eeZEXFZp4XpCwYx82MnZW7E9t5qz7yZ0ErH4xvTfiKi6gasyz7X1jqv09uCBQuiK0xORixdGgHps9J+v9EtmScn0z3zLb9vq/WvWDH9eH7dihX15ai1b4x5GGB11Ghb640ANki6GZgnaX2hPF8P4KBOKKWekfcqI6b3dsfHu2NnbmWy0UyjYxqps14PP++Zr1w5XZ7ZsyvXP5MUy47HN6Z91NIOSYGwO3A1sF95q3dtu7aujQAiUg90fHx6b3d8vH7PtB31VuoRn3zy9POq9Xir9dBbqbP4rI308Ccnk5zF/a1ba/foi/fJt34dZRkzoFBnBFB3JnBE/DoiDgbuAHbIto0RcUuHdFLviID77oNVq6aXr1qVyis5GstlrTgjiz3isqP1/POTwzM/rzjzNa+rWg+9liy16iyGb1azvS9dmspPOQWWLZu617JlaTv88NqhoA7pNKb31NIO+QY8F7gFuAS4FPhf4DmNXNuOras+gHLvvzgKKPdOW7VjV6u73CMeG6ve88573HlPOz8/L2+kR91ML7yS7b14/fh45ZFTrRGLRwDGdBTqjAAaVQBrgKcU9p8MrGnk2nZsfWkC6oTztWzGKTbuxUayWJ4rg6KyqGd+qVVns3JXasjr3WsQne3GDCDtUgDrGynr1NZVBVBpFFCtJ9vOXmy1e23dWrlRrVd3IzK0S/6yEmnkXu0cPRljKtIuBfB54EzgiGz7LPD5Rq5tx9bXYaC1wiPbUW/es6/WyLfae29XL7yawszLat3LIZ3GdJR6CqDRFcHeCVwHjANLgeuzsuGinsOz0fDIycnm0hRXqnflShgbg3XrKs98zeso1x0NOqGbfdZK5M+/ahUsXpzCZcfHp5zo4+O17+WQTmN6Sy3tkBQIs4Br653Xya2lEcBMepeNXFupl17+bNacUj63GFpZrLPo6M3NU+X9dj5rLYqmnKJjeMUK9+iN6THUGQE0tCKYpHOAv4+IWzurjirT9Ipg3UrnkNezciUsXz41sQnalwwtovJErYkJ+P73U8/7tNPSsWXL4Ior4Mgju5u2opqMxpie0pYVwYA9gOskXSjp/Hxrj4htJhqMb29HPXkmzFmzkhIoUm78y/U2Y6qptL9iRWr8V62abgq64oqZP2ezsnbblNPqb2mMmUaji8Kf0lEp2kk3Fg6ZmEgTw047Ld1v61ZYWFKyxVQJnRiRSFP1t/M5+z0ZXr/LZ8wgUcs+BDyatCLYp0irgz2y1vmd2lr2AZQjZNphk56cjFi8eMrefvLJEXPnpv3dd4/YsqVyTH6nYt4biQRq1M7f7/H5/S6fMX0GMwkDBc4D/i1r/L8FnF7r/E5tTSuAYiNdDk2caZz5ySdHHHzw9Hvn2wknTIU/5rNyc3lmMuO21nPWu2+z8fb9PkO33+Uzpo+YqQK4pvD9kbQpLTRwM3ANsK6egNGsAijHpZdTFDQbJVO+d974VFMCxZ5/+dpqPfX8ezONdaNJ2lrpMc90dnCn6Xf5jOkTZqoA1tbab3XLFMDcRs9vegSQp3MoT1BavLg9Jpdq+YKqNUiVeq25IqoU2tloY91sNs9Gesz93sPud/mM6SNmqgC2Ag9k24PAlsL3B2pdW+e+nVUAEVONayM9xWbNLvUUQKVGudpopDhjtlrun3ry1JO9md+hn23s/S6fMX3GjBRApzZSNtG1pCRzx1c553hgNbB63333bf7JG+0pNmsj37o1YrfdKjf8ixZVToFQnixVViCNpHdodcJWsz3mfs/R0+/yGdNH9KsC2DP73JW02Mxzap3fkhO4kZ5isz3Ksg9g69YpZ/NBByUzTrUGqWzzLzfyZZt9sbGuNiO4keUTW/UB1NrvNf0unzF9Qj0F0Og8gLYSERuzz7skfRNYRFpnoD00soB4RPNzBsrLH86aBT/7WZqBmy+OAtWvTQ+9bQ6fww6DRYvSOatWpRw6kCZ1nX76VE6g/N61lk8s7ktpWcZmF1Lv9xw9/S6fMQNCQ6kg2lqh9DhgVkQ8mH3/EfDBiPh+tWuaTgWRU61xLE8mmpyERzxi6rzJydqNSq1Gt548xcb71FNT43/FFen4nnvCrrum+tevhyVL4Cc/gR13hGc8o3qqiWrPldc3e/aUcmpGXmPMQNOuVBDtZDfgMklXAz8Hvlur8Z8RlXqKEdNTRUxOwoIF08+rl1Wz0R5opXsURyYRKZ0DpIZ/48bU01+/Hg4+ON133brU+JdTTeQLsOeN/IoV1VNg3H//dFmqLdReT3ZjzHBRyz7UL1vL6wFUsxVXsrWPjVWetdsqtZyVk5NTx7durR1VVC06qJK8rUQR1ZPVGDOw0I9O4Ga3lhRAvUat7IjNJ2410/g1omAqOV/LDfeWLdUVwAc+sO217VwkxqGVxgwto6kAajVq4+P1e8qNNHqNKJh6dZSPV9rGxqaUQH5tq8tENvJ7NXOdMaavGU0FEFG5UVu8OGLJkimTy/h42s9DOSulcKh373phprV64+WGvNyz3333beWq1ljPNOmc0ysYM3TUUwC9cAJ3h2LIY87ixfDJT6aom/FxuPzytL9oUdqfPTst7DIxUd8JnC+fePrpKRy0GNlTdM4WyZ2z+bZ8+fTj228/ff/226eWaJw1a9soouIykcuXVw75bGSJx1qyGmOGl1raoV+2to0AKuUHqjYyyFM9l+9ZpBFTTLk3vnjxdDny74sWbStXpRFJI6anWjLX+p3sAzBmqGAkTUD1fAC1zC5jY1ONcTGlc7nhreeMrdRQj49PmZvKiiC/V56wrt6M5Fr7zeIoIGOGktFUABFTGUGLjVrR3l9vy9M9V7KvFxv/WuGjlRrqWukeyvJ2sxF2egVjho56CqDrM4FboaWZwOVlG/MJX+vWTdnJly5NPoBqVLLpF2fjjo3BmjXT7fONLE0Yka7JyWceR3hxdWNM2+jHmcCdJyLNis0XTI/M4bpuXWq081m19RrXfLZtfm7ZqZw3/sXjjTT+1RyuznFjjOkiw6kAakXp5I12nthtbKz6fQ45JPXOoXLDvXz51PG83loURxHlKB5H3RhjusxwKgCo3GM/9dSpHntEypGzbl0KD91tt6nzxsfhoIPg6qvh8MNTQ5033GNjsHXrVMO9YEHKw9OoTJWylDYSqmmMMW1meBVALVMLTG+M/+u/YP78VD42lsqPOGLqujytcp6WefnyZB7K98vJ1moxMTE9XXSjpiNjjGk3tTzE/bLNKAw0j6wp7xfPzT/LIaLlc1tNtmaMMT2AkZwJnPfu81TLkHrZS5akWcB5bvyi41VKEUNF8giinFmzKpuVbLoxxgwgw6kAINnlFy+eigSamIBLL00KYPPmZNdftmzK9JLb+Yvk6wXk5p16ZiVjjBkgerIkZFfIe/TStrH7K1emhnvVqqQkJifhP/4j2fN33x1e/Wq47LJ03SWXpBw9Rx6ZbP3FnD/FeQEeCRhjBozhnQiWU550VWbJkqm1eOfOhbvvnjpW3B8fT2al++/fdnJYI5O/jDGmy9SbCDa8IwCobLIpMj4+ZfcvjxRgeuOfjyaKCsAFJWUAAA8+SURBVLNSqKkxxgwIw+sDKE+62rq1+qSveg150Rk8MbGt3T/3MRhjzAAxvAqgGOef2/zXrZt+zqpVyRFcyQFcZOnS1OBPTsL551deeH3z5vrO4PLxATC/GWOGl9HwAQAcdliKAFqyJDXYy5YlBbBoERx6aPp+8MFp9m9O0QewZEn6/OQnpyaA5RRn9lZjYiIpCfsPjDFdYrR9ADDVKB95ZIr4yc0569bBLrvAi1+cnMTj43DeebDDDvDWt8LPf54a6b32Skohzxq6eHGaOfyIR0zVUa/xz5PTFSOGiuYpZ/00xvSCWrPE+mVraT2ASlRazGVsLGLLlqn8/2NjEQ89NH3FrnqrijWylrAXXjfGdBlGdj2AnHLvOm9+YWp9gJyxMVi9Gt797pT7J08pXSQ3E+VrASxfPpUk7uijp2YZV5Ol0joAxhjTAUZzPYCccsROBOyzTzLrQGrsi1x5ZWr8c6duMdUzJDPR1Vcn30CzSeE8i9gY02cMrw+gkt196VK4/fa0f8gh216z3Xbpc+lS+MQnYO+9tz1nfDyNDh54IN07v3959bDyqKNo8/csYmNMP1DLPtQvW8s+gEp29yVLIg46aHpZef+hh6qv+ZtnCJ2cnH5N7gOotpZvpxZe91q+xpgqUMcHMLwjAJjK41/ktNNSCOj69VNlz33u9P3tt0+fxTV/84lic+akz7I5Z8GC6T6BcnTPxMS22Udn2vN3aKkxZibU0g6d2oAjgf8GbgJOqnd+yyOAYrRPvuXRPuWtUvmWLdPvl/f889FAHv1TrqMb0T1lOSrtG2NGGuqMAHrR+D8C+AXwRGB74GrgwFrXtKQAig1iuYHOG/wlS2orgWoNadmcs3Xr9Ou61fg6tNQYU4N6CqAXUUCLgJsi4pcR8RDwFeCYttdSTAWxZs30Y7vtBmvXbpv87eqrp/IG1VqsvbisY0Qy+xTpVnRPtXWP7VA2xjRALxTAXsCvCvu3ZWXTkHS8pNWSVm/atKm1miYmUphmuYF+7WvTZ9mOn68VkNv8ay3WXrS55zb/ycnaiqPd5PUXcWipMaZBeqEAKnVPt2mxIuKMiFgYEQvnzZvXWk1577zcQH/yk8lpWy7PY/sjGlusvTjKyHve9RRHu+i18jHGDDy9iAK6DdinsL83sLEjNeUN9Pj49AY6YsrcUyyH6Q13Iw14J6J7GqGa8oHOKx9jzFDQCwVwJXCApCcAtwOvB97YdSmOOCKtG9yOhrt8Tbca314pH2PMUNB1E1BEbAFOAH4AbAC+GhHXdaiyqXw+xfz9q1al8jKD2HD2SvkYYwaenkwEi4gLgAs6XlHRLFJO27BypRtLY8xIM9zJ4KDybOA8MsizZY0xI8zwK4B8GccieQRQI8s4VqN8naNujDEDxnArgDwMdN266QvC5/utmoEqpZn2wvDGmAFjuBVArdnARx89fXGWRskdy60uDG+MMX3CcGcDhdQrn5zcdjZwvnhLsyOAWo5lh2AaYwaI4R4BQPXZwDOZMescPMaYIWD4FUAn0jU4B48xZggYfhMQtHfGbDkHj5d3NMYMKKOhAKB9M2adg8cYMyQoBsBssXDhwli9enWvxZhO2YHcikPZGGM6iKQ1EbGw2vHh9QF0eqKWc/AYYwac4VQAnqhljDF1GT4F4IlaxhjTEMPnBPZELWOMaYjhdQJHTE/1MDnpxt8YM1KMphPYE7WMMaYuw6cAvFi6McY0xHD6ADxRyxhj6jLcPgBP1DLGjDCj6QMAT9Qyxpg6DK8CMMYYUxMrAGOMGVGsAIwxZkSxAjDGmBFlIKKAJG0Cbmnx8rnA3W0Up9NY3s4zaDJb3s4yaPJC4zLvFxHzqh0cCAUwEyStrhUG1W9Y3s4zaDJb3s4yaPJC+2S2CcgYY0YUKwBjjBlRRkEBnNFrAZrE8naeQZPZ8naWQZMX2iTz0PsAjDHGVGYURgDGGGMqYAVgjDEjytAoAEk3S7pG0jpJ26QOVWKVpJskrZd0SC/kzGR5SiZnvj0gaVnpnCMk3V845+Quy3iWpLskXVso21nSjyTdmH3uVOXaIyX9d/Zbn9Rjmf9Z0g3Z3/ybkuZUubbm+9NFeSck3V74ux9V5dqu/8ZV5D2vIOvNktZVubYXv+8+kn4saYOk6yQtzcr78j2uIW/n3uGIGIoNuBmYW+P4UcD3AAGHAlf0WuZMrkcAvyZN2CiWHwF8p4dyPQc4BLi2UPYx4KTs+0nAR6s8zy+AJwLbA1cDB/ZQ5hcBj8y+f7SSzI28P12UdwJ4TwPvTNd/40rylo5/Aji5j37fPYBDsu87AP8DHNiv73ENeTv2Dg/NCKABjgG+FInLgTmS9ui1UMALgF9ERKsznTtCRFwK3FsqPgb4Yvb9i8ArKly6CLgpIn4ZEQ8BX8mu6ziVZI6IH0bElmz3cmDvbsjSCFV+40boyW9cS15JAl4LnNtpORolIu6IiLXZ9weBDcBe9Ol7XE3eTr7Dw6QAAvihpDWSjq9wfC/gV4X927KyXvN6qv/THCbpaknfk/S0bgpVhd0i4g5ILyuwa4Vz+vV3BngbaRRYiXrvTzc5IRvun1XFPNGPv/GzgTsj4sYqx3v6+0qaDzwDuIIBeI9L8hZp6zs8TEtCPjMiNkraFfiRpBuyHktOpRVhehoDK2l74Gjg7yscXksyC/0mswN/Czigm/K1SN/9zgCS3g9sAc6pckq996dbfAb4EOk3+xDJrPK20jn9+Bu/gdq9/579vpIeD3wdWBYRD6ixxaF69huX5S2Ut/0dHpoRQERszD7vAr5JGsIVuQ3Yp7C/N7CxO9JV5SXA2oi4s3wgIh6IiN9k3y8AtpM0t9sClrgzN5tln3dVOKfvfmdJxwIvA94UmbG0TAPvT1eIiDsjYmtETAKfrSJHX/3Gkh4JvAo4r9o5vfp9JW1HakzPiYhvZMV9+x5Xkbdj7/BQKABJj5O0Q/6d5DS5tnTa+cBblDgUuD8fBvaQqr0mSbtndlUkLSL9re7pomyVOB84Nvt+LPDtCudcCRwg6QnZCOf12XU9QdKRwHuBoyPid1XOaeT96Qolv9Qrq8jRV78x8ELghoi4rdLBXv2+2f/PmcCGiFhZONSX73E1eTv6DnfSq92tjeSpvzrbrgPen5W/E3hn9l3Av5A8+9cAC3ss82NJDfrsQllR3hOyZ7ma5Pg5vMvynQvcAfyJ1Bt6O7ALcCFwY/a5c3bunsAFhWuPIkUw/CL/W/RQ5ptIttx12favZZmrvT89kvfs7P1cT2pw9uiX37iSvFn5F/L3tnBuP/y+zyKZbdYX/v5H9et7XEPejr3DTgVhjDEjylCYgIwxxjSPFYAxxowoVgDGGDOiWAEYY8yIYgVgjDEjihWAaQhJW7Msg9dK+pqkx7b5/hdLqrnItaRlxXolXVAtM2KbZJon6QpJV0l6dunYdpI+kmWUvFbSzyW9pChXtr2ryTr3lPTvTV5zQpaxMoqTBbM5L3Uz4EpakGWRvCk7P59/8iilbJ83Zb/D/MI1x2bPfmM2SckMIFYAplF+HxFjEfF04CHSnIVus4w0fwKAiDgqIjZ3sL4XkCY4PSMiflI69iFS9sanZ7/Jy0kZHItyzQGaUgARsTEiXt2knD8lTcYqJxR8CSl9yAHA8aQ0E5X4THY8P/fIrPztwH0RsT9wKikTJZJ2BlYAi0mzTVdUyVlk+hwrANMKPwH2V8qr/q2sd3m5pIPg4Zz2Z0u6KOshHpeVHyHpO/lNJH1K0lvLN5f0GUmrlXKin5KVjZMmvvxY0o+zspvzHq+k5VlP/FplaytImq+UW/2z2b1+KOkxFerbT9KF2XNcKGlfSWOktMFHZSOfxxTOfyxwHLAkIv4ID6dw+GpJro8AT8qu/+fsNzmmcJ9zJB1dkmW+snz7kt4q6RuSvp/9jh+r9MeIiKsi4uYKh+pmwM32d4yIn0WaFPQlprJjFrNm/jvwgmx08GLgRxFxb0TcB/yITGlko6Lrs9/y45XkNf2DFYBpCqW8Ly8hzVY9BbgqIg4C3kdqPHIOAl4KHAacLGnPJqp5f0QszO7xXEkHRcQqUi6W50XE80oyLQD+itQjPRQ4TtIzssMHAP8SEU8DNgN/UaG+T5EayoNIibZWRcQ64GTgvGzk8/vC+fsDt0YhUVcVTiKl+h6LiL8FPpfJiaTZwOHABXXuMQa8Dvhz4HWS9qlzfpFGMlrulZVXOufh6yOlI76fNIu24n2zkcErgadlv+U/NiGr6QFWAKZRHqO02tNq4FZSzpJnkVIXEBEXAbtkDRvAtyPi9xFxN/Bjmkv+9VpJa4GrgKeRFsWoxbOAb0bEbyMl0PsGKT0xwP9mjTnAGmB+hesPA76cfT87u1/biYhLSCOnXUl5oL4eU3neq3FhRNwfEX8Argf2a6LKRjJa1jqn2rFq5Q8AfwA+J+lVQMW8NaZ/sAIwjZL7AMYiYkmkRTJqNR7lhiZIqWyL79yjyxdLegLwHuAFWS/yu5XOK19W49gfC9+30lgK9Hr5UW4C9lWWfKtJzgbeRBoJfL6B81uRP6eRjJa3MX2BkeI5D1+fjfxmkxaEqXjfTJktImWzfAXw/SZkNT3ACsDMhEtJjRmSjgDuLphFjpH0aEm7kJa3vJLkpDwwiy6ZTXKyltkR+C1wv6TdSOamnAfJHK0V5HiFpMcqZUJ8JclP0Sj/Rcr2SPY8l9U6OVJGxjOBVUqZIpG0h6S/LJ1aSd4vkJzZRMR1TcjYClUz4Ga+jr2y/QclHZrZ99/CVHbMYtbMVwMXZX6CHwAvkrRT5vx9EfADpTz2syOlL19GMl+ZPmaYFoQx3WcC+Lyk9aThfjEc8Oek3vu+wIciy1Uu6aukbIc3kkw804iIqyVdRcpo+EtShEvOGcD3JN1R9ANExFpJX8jqBPhcRFxVDFuswzhwlqS/BTaR2enr8A8kG/f1kv5AUlonl57lHkk/zZy634uIv42IOyVtIC3w0xYyB/nfAbsD6yVdEBHvIPkX8mySv2PK/zCL5MfIl3f8G5Jiegxptal8xakzgbMl3ZSd+/rsue6V9CGSUgf4YFa2B/BtSY8mjcpObNczms7gbKCm7UiaAH4TEY4CKZFFEF1DWvz7/h7J8HTgbRGxvBf1m/7BJiBjuoSkFwI3AJ/sVeMPEBHXuvE34BGAMcaMLB4BGGPMiGIFYIwxI4oVgDHGjChWAMYYM6JYARhjzIjy/wEbJr2me5xXnwAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Create a scatter plot of the data. To change the markers to red \"x\",\n",
    "# we used the 'marker' and 'c' parameters\n",
    "plt.scatter(x_train, y_train, marker='x', c='r') \n",
    "\n",
    "# Set the title\n",
    "plt.title(\"Profits vs. Population per city\")\n",
    "# Set the y-axis label\n",
    "plt.ylabel('Profit in $10,000')\n",
    "# Set the x-axis label\n",
    "plt.xlabel('Population of City in 10,000s')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Your goal is to build a linear regression model to fit this data.\n",
    "- With this model, you can then input a new city's population, and have the model estimate your restaurant's potential monthly profits for that city."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a name=\"4\"></a>\n",
    "## 4 - Refresher on linear regression\n",
    "\n",
    "In this practice lab, you will fit the linear regression parameters $(w,b)$ to your dataset.\n",
    "- The model function for linear regression, which is a function that maps from `x` (city population) to `y` (your restaurant's monthly profit for that city) is represented as \n",
    "    $$f_{w,b}(x) = wx + b$$\n",
    "    \n",
    "\n",
    "- To train a linear regression model, you want to find the best $(w,b)$ parameters that fit your dataset.  \n",
    "\n",
    "    - To compare how one choice of $(w,b)$ is better or worse than another choice, you can evaluate it with a cost function $J(w,b)$\n",
    "      - $J$ is a function of $(w,b)$. That is, the value of the cost $J(w,b)$ depends on the value of $(w,b)$.\n",
    "  \n",
    "    - The choice of $(w,b)$ that fits your data the best is the one that has the smallest cost $J(w,b)$.\n",
    "\n",
    "\n",
    "- To find the values $(w,b)$ that gets the smallest possible cost $J(w,b)$, you can use a method called **gradient descent**. \n",
    "  - With each step of gradient descent, your parameters $(w,b)$ come closer to the optimal values that will achieve the lowest cost $J(w,b)$.\n",
    "  \n",
    "\n",
    "- The trained linear regression model can then take the input feature $x$ (city population) and output a prediction $f_{w,b}(x)$ (predicted monthly profit for a restaurant in that city)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a name=\"5\"></a>\n",
    "## 5 - Compute Cost\n",
    "\n",
    "Gradient descent involves repeated steps to adjust the value of your parameter $(w,b)$ to gradually get a smaller and smaller cost $J(w,b)$.\n",
    "- At each step of gradient descent, it will be helpful for you to monitor your progress by computing the cost $J(w,b)$ as $(w,b)$ gets updated. \n",
    "- In this section, you will implement a function to calculate $J(w,b)$ so that you can check the progress of your gradient descent implementation.\n",
    "\n",
    "#### Cost function\n",
    "As you may recall from the lecture, for one variable, the cost function for linear regression $J(w,b)$ is defined as\n",
    "\n",
    "$$J(w,b) = \\frac{1}{2m} \\sum\\limits_{i = 0}^{m-1} (f_{w,b}(x^{(i)}) - y^{(i)})^2$$ \n",
    "\n",
    "- You can think of $f_{w,b}(x^{(i)})$ as the model's prediction of your restaurant's profit, as opposed to $y^{(i)}$, which is the actual profit that is recorded in the data.\n",
    "- $m$ is the number of training examples in the dataset\n",
    "\n",
    "#### Model prediction\n",
    "\n",
    "- For linear regression with one variable, the prediction of the model $f_{w,b}$ for an example $x^{(i)}$ is representented as:\n",
    "\n",
    "$$ f_{w,b}(x^{(i)}) = wx^{(i)} + b$$\n",
    "\n",
    "This is the equation for a line, with an intercept $b$ and a slope $w$\n",
    "\n",
    "#### Implementation\n",
    "\n",
    "Please complete the `compute_cost()` function below to compute the cost $J(w,b)$."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a name=\"ex01\"></a>\n",
    "### Exercise 1\n",
    "\n",
    "Complete the `compute_cost` below to:\n",
    "\n",
    "* Iterate over the training examples, and for each example, compute:\n",
    "    * The prediction of the model for that example \n",
    "    $$\n",
    "    f_{wb}(x^{(i)}) =  wx^{(i)} + b \n",
    "    $$\n",
    "   \n",
    "    * The cost for that example  $$cost^{(i)} =  (f_{wb} - y^{(i)})^2$$\n",
    "    \n",
    "\n",
    "* Return the total cost over all examples\n",
    "$$J(\\mathbf{w},b) = \\frac{1}{2m} \\sum\\limits_{i = 0}^{m-1} cost^{(i)}$$\n",
    "  * Here, $m$ is the number of training examples and $\\sum$ is the summation operator\n",
    "\n",
    "If you get stuck, you can check out the hints presented after the cell below to help you with the implementation."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "deletable": false
   },
   "outputs": [],
   "source": [
    "# UNQ_C1\n",
    "# GRADED FUNCTION: compute_cost\n",
    "\n",
    "def compute_cost(x, y, w, b): \n",
    "    \"\"\"\n",
    "    Computes the cost function for linear regression.\n",
    "    \n",
    "    Args:\n",
    "        x (ndarray): Shape (m,) Input to the model (Population of cities) \n",
    "        y (ndarray): Shape (m,) Label (Actual profits for the cities)\n",
    "        w, b (scalar): Parameters of the model\n",
    "    \n",
    "    Returns\n",
    "        total_cost (float): The cost of using w,b as the parameters for linear regression\n",
    "               to fit the data points in x and y\n",
    "    \"\"\"\n",
    "    # number of training examples\n",
    "    m = x.shape[0] \n",
    "    \n",
    "    # You need to return this variable correctly\n",
    "    total_cost = 0\n",
    "    \n",
    "    ### START CODE HERE ###  \n",
    "    # Variable to keep track of sum of cost from each example\n",
    "    cost_sum = 0\n",
    "    \n",
    "        # Loop over training examples\n",
    "    for i in range(m):\n",
    "            # Your code here to get the prediction f_wb for the ith example\n",
    "        f_wb = w * x[i] + b\n",
    "            # Your code here to get the cost associated with the ith example\n",
    "        cost = (f_wb - y[i]) ** 2\n",
    "        \n",
    "            # Add to sum of cost for each example\n",
    "        cost_sum = cost_sum + cost \n",
    "\n",
    "        # Get the total cost as the sum divided by (2*m)\n",
    "        total_cost = (1 / (2 * m)) * cost_sum\n",
    "    ### END CODE HERE ### \n",
    "\n",
    "    return total_cost"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<details>\n",
    "  <summary><font size=\"3\" color=\"darkgreen\"><b>Click for hints</b></font></summary>\n",
    "    \n",
    "    \n",
    "   * You can represent a summation operator eg: $h = \\sum\\limits_{i = 0}^{m-1} 2i$ in code as follows:\n",
    "     ```python \n",
    "    h = 0\n",
    "    for i in range(m):\n",
    "        h = h + 2*i\n",
    "    ```\n",
    "  \n",
    "   * In this case, you can iterate over all the examples in `x` using a for loop and add the `cost` from each iteration to a variable (`cost_sum`) initialized outside the loop.\n",
    "\n",
    "   * Then, you can return the `total_cost` as `cost_sum` divided by `2m`.\n",
    "     \n",
    "    <details>\n",
    "          <summary><font size=\"2\" color=\"darkblue\"><b> Click for more hints</b></font></summary>\n",
    "        \n",
    "    * Here's how you can structure the overall implementation for this function\n",
    "    ```python \n",
    "    def compute_cost(x, y, w, b):\n",
    "        # number of training examples\n",
    "        m = x.shape[0] \n",
    "    \n",
    "        # You need to return this variable correctly\n",
    "        total_cost = 0\n",
    "    \n",
    "        ### START CODE HERE ###  \n",
    "        # Variable to keep track of sum of cost from each example\n",
    "        cost_sum = 0\n",
    "    \n",
    "        # Loop over training examples\n",
    "        for i in range(m):\n",
    "            # Your code here to get the prediction f_wb for the ith example\n",
    "            f_wb = \n",
    "            # Your code here to get the cost associated with the ith example\n",
    "            cost = \n",
    "        \n",
    "            # Add to sum of cost for each example\n",
    "            cost_sum = cost_sum + cost \n",
    "\n",
    "        # Get the total cost as the sum divided by (2*m)\n",
    "        total_cost = (1 / (2 * m)) * cost_sum\n",
    "        ### END CODE HERE ### \n",
    "\n",
    "        return total_cost\n",
    "    ```\n",
    "    \n",
    "    If you're still stuck, you can check the hints presented below to figure out how to calculate `f_wb` and `cost`.\n",
    "    \n",
    "    <details>\n",
    "          <summary><font size=\"2\" color=\"darkblue\"><b>Hint to calculate f_wb</b></font></summary>\n",
    "           &emsp; &emsp; For scalars $a$, $b$ and $c$ (<code>x[i]</code>, <code>w</code> and <code>b</code> are all scalars), you can calculate the equation $h = ab + c$ in code as <code>h = a * b + c</code>\n",
    "          <details>\n",
    "              <summary><font size=\"2\" color=\"blue\"><b>&emsp; &emsp; More hints to calculate f</b></font></summary>\n",
    "               &emsp; &emsp; You can compute f_wb as <code>f_wb = w * x[i] + b </code>\n",
    "           </details>\n",
    "    </details>\n",
    "\n",
    "     <details>\n",
    "          <summary><font size=\"2\" color=\"darkblue\"><b>Hint to calculate cost</b></font></summary>\n",
    "          &emsp; &emsp; You can calculate the square of a variable z as z**2\n",
    "          <details>\n",
    "              <summary><font size=\"2\" color=\"blue\"><b>&emsp; &emsp; More hints to calculate cost</b></font></summary>\n",
    "              &emsp; &emsp; You can compute cost as <code>cost = (f_wb - y[i]) ** 2</code>\n",
    "          </details>\n",
    "    </details>\n",
    "        \n",
    "    </details>\n",
    "\n",
    "</details>\n",
    "\n",
    "    \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "You can check if your implementation was correct by running the following test code:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'numpy.float64'>\n",
      "Cost at initial w: 75.203\n",
      "\u001b[92mAll tests passed!\n"
     ]
    }
   ],
   "source": [
    "# Compute cost with some initial values for paramaters w, b\n",
    "initial_w = 2\n",
    "initial_b = 1\n",
    "\n",
    "cost = compute_cost(x_train, y_train, initial_w, initial_b)\n",
    "print(type(cost))\n",
    "print(f'Cost at initial w: {cost:.3f}')\n",
    "\n",
    "# Public tests\n",
    "from public_tests import *\n",
    "compute_cost_test(compute_cost)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Expected Output**:\n",
    "<table>\n",
    "  <tr>\n",
    "    <td> <b>Cost at initial w:<b> 75.203 </td> \n",
    "  </tr>\n",
    "</table>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a name=\"6\"></a>\n",
    "## 6 - Gradient descent \n",
    "\n",
    "In this section, you will implement the gradient for parameters $w, b$ for linear regression. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "As described in the lecture videos, the gradient descent algorithm is:\n",
    "\n",
    "$$\\begin{align*}& \\text{repeat until convergence:} \\; \\lbrace \\newline \\; & \\phantom {0000} b := b -  \\alpha \\frac{\\partial J(w,b)}{\\partial b} \\newline       \\; & \\phantom {0000} w := w -  \\alpha \\frac{\\partial J(w,b)}{\\partial w} \\tag{1}  \\; & \n",
    "\\newline & \\rbrace\\end{align*}$$\n",
    "\n",
    "where, parameters $w, b$ are both updated simultaniously and where  \n",
    "$$\n",
    "\\frac{\\partial J(w,b)}{\\partial b}  = \\frac{1}{m} \\sum\\limits_{i = 0}^{m-1} (f_{w,b}(x^{(i)}) - y^{(i)}) \\tag{2}\n",
    "$$\n",
    "$$\n",
    "\\frac{\\partial J(w,b)}{\\partial w}  = \\frac{1}{m} \\sum\\limits_{i = 0}^{m-1} (f_{w,b}(x^{(i)}) -y^{(i)})x^{(i)} \\tag{3}\n",
    "$$\n",
    "* m is the number of training examples in the dataset\n",
    "\n",
    "    \n",
    "*  $f_{w,b}(x^{(i)})$ is the model's prediction, while $y^{(i)}$, is the target value\n",
    "\n",
    "\n",
    "You will implement a function called `compute_gradient` which calculates $\\frac{\\partial J(w)}{\\partial w}$, $\\frac{\\partial J(w)}{\\partial b}$ "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a name=\"ex02\"></a>\n",
    "### Exercise 2\n",
    "\n",
    "Please complete the `compute_gradient` function to:\n",
    "\n",
    "* Iterate over the training examples, and for each example, compute:\n",
    "    * The prediction of the model for that example \n",
    "    $$\n",
    "    f_{wb}(x^{(i)}) =  wx^{(i)} + b \n",
    "    $$\n",
    "   \n",
    "    * The gradient for the parameters $w, b$ from that example \n",
    "        $$\n",
    "        \\frac{\\partial J(w,b)}{\\partial b}^{(i)}  =  (f_{w,b}(x^{(i)}) - y^{(i)}) \n",
    "        $$\n",
    "        $$\n",
    "        \\frac{\\partial J(w,b)}{\\partial w}^{(i)}  =  (f_{w,b}(x^{(i)}) -y^{(i)})x^{(i)} \n",
    "        $$\n",
    "    \n",
    "\n",
    "* Return the total gradient update from all the examples\n",
    "    $$\n",
    "    \\frac{\\partial J(w,b)}{\\partial b}  = \\frac{1}{m} \\sum\\limits_{i = 0}^{m-1} \\frac{\\partial J(w,b)}{\\partial b}^{(i)}\n",
    "    $$\n",
    "    \n",
    "    $$\n",
    "    \\frac{\\partial J(w,b)}{\\partial w}  = \\frac{1}{m} \\sum\\limits_{i = 0}^{m-1} \\frac{\\partial J(w,b)}{\\partial w}^{(i)} \n",
    "    $$\n",
    "  * Here, $m$ is the number of training examples and $\\sum$ is the summation operator\n",
    "\n",
    "If you get stuck, you can check out the hints presented after the cell below to help you with the implementation."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {
    "deletable": false
   },
   "outputs": [],
   "source": [
    "# UNQ_C2\n",
    "# GRADED FUNCTION: compute_gradient\n",
    "def compute_gradient(x, y, w, b): \n",
    "    \"\"\"\n",
    "    Computes the gradient for linear regression \n",
    "    Args:\n",
    "      x (ndarray): Shape (m,) Input to the model (Population of cities) \n",
    "      y (ndarray): Shape (m,) Label (Actual profits for the cities)\n",
    "      w, b (scalar): Parameters of the model  \n",
    "    Returns\n",
    "      dj_dw (scalar): The gradient of the cost w.r.t. the parameters w\n",
    "      dj_db (scalar): The gradient of the cost w.r.t. the parameter b     \n",
    "     \"\"\"\n",
    "    \n",
    "    # Number of training examples\n",
    "    m = x.shape[0]\n",
    "    \n",
    "    # You need to return the following variables correctly\n",
    "    dj_dw = 0\n",
    "    dj_db = 0\n",
    "    \n",
    "    ### START CODE HERE ### \n",
    "    for i in range(m):  \n",
    "     # Your code here to get prediction f_wb for the ith example\n",
    "     f_wb = f_wb = w * x[i] + b\n",
    "\n",
    "     # Your code here to get the gradient for w from the ith example \n",
    "     dj_dw_i = (f_wb - y[i]) * x[i]\n",
    "\n",
    "     # Your code here to get the gradient for b from the ith example \n",
    "     dj_db_i = f_wb - y[i]\n",
    "\n",
    "     # Update dj_db : In Python, a += 1  is the same as a = a + 1\n",
    "     dj_db += dj_db_i\n",
    "\n",
    "     # Update dj_dw\n",
    "     dj_dw += dj_dw_i\n",
    "\n",
    " # Divide both dj_dw and dj_db by m\n",
    "    dj_dw = dj_dw / m\n",
    "    dj_db = dj_db / m\n",
    "    ### END CODE HERE ### \n",
    "        \n",
    "    return dj_dw, dj_db"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<details>\n",
    "  <summary><font size=\"3\" color=\"darkgreen\"><b>Click for hints</b></font></summary>\n",
    "       \n",
    "    * You can represent a summation operator eg: $h = \\sum\\limits_{i = 0}^{m-1} 2i$ in code as follows:\n",
    "     ```python \n",
    "    h = 0\n",
    "    for i in range(m):\n",
    "        h = h + 2*i\n",
    "    ```\n",
    "    \n",
    "    * In this case, you can iterate over all the examples in `x` using a for loop and for each example, keep adding the gradient from that example to the variables `dj_dw` and `dj_db` which are initialized outside the loop. \n",
    "\n",
    "   * Then, you can return `dj_dw` and `dj_db` both divided by `m`.    \n",
    "    <details>\n",
    "          <summary><font size=\"2\" color=\"darkblue\"><b> Click for more hints</b></font></summary>\n",
    "        \n",
    "    * Here's how you can structure the overall implementation for this function\n",
    "    ```python \n",
    "    def compute_gradient(x, y, w, b): \n",
    "        \"\"\"\n",
    "        Computes the gradient for linear regression \n",
    "        Args:\n",
    "          x (ndarray): Shape (m,) Input to the model (Population of cities) \n",
    "          y (ndarray): Shape (m,) Label (Actual profits for the cities)\n",
    "          w, b (scalar): Parameters of the model  \n",
    "        Returns\n",
    "          dj_dw (scalar): The gradient of the cost w.r.t. the parameters w\n",
    "          dj_db (scalar): The gradient of the cost w.r.t. the parameter b     \n",
    "         \"\"\"\n",
    "    \n",
    "        # Number of training examples\n",
    "        m = x.shape[0]\n",
    "    \n",
    "        # You need to return the following variables correctly\n",
    "        dj_dw = 0\n",
    "        dj_db = 0\n",
    "    \n",
    "        ### START CODE HERE ### \n",
    "        # Loop over examples\n",
    "        for i in range(m):  \n",
    "            # Your code here to get prediction f_wb for the ith example\n",
    "            f_wb = \n",
    "            \n",
    "            # Your code here to get the gradient for w from the ith example \n",
    "            dj_dw_i = \n",
    "        \n",
    "            # Your code here to get the gradient for b from the ith example \n",
    "            dj_db_i = \n",
    "     \n",
    "            # Update dj_db : In Python, a += 1  is the same as a = a + 1\n",
    "            dj_db += dj_db_i\n",
    "        \n",
    "            # Update dj_dw\n",
    "            dj_dw += dj_dw_i\n",
    "    \n",
    "        # Divide both dj_dw and dj_db by m\n",
    "        dj_dw = dj_dw / m\n",
    "        dj_db = dj_db / m\n",
    "        ### END CODE HERE ### \n",
    "        \n",
    "        return dj_dw, dj_db\n",
    "    ```\n",
    "    \n",
    "    If you're still stuck, you can check the hints presented below to figure out how to calculate `f_wb` and `cost`.\n",
    "    \n",
    "    <details>\n",
    "          <summary><font size=\"2\" color=\"darkblue\"><b>Hint to calculate f_wb</b></font></summary>\n",
    "           &emsp; &emsp; You did this in the previous exercise! For scalars $a$, $b$ and $c$ (<code>x[i]</code>, <code>w</code> and <code>b</code> are all scalars), you can calculate the equation $h = ab + c$ in code as <code>h = a * b + c</code>\n",
    "          <details>\n",
    "              <summary><font size=\"2\" color=\"blue\"><b>&emsp; &emsp; More hints to calculate f</b></font></summary>\n",
    "               &emsp; &emsp; You can compute f_wb as <code>f_wb = w * x[i] + b </code>\n",
    "           </details>\n",
    "    </details>\n",
    "        \n",
    "    <details>\n",
    "          <summary><font size=\"2\" color=\"darkblue\"><b>Hint to calculate dj_dw_i</b></font></summary>\n",
    "           &emsp; &emsp; For scalars $a$, $b$ and $c$ (<code>f_wb</code>, <code>y[i]</code> and <code>x[i]</code> are all scalars), you can calculate the equation $h = (a - b)c$ in code as <code>h = (a-b)*c</code>\n",
    "          <details>\n",
    "              <summary><font size=\"2\" color=\"blue\"><b>&emsp; &emsp; More hints to calculate f</b></font></summary>\n",
    "               &emsp; &emsp; You can compute dj_dw_i as <code>dj_dw_i = (f_wb - y[i]) * x[i] </code>\n",
    "           </details>\n",
    "    </details>\n",
    "        \n",
    "    <details>\n",
    "          <summary><font size=\"2\" color=\"darkblue\"><b>Hint to calculate dj_db_i</b></font></summary>\n",
    "             &emsp; &emsp; You can compute dj_db_i as <code> dj_db_i = f_wb - y[i] </code>\n",
    "    </details>\n",
    "        \n",
    "    </details>\n",
    "\n",
    "</details>\n",
    "\n",
    "    \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Run the cells below to check your implementation of the `compute_gradient` function with two different initializations of the parameters $w$,$b$."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Gradient at initial w, b (zeros): -65.32884974555672 -5.83913505154639\n",
      "Using X with shape (4, 1)\n",
      "\u001b[92mAll tests passed!\n"
     ]
    }
   ],
   "source": [
    "# Compute and display gradient with w initialized to zeroes\n",
    "initial_w = 0\n",
    "initial_b = 0\n",
    "\n",
    "tmp_dj_dw, tmp_dj_db = compute_gradient(x_train, y_train, initial_w, initial_b)\n",
    "print('Gradient at initial w, b (zeros):', tmp_dj_dw, tmp_dj_db)\n",
    "\n",
    "compute_gradient_test(compute_gradient)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's run the gradient descent algorithm implemented above on our dataset.\n",
    "\n",
    "**Expected Output**:\n",
    "<table>\n",
    "  <tr>\n",
    "    <td> <b>Gradient at initial , b (zeros)<b></td>\n",
    "    <td> -65.32884975 -5.83913505154639</td> \n",
    "  </tr>\n",
    "</table>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Gradient at test w, b: -47.41610118114435 -4.007175051546391\n"
     ]
    }
   ],
   "source": [
    "# Compute and display cost and gradient with non-zero w\n",
    "test_w = 0.2\n",
    "test_b = 0.2\n",
    "tmp_dj_dw, tmp_dj_db = compute_gradient(x_train, y_train, test_w, test_b)\n",
    "\n",
    "print('Gradient at test w, b:', tmp_dj_dw, tmp_dj_db)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Expected Output**:\n",
    "<table>\n",
    "  <tr>\n",
    "    <td> <b>Gradient at test w<b></td>\n",
    "    <td> -47.41610118 -4.007175051546391</td> \n",
    "  </tr>\n",
    "</table>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a name=\"2.6\"></a>\n",
    "### 2.6 Learning parameters using batch gradient descent \n",
    "\n",
    "You will now find the optimal parameters of a linear regression model by using batch gradient descent. Recall batch refers to running all the examples in one iteration.\n",
    "- You don't need to implement anything for this part. Simply run the cells below. \n",
    "\n",
    "- A good way to verify that gradient descent is working correctly is to look\n",
    "at the value of $J(w,b)$ and check that it is decreasing with each step. \n",
    "\n",
    "- Assuming you have implemented the gradient and computed the cost correctly and you have an appropriate value for the learning rate alpha, $J(w,b)$ should never increase and should converge to a steady value by the end of the algorithm."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [],
   "source": [
    "def gradient_descent(x, y, w_in, b_in, cost_function, gradient_function, alpha, num_iters): \n",
    "    \"\"\"\n",
    "    Performs batch gradient descent to learn theta. Updates theta by taking \n",
    "    num_iters gradient steps with learning rate alpha\n",
    "    \n",
    "    Args:\n",
    "      x :    (ndarray): Shape (m,)\n",
    "      y :    (ndarray): Shape (m,)\n",
    "      w_in, b_in : (scalar) Initial values of parameters of the model\n",
    "      cost_function: function to compute cost\n",
    "      gradient_function: function to compute the gradient\n",
    "      alpha : (float) Learning rate\n",
    "      num_iters : (int) number of iterations to run gradient descent\n",
    "    Returns\n",
    "      w : (ndarray): Shape (1,) Updated values of parameters of the model after\n",
    "          running gradient descent\n",
    "      b : (scalar)                Updated value of parameter of the model after\n",
    "          running gradient descent\n",
    "    \"\"\"\n",
    "    \n",
    "    # number of training examples\n",
    "    m = len(x)\n",
    "    \n",
    "    # An array to store cost J and w's at each iteration — primarily for graphing later\n",
    "    J_history = []\n",
    "    w_history = []\n",
    "    w = copy.deepcopy(w_in)  #avoid modifying global w within function\n",
    "    b = b_in\n",
    "    \n",
    "    for i in range(num_iters):\n",
    "\n",
    "        # Calculate the gradient and update the parameters\n",
    "        dj_dw, dj_db = gradient_function(x, y, w, b )  \n",
    "\n",
    "        # Update Parameters using w, b, alpha and gradient\n",
    "        w = w - alpha * dj_dw               \n",
    "        b = b - alpha * dj_db               \n",
    "\n",
    "        # Save cost J at each iteration\n",
    "        if i<100000:      # prevent resource exhaustion \n",
    "            cost =  cost_function(x, y, w, b)\n",
    "            J_history.append(cost)\n",
    "\n",
    "        # Print cost every at intervals 10 times or as many iterations if < 10\n",
    "        if i% math.ceil(num_iters/10) == 0:\n",
    "            w_history.append(w)\n",
    "            print(f\"Iteration {i:4}: Cost {float(J_history[-1]):8.2f}   \")\n",
    "        \n",
    "    return w, b, J_history, w_history #return w and J,w history for graphing"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's run the gradient descent algorithm above to learn the parameters for our dataset."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Iteration    0: Cost     6.74   \n",
      "Iteration  150: Cost     5.31   \n",
      "Iteration  300: Cost     4.96   \n",
      "Iteration  450: Cost     4.76   \n",
      "Iteration  600: Cost     4.64   \n",
      "Iteration  750: Cost     4.57   \n",
      "Iteration  900: Cost     4.53   \n",
      "Iteration 1050: Cost     4.51   \n",
      "Iteration 1200: Cost     4.50   \n",
      "Iteration 1350: Cost     4.49   \n",
      "w,b found by gradient descent: 1.166362350335582 -3.63029143940436\n"
     ]
    }
   ],
   "source": [
    "# initialize fitting parameters. Recall that the shape of w is (n,)\n",
    "initial_w = 0.\n",
    "initial_b = 0.\n",
    "\n",
    "# some gradient descent settings\n",
    "iterations = 1500\n",
    "alpha = 0.01\n",
    "\n",
    "w,b,_,_ = gradient_descent(x_train ,y_train, initial_w, initial_b, \n",
    "                     compute_cost, compute_gradient, alpha, iterations)\n",
    "print(\"w,b found by gradient descent:\", w, b)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Expected Output**:\n",
    "<table>\n",
    "  <tr>\n",
    "    <td> <b> w, b found by gradient descent<b></td>\n",
    "    <td> 1.16636235 -3.63029143940436</td> \n",
    "  </tr>\n",
    "</table>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will now use the final parameters from gradient descent to plot the linear fit. \n",
    "\n",
    "Recall that we can get the prediction for a single example $f(x^{(i)})= wx^{(i)}+b$. \n",
    "\n",
    "To calculate the predictions on the entire dataset, we can loop through all the training examples and calculate the prediction for each example. This is shown in the code block below."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [],
   "source": [
    "m = x_train.shape[0]\n",
    "predicted = np.zeros(m)\n",
    "\n",
    "for i in range(m):\n",
    "    predicted[i] = w * x_train[i] + b"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will now plot the predicted values to see the linear fit."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0.5, 0, 'Population of City in 10,000s')"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Plot the linear fit\n",
    "plt.plot(x_train, predicted, c = \"b\")\n",
    "\n",
    "# Create a scatter plot of the data. \n",
    "plt.scatter(x_train, y_train, marker='x', c='r') \n",
    "\n",
    "# Set the title\n",
    "plt.title(\"Profits vs. Population per city\")\n",
    "# Set the y-axis label\n",
    "plt.ylabel('Profit in $10,000')\n",
    "# Set the x-axis label\n",
    "plt.xlabel('Population of City in 10,000s')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Your final values of $w,b$ can also be used to make predictions on profits. Let's predict what the profit would be in areas of 35,000 and 70,000 people. \n",
    "\n",
    "- The model takes in population of a city in 10,000s as input. \n",
    "\n",
    "- Therefore, 35,000 people can be translated into an input to the model as `np.array([3.5])`\n",
    "\n",
    "- Similarly, 70,000 people can be translated into an input to the model as `np.array([7.])`\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "deletable": false,
    "editable": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "For population = 35,000, we predict a profit of $4519.77\n",
      "For population = 70,000, we predict a profit of $45342.45\n"
     ]
    }
   ],
   "source": [
    "predict1 = 3.5 * w + b\n",
    "print('For population = 35,000, we predict a profit of $%.2f' % (predict1*10000))\n",
    "\n",
    "predict2 = 7.0 * w + b\n",
    "print('For population = 70,000, we predict a profit of $%.2f' % (predict2*10000))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Expected Output**:\n",
    "<table>\n",
    "  <tr>\n",
    "    <td> <b> For population = 35,000, we predict a profit of<b></td>\n",
    "    <td> $4519.77 </td> \n",
    "  </tr>\n",
    "  \n",
    "  <tr>\n",
    "    <td> <b> For population = 70,000, we predict a profit of<b></td>\n",
    "    <td> $45342.45 </td> \n",
    "  </tr>\n",
    "</table>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Congratulations on completing this practice lab on linear regression! Next week, you will create models to solve a different type of problem: classification. See you there!**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<details>\n",
    "  <summary><font size=\"2\" color=\"darkgreen\"><b>Please click here if you want to experiment with any of the non-graded code.</b></font></summary>\n",
    "    <p><i><b>Important Note: Please only do this when you've already passed the assignment to avoid problems with the autograder.</b></i>\n",
    "    <ol>\n",
    "        <li> On the notebook’s menu, click “View” > “Cell Toolbar” > “Edit Metadata”</li>\n",
    "        <li> Hit the “Edit Metadata” button next to the code cell which you want to lock/unlock</li>\n",
    "        <li> Set the attribute value for “editable” to:\n",
    "            <ul>\n",
    "                <li> “true” if you want to unlock it </li>\n",
    "                <li> “false” if you want to lock it </li>\n",
    "            </ul>\n",
    "        </li>\n",
    "        <li> On the notebook’s menu, click “View” > “Cell Toolbar” > “None” </li>\n",
    "    </ol>\n",
    "    <p> Here's a short demo of how to do the steps above: \n",
    "        <br>\n",
    "        <img src=\"output_640_16fps.gif\" align=\"center\">\n",
    "</details>"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
