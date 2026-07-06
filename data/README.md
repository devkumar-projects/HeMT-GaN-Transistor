# Data directory

No raw numerical result tables were present in the supplied archive, so this
repository does not fabricate them. Place new machine-readable exports here
or under a versioned experiment directory.

Recommended columns include explicit units, for example:

```text
gate_voltage_V,drain_voltage_V,source_current_A_per_cm,drain_current_A_per_cm,newton_iterations,residual
```

Every export should identify the Git commit, deck revision, Ecorce version,
mesh statistics, physical models, temperature, terminal mapping and implicit
out-of-plane depth.
