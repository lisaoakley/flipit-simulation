## FlipIt Simulation

Simulation and strategy implementations for the discrete version of [FLIPIT: The Game of "Stealthy Takeover"](http://www.ccs.neu.edu/home/alina/papers/FlipIt.pdf) introduced by Marten van Dijk, Ari Juels, Alina Oprea, and Ronald L. Rivest.

Requirements:
[FlipIt Gym Environment](https://github.com/lisaoakley/gym-flipit)

[PyYaml](https://pypi.org/project/PyYAML/#description)

## How to Use
In `configs` directory, make a config file for experiment you want to run.

Run `python3 run.py 'configs/[config filename]'`

## Citing
Please cite the following paper:
```
@InProceedings{oakley2019qflip,
author="Oakley, Lisa and Oprea, Alina",
title="QFlip: An Adaptive Reinforcement Learning Strategy for the FlipIt Security Game",
booktitle="Proceedings of the 10th Conference on Decision and Game Theory for Security",
year="2019",
publisher="Springer International Publishing",
pages="364--384",
isbn="978-3-030-32430-8"
}
```
