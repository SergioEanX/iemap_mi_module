## Notes

To update the Pypi module, run the following command:

```bash
poetry build
poetry publish
```

**Warning: Remember to update `version` in `pyproject.toml` and `__init__.py` files before issuing previous commands!!!
**   
**Otherwise, the module will not be updated.**