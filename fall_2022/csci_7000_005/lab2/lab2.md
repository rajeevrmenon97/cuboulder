# LAB 2 - Control Plane Experimentation

## Preparation

1. Either in CloudLab (single node) or a VM, install SEED emulator - see notes from class.

1. As prep, build and run the A00 experiment, and make sure you can interact with the environment - see notes from class.

1. As further prep, Walk through B04 - BGP hijacking example, which extends B00 - the mini Internet topology.  Perform the hijack as described in the README, and in class notes.

## Assignment

1. Create new topology for SEED
    It needs to be complex enough to show off the BGP hijacking and filtering.  It must not be an existing topology in the examples directory. Make sure you can ping from different hosts.

1. Perform a ping experiment - this will illustrate measuring downtime. 

    1. On base topology (before attack). Perform ping all to all. (capture data - timestamp, latency or failure)

    1. Modify the router config of the attacker to perform the attack.  Perform ping all to all, capture data.

    1. Modify the router config of the attacker's provider(s) to filter (defend against the attack).  perform ping all to all (capture data)

    1. Plot time on x-axis, latency of ping on y-axis, and for failed pings, plot a different mark with latency 0 (can be done with single point in gnu plot - https://stackoverflow.com/questions/19452516/add-a-single-point-at-an-existing-plot)

## Answer

1. Topology - [topology.py](topology.py)

1. Script to ping all hosts - [ping_all.py](ping_all.py)