.. ARgorithmToolkit documentation master file, created by
   sphinx-quickstart on Sat Dec 26 13:11:39 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


ARgorithm
=========

The ARgorithm project provides an interface to render your algorithms
and data structures in augmented reality. The ARgorithmToolkit package
offers packages and a command line interface needed to make and submit
algorithms for the following.

.. toctree::
    :maxdepth: 2
    :caption: Contents:
    
    Understanding modules <modules>
    Need help? <help>
    License <license>


How does it work ?
~~~~~~~~~~~~~~~~~~

The Toolkit package is for developers who want to transport their own
algorithms into augmented reality. The toolkit provides you with a
**template library** which works just like your usual template library
except this one records **states** . Each state is an event that occurs
in your data structure and by keeping track of the states of your
variables , data structures etc we then render them in augmented
reality.

Getting started
~~~~~~~~~~~~~~~

You can install the ARgorithmToolkit using pip

.. code:: shell

    pip install ARgorithmToolkit

or you can clone the repo

.. code:: bash

    git clone https://github.com/ARgorithm/Toolkit.git 
    cd Toolkit
    make init

This will also setup ARgorithm on your command line

.. code:: bash

    user@pc:~$  ARgorithm -h
    usage: ARgorithm [-h] {init,submit,test,delete,account} ...

    ARgorithm CLI

    optional arguments:
      -h, --help            show this help message and exit

    command:
      {init,submit,test,delete,account}
                            try command --help for more details

After that you can get started with your own ARgorithm

.. code:: bash

    ARgorithm init

This will generate your ``.py`` file and your ``.config.json`` file.

1. The ``<name>.py`` file will store your code that you will submit to
   the server hosting all ARgorithms
2. The ``<name>.config.json`` stores important details about your
   ARgorithm such as its purpose and parameters required

The ``<name>.py`` file initially looks like this

.. code:: python

    import ARgorithmToolkit

    def run(**kwargs):
        stateset = ARgorithmToolkit.StateSet()
        
        #
        #   Your code
        #
        
        return

You can add whatever code you want to this file using all the tools and
classes present in ARgorithmToolkit but be sure to

1. Your file should have one function which takes ``**kwargs`` input
   (refer
   `here <https://book.pythontips.com/en/latest/args_and_kwargs.html>`__
   to know more about kwargs) that will should perform whatever you
   desire and should return the stateset. You can check out later in the
   document on how to use this stateset
2. you can create classes and additional functions in your code. Support
   for importing external modules is not yet added so its advisable not
   to add those.

the ``<name>.config.json`` file is a JSON file storing all the metadata

.. code:: json

    {
        "argorithmID" : "<name>",
        "file" : "<name>.py",
        "function" : "<function to be called>",
        "parameters" : {
            "variable-name" : "<data-type>"
        } , 
        "default" : {
            "variable-name" : "<value>"
        },
        "description" : "Tell us about your ARgorithm"
    }

+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Key           | Description                                                                                                                                                                                                   |
+===============+===============================================================================================================================================================================================================+
| argorithmID   | name of your ARgorithm , this is generally pre filled from when you run the init command. The name of your code file should be *name*.py and the config should be *name*.config.json. [will be fixed later]   |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| file          | The file containing your codefile                                                                                                                                                                             |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| function      | The function that is going to be called                                                                                                                                                                       |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| parameters    | the parameters that your ARgorithm would need, this helps in anyone using your ARgorithm to understand what is the input format                                                                               |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| default       | default parameters in case no parameters are passed                                                                                                                                                           |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| description   | The description of ARgorithm. Helpful to people using your ARgorithm as well as other developers                                                                                                              |
+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

You can check out ARgorithm examples in our Github Repo

Once you are done , you can submit to server by running

.. code:: bash

    ARgorithm submit

or

.. code:: bash

    ARgorithm submit --name <name>

you can test your ARgorithm submission by using

.. code:: bash

    ARgorithm test

you can delete your ARgorithm submission by using

::

    ARgorithm delete

If the server need authentication for any action , you will be prompted
for it. If you do not have a account on the server then you can register
using

::

    ARgorithm account new

you can login using

::

    ARgorithm account login

The access token generated during login stays in your system till it
expires so you dont have to login again and again. In case the token
expires or is invalid , you will be prompted to login again.

you can use the ``-o`` or ``--overwrite`` flag to overwrite a
pre-existing login

*if running server image on local machine , add **-l** or **--local**
flag in the ``submit``,\ ``delete`` , ``account``\ and ``test`` commands
. To run the server locally , pull the docker image*
``alanjohn/argorithm-server:latest`` *and run it. Check out server repo
`here <https://github.com/ARgorithm/Server>`__*

Using ARgorithmToolkit
----------------------

ARgorithmToolkit adds a few extra steps when it comes to initializing
instances whose states you want to record but thats because a lot of
data has to be maintained in order for smooth transitions

.. code:: python

    >>> import ARgorithmToolkit
    >>> algo = ARgorithmToolkit.StateSet()
    >>> x = ARgorithmToolkit.Variable('x',algo,0,comments='Our first variable')
    >>> x.value
    0
    >>> x.value += 10
    >>> x.value
    10
    >>> print(algo)
    {'state_type': 'variable_declare', 'state_def': {'variable_name': 'x', 'value': 0}, 'comments': 'Our first variable'}
    {'state_type': 'variable_highlight', 'state_def': {'variable_name': 'x', 'value': 10}, 'comments': ''}

As ARgorithm is tool for creating visual demonstration , you can add
comments parameter to most functions. These comments get included in
states and get featured as text when that state is rendered in AR.

Make sure you make the objects you want to keep track of as part of the
same stateset. Each object is instantiated with a **name** this is
important to identify arrays when rendering them

You can refer the docs and samples in the
`repo <https://github.com/ARgorithm/Toolkit>`__ to understand more
clearly.

StateSet
--------

The core class to all algorithm and data structures in ARgorithmToolkit
You will always need to declare this and use this when using different
ARgorithmToolkit features. This is where the states are stored that
later get rendered to ARgorithm App. So obviously all your ARgorithms
are supposed to return this

You wont have it to interact with it much other than while initialising
objects and returning results. It has a ``add_comment`` method that
allows you to create blank states carrying description in the form of
comments that you might want to show to the client while the ARgorithm
is being rendered. This will prove handy when creating good
demonstrations

.. code:: python

    >>> import ARgorithmToolkit
    >>> algo = ARgorithmToolkit.StateSet()
    >>> algo.add_comment("Hello world")
    >>> print(algo)
    {'state_type': 'comment', 'state_def': None, 'comments': 'Hello world'}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`