readme.txt

For an end-user, this app should offer a Command Line Interface (CLI) to a simple Machine Learning App.

If you are the administrator, you should rely on Bash and Python to administer the app.

To install this app, follow the instructions listed below:

- Obtain a Linux host or Linux Virtual Machine.

- If you are familiar with VirtualBox, the ova-file listed below should provide a nice Linux Virtual Machine:
  - https://drive.google.com/file/d/0B32INV-pzunwazA4UDdLUjFVQjA/view?usp=sharing
  - After you boot the above machine, the password is 'a'
  - The above machine has Anaconda Python installed inside the ann account.

- If you want to use your own Linux host rather than the above Virtual Machine, I suggest you create an account called 'ann' and use that account to own the app.

- If you are new to Linux, I suggest you learn Linux as you learn about this app:
  - If you have Linux questions, get an account on StackOverflow, and ask questions.
  - Dont let lack of Linux knowledge slow you down as you wrestle with this app.

- After you login, you should see if Anaconda Python is installed already with this shell command:

    ~/anaconda3/bin/python

- If Anaconda is not installed, you should install it because this app depends on Anaconda:

    wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
    bash Anaconda3-4.2.0-Linux-x86_64.sh
    mv anaconda3/bin/curl anaconda3/bin/curl_ana
    echo 'export PATH=${HOME}/anaconda3/bin:$PATH' >> ~/.bashrc
    bash

- The next installation step is to git-clone this app.  If you have git installed the commands listed below should work okay:

    cd ~
    git clone https://github.com/danbikle/mlcl2.git

- If you don't have git installed, I suggest you install it with other useful packages you might need later:

    sudo apt-get update
    sudo apt-get upgrade

    sudo apt-get install gitk autoconf bison build-essential libssl-dev libyaml-dev \
    libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm3  sqlite3 curl   \
    libgdbm-dev libsqlite3-dev postgresql postgresql-server-dev-all aptitude r-base r-base-dev \
    libpq-dev emacs wget openssh-server ruby ruby-dev libbz2-dev linux-headers-$(uname -r)
    

- After you clone mlcl2 to ~/mlcl2 , you should consider this app to be installed.

- To operate the app just type in one shell command:

    ./slice_learn_predict.bash

If you have questions, find bugs or offer enhancements, e-me: bikle101@gmail.com
