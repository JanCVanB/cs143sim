cs143sim
========

Simulator for operation of an abstract communication network (Caltech CS/EE 143, Fall 2014)

Visit the documentation site `here <jvanbrug.github.io/cs143sim>`_!

Project Specifications
----------------------

Your group is tasked with creating a computer program that fits the descriptor of "abstract network simulator". From a high-level overview, this program should:

- Take as input a description of a network in a format of your choice.
- Run a simulation of the described network for a user-specified duration.
- Record data from user-specified simulation variables at regular intervals.
- Output graphs after each run showing the progression of the specified variables over time.

Ideally, you should be able to measure any simulation quantity you want; doing so will help you with the debugging process. However, there are a few metrics we are really interested in:

- Per-link buffer occupancy, packet loss, and flow rate.
- Per-flow send/receive rate and packet round-trip delay.
- Per-host send/receive rate.

For each of these, you should be able to produce both a time trace and an overall average.

Project Links
-------------

- `Course Website <http://courses.cms.caltech.edu/cs143/>`_
- `Project Description <http://courses.cms.caltech.edu/cs143/Project/NetworkSimGuidelines-2013-Rev2.pdf>`_
- `Test Cases <http://courses.cms.caltech.edu/cs143/Project/NetworkSimTestCases-2013-Rev4.pdf>`_
- `Project Tutorial <http://courses.cms.caltech.edu/cs143/Project/ProjectTutorial-2013-Rev1.pdf>`_
