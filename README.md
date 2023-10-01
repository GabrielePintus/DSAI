# Data Science and Artificial Intelligence

Welcome to the homepage of the Master's Degree Program in [Data Science and Artificial Intelligence](https://dsai.units.it/) at UniTS. Hereafter you can find all the repositories of the courses.


## Courses

### First year

| Name | Repository |
| ---- | ---------- |
| Statistical Methods | [StatisticalMethods](https://github.com/GabrielePintus/StatisticalMethods) |
| Machine Learning Operations | [MachineLearningOperations](https://github.com/GabrielePintus/MachineLearningOperations) |
| High Performance and Cloud Computing | [HighPerformanceCloudComputing](https://github.com/GabrielePintus/HighPerformanceCloudComputing.git) |
| Global Multiobjective Optimization | [GlobalMultiobjectiveOptimization](https://github.com/GabrielePintus/GlobalMultiobjectiveOptimization) |

## How to use DSAI repository on your computer
## Using a lot of git commands (classic way)
1. Clone the DSAI repository on your computer using the following command (ignore the empty directories such as "StatisticalMethods"):
```
git clone https://github.com/GabrielePintus/DSAI
```
2. Clone all the other repositories (outside of the DSAI repository), for example: 
```
git clone https://github.com/GabrielePintus/StatisticalMethods
```
3. Use all these repo directories as usual (git status, commit, push, etc.)
You should have obtained a tree like this:
```
.
├── Desktop
│   └── DSAI
│       ├── README.md
│       ├── StatisticalMethods
│       │   HighPerformanceComputing
│       │   GlobalMultiobjectiveOptimization
...
...
│   └── StatisticalMethods
│       ├── README.md
│       ├── Slides
...
...
│   └── HighPerformanceComputing
│       ├── README.md
│       ├── Notes
...
...
```
Notice that the directories for the courses inside the DSAI repository are empty. Do you want to have all the content under the DSAI repository? Then you have to use git submodules (see below).

## Git Submodules (tricky but useful)
Git submodules are a way to "keep a Git repository in another Git repository". A repo that cointains submodules has a file called ".gitmodules" that contains a list of the submodules and their URLs.
Submodules can be seen as a pointer (a reference) to a **specific commit** of another repository.

### How to clone the DSAI repository
If you cloned the DSAI repository with "git clone <repo-URL>" you would notice that the submodules are empty. This is because the submodules are not cloned by default. To clone the submodules you have to run the following command:
```
git clone --recurse-submodules --remote-submodules <repo-URL>
```
The "--recurse-submodules" option will clone the submodules and the "--remote-submodules" option will clone the submodules from the remote repository instead of using the local ones.
In other words, "--recurse-submodules" will fill the directories of the submodules which are empty while "--remote-submodules" says to use the latest commit of the submodules from the remote repository instead of using the commit we are pointing at.

### How to "update" the DSAI repository
As always to pull the latest changes from the remote repository you have to run the following command:
```
git pull
```
But this command will not update the submodules (the pointers to the commits of the other repos will not be updated). To update the submodules you have to run the following command:
```
git submodule update --remote
```
### What happens when I modify a submodule?
If you modify a submodule you have to commit and push the changes to the remote repository of the submodule. Then you have to commit and push the changes of the main repository (the one that contains the submodule) to the remote repository of the main repository. In this way, the pointer to the commit of the submodule will be updated.
Practically:
1. You have modified a submodule
2. You commit and push the changes of the submodule to the remote repository of the submodule using the following commands (inside the submodule directory):
```
git add <file>
git commit -m "message"
git push
```
3. You commit and push the changes of the main repository to the remote repository of the main repository using the following commands (inside the main repository directory):
```
git add <file>
git commit -m "message"
git push
```

### How do I add a new submodule (you shouldn't need this)
To add a new submodule you have to run the following command:
```
git submodule add <repo-URL> <directory>
```
where <repo-URL> is the URL of the repository you want to add as a submodule and <directory> is the directory where you want to put the submodule. For example:
```
git submodule add https://github.com/GabrielePintus/StatisticalMethods StatisticalMethods
```
This command will create a new directory called "StatisticalMethods" and will put the submodule inside it. Then you have to commit and push the changes of the main repository to the remote repository of the main repository using the following commands (inside the main repository directory):
```
git add <file>
git commit -m "message"
git push
```