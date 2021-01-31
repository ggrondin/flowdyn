# Changelog & Release Notes

## Upgrading

To upgrade to the latest version of `flowdyn` use `pip`:

```bash
pip install flowdyn --upgrade
```

You can determine your currently installed version using this command:

```bash
pip show flowdyn
```

## Versions

### [1.x.x](https://pypi.org/project/flowdyn/) (2021-xx-xx)

#### changed

- avoid warnings with `vanalbada` and `vanleer` limiters when uniform flows
- analytical 1D solution for nozzle flows in `solution.euler_nozzle`
- improve test coverage
- optimize some mesh computation

#### fixed

### [1.0.1](https://pypi.org/project/flowdyn/) (2021-01-29)

#### fixed

- fix computation of `modelphy.euler` supersonic inlet condition 

### [1.0.0](https://pypi.org/project/flowdyn/) (2021-01-27)

- models: convection, Burgers, Euler and derived (nozzle)
- Finite Volume method for 1d mesh
- numerical methods: linear 1st to 3rd order extrapolation ; MUSCL method and associated limiters
- integrators: explicit, Runge-Kutta, implicit
