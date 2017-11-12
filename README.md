
This project contains python functions to creates and kill spot
requests. Persistence is guaranteed by cloning the image of the the instance
when it is killed. A better way to do this would be to mount a volume on start.

Inspired from
[Keras blog post](https://blog.keras.io/running-jupyter-notebooks-on-gpu-on-aws-a-starter-guide.html)

# Installation 

Requires `python3` and execute the following line in your favorite shell.

```{sh}
sudo pip3 install boto3 stormssh
```

Please configure `boto3` and `aws-cli` in general before.

# How TO

Use the script `make_spot_instance.py` to create a spot instance and configure
the `~/.ssh/config` file to allow simple connection. The script
`end_instance.py` will save the image on the machine, cancel the spot request
and terminate the instance.

# EC2 machine configuration

## SSL

```{sh}
mkdir ssl
cd ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout "cert.key" -out "cert.pem" -batch
```

If you use **emacs-ipython-notebook*, evaluate the following command

```{lisp}
(setq request-curl-options '("--insecure"))
```

# Add ssh key to available keys

```{sh}
NAME_PEM_FILE = "linux-key.pem"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/$NAME_PEM_FILE
```

# Jupyter

```{sh}
jupyter notebook --generate-config
```

## Packages to install for jupyter

This would allow to use the emacs keymaps for the notebook. This is not
compulsory with emacs ipython notebook.

```{sh}
sudo pip3 install jupyter-emacskeys
```

## Aws commands

```{sh}
mkdir notebooks
cd notebooks
jupyter notebook --port=8888
```

## Port redirection

```{sh}
ssh -L 8000:localhost:8888 ubuntu@IP_ADDRESS
```

## Password for jupyter folder

```{python}
c = get_config()  # get the config object
c.NotebookApp.certfile = u'/home/ubuntu/ssl/cert.pem' # path to the certificate we generated
c.NotebookApp.keyfile = u'/home/ubuntu/ssl/cert.key' # path to the certificate key we generated
c.IPKernelApp.pylab = 'inline'  # in-line figure when using Matplotlib
c.NotebookApp.ip = '*'  # serve the notebooks locally
c.NotebookApp.open_browser = False  # do not open a browser window by default when using notebooks
c.NotebookApp.password = 'sha1:a03a59943e29:361ebae216316c1f67eb96f8d6cbf5cb32daf535'
```

## Emacs IPython Notebook (EIN) configuration

Please evaluate the following command when you intend to ein

```{sh}
mkdir jupyter_security
sshfs aws:/run/user/1000/jupyter/ ~/jupyter_security
```

```{lisp}
(setq request-curl-options '("--insecure")) ;; allow unverified ssl
(setq ein:console-args '("--ssh" "aws" "--simple-prompt")) ;; the server
(setq ein:console-security-dir "~/jupyter_security") ;; the local folder where security files are forwarded
```


