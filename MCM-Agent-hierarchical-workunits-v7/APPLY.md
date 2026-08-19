# MCM-Agent recursive hierarchical work-unit patch

This overlay implements the next deterministic static stage:

- Event-State Interaction Graph;
- recursive HierarchicalWorkUnit construction;
- complexity + coupling driven partitioning;
- shared state/logic promotion to the parent;
- statement/state/event conservation ledger;
- physical child-module preservation;
- parent input with `umcm://<child-id>` replacement slots;
- `module-tree`, `module-stats`, and `module-plan` CLI via `mcm-plan`.

## Apply

From the root of `curious-whq/MCM-Agent`:

```bash
unzip MCM-Agent-hierarchical-workunits-v7-overlay.zip -d /tmp/mcm-hier
cp -a /tmp/mcm-hier/MCM-Agent-hierarchical-workunits-v7/. .
```

Then run:

```bash
python -m unittest tests.test_frontend_workunit -v
python -m unittest discover -s tests -p 'test_frontend*.py' -v
pip install -e .
```

Example:

```bash
mcm-plan module-tree design.fir --root-module BoomMSHR
mcm-plan module-stats design.fir --root-module LSU
mcm-plan module-plan design.fir --root-instance 'YOUR.CONCRETE.INSTANCE'
```

The old `mcm-static slice`, `instance-slice`, `route`, and handoff paths are not removed.
