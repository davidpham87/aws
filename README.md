
This project contains python functions to creates and kill spot
requests. Persistence is guaranteed by cloning the image of the the instance
when it is killed. A better way to do this would be to mount a volume on start.

Inspired from
[Keras blog post](https://blog.keras.io/running-jupyter-notebooks-on-gpu-on-aws-a-starter-guide.html)

# SSL

```{sh}
mkdir ssl
cd ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout "cert.key" -out "cert.pem" -batch
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
