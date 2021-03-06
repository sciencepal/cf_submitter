**Objective**

Create a command line problem submitter for codeforces.com contests (cf rounds)


**Steps to install**

1. Clone repo to local (say, /opt/cf_submitter)
2. Go to Firefox browser
3. Login/Relogin to codeforces and check option for Remember me for a month
4. Go to http://codeforces.com and Inspect Element in browser
5. Search all these parameters separately : **bfaa**, **_tta**, **csrf_token**
6. Substitute values at the beginning of the script
7. Substitute locations of cookie file etc in script (changes needed are documented in script)

**Additional steps for ease of access**

7. Open terminal and open **~/.bashrc** in the editor of your choice
8. Go to end of file and type the following:
    **alias cf="python3 /opt/cf_submitter/cf_submitter.py"** //or your location of the file
9. Save and exit
8. In command line type **source ~/.bashrc** .

**Steps to run**

1. Everytime you register for a contest, copy the contest URL and perform step 2
2. In Command Line, type **cf <contest_link>**. This sets contest and cookies
3. If you write all codes in the same file (like me), set the path of that file in the script.
    Type **python3 /opt/cf_submitter/cf_submitter.py <problem_code>** in terminal.
    (eg. 'python3 /opt/cf_submitter/cf_submitter.py A' submits solution to problem A).
    If you have followed the optional ease of access steps, the same can be achieved by typing only 
    **cf A** in terminal
4. Else you can specify the file path of your solution file as a parameter like : 
    **python3 /opt/cf_submitter/cf_submitter.py <problem_code> <sol_file_path>**
    If you have followed the optional ease of access steps, the same can be achieved by typing
    **cf A <sol_file_path>** in terminal.
    
**Requirements**

python3, 
sqlite3, 
pickle, 
python3-bs4 Beautifulsoup
