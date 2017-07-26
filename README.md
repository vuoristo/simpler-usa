# Simpler universe-starter-agent

The codebase implements an agent that can solve a number of `gym` environments. It is based on [universe-starter-agent](https://github.com/openai/universe-starter-agent).
It contains a basic implementation of the [A3C algorithm](https://arxiv.org/abs/1602.01783), adapted for real-time environments.

# Dependencies

* Python 2.7 or 3.5
* [six](https://pypi.python.org/pypi/six) (for py2/3 compatibility)
* [TensorFlow](https://www.tensorflow.org/) >=1.0
* [tmux](https://tmux.github.io/) (the start script opens up a tmux session with multiple windows)
* [htop](https://hisham.hm/htop/) (shown in one of the tmux windows)
* [gym](https://pypi.python.org/pypi/gym)
* gym[atari]
* [opencv-python](https://pypi.python.org/pypi/opencv-python)
* [numpy](https://pypi.python.org/pypi/numpy)
* [scipy](https://pypi.python.org/pypi/scipy)

# Differences to universe-starter-agent

* No universe environments. Supporting universe adds complexity and slows down experimentation with simpler Atari or other environments.
* Collect hyperparameters to cli arguments.
* No support for tf == 0.12
* Style changed to closer match PEP 8

# Getting Started

```
conda create --name universe-starter-agent python=3.5
source activate universe-starter-agent

brew install tmux htop cmake     # On Linux use sudo apt-get install -y tmux htop cmake golang libjpeg-dev

pip install "gym[atari]"
pip install six
pip install tensorflow
conda install -y -c https://conda.binstar.org/menpo opencv3
conda install -y numpy
conda install -y scipy
```


Add the following to your `.bashrc` so that you'll have the correct environment when the `train.py` script spawns new bash shells
```source activate universe-starter-agent```

## Atari Pong

`python train.py --num-workers 2 --env-id PongDeterministic-v4 --log-dir /tmp/pong`

The command above will train an agent on Atari Pong using ALE simulator.
It will see two workers that will be learning in parallel (`--num-workers` flag) and will output intermediate results into given directory.

The code will launch the following processes:
* worker-0 - a process that runs policy gradient
* worker-1 - a process identical to process-1, that uses different random noise from the environment
* ps - the parameter server, which synchronizes the parameters among the different workers
* tb - a tensorboard process for convenient display of the statistics of learning

Once you start the training process, it will create a tmux session with a window for each of these processes. You can connect to them by typing `tmux a` in the console.
Once in the tmux session, you can see all your windows with `ctrl-b w`.
To switch to window number 0, type: `ctrl-b 0`. Look up tmux documentation for more commands.

To access TensorBoard to see various monitoring metrics of the agent, open [http://localhost:12345/](http://localhost:12345/) in a browser.

Using 16 workers, the agent should be able to solve `PongDeterministic-v4` within 30 minutes (often less) on an `m4.10xlarge` instance.
Using 32 workers, the agent is able to solve the same environment in 10 minutes on an `m4.16xlarge` instance.
If you run this experiment on a high-end MacBook Pro, the above job will take just under 2 hours to solve Pong.

Add '--visualise' toggle if you want to visualise the worker using env.render() as follows:

`python train.py --num-workers 2 --env-id PongDeterministic-v4 --log-dir /tmp/pong --visualise`

![pong](https://github.com/vuoristo/simpler-usa/raw/master/imgs/tb_pong.png "Pong")

For best performance, it is recommended for the number of workers to not exceed available number of CPU cores.

You can stop the experiment with `tmux kill-session` command.

# TODOs:

* Move rest of the hyperparameters to arguments
* Clean up train.py
