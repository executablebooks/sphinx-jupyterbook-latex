# Configuration

The following configuration settings can be set in `conf.py` or `_config.yml` (jupyter-book)

For example, ensuring `sphinx.ext.imgconvert` doesn't get loaded you can use:

::::{grid} 2
:::{grid-item-card} Sphinx

Add the following to your `config.py` file:

```python
jb_load_imgconverter = False
```
:::

:::{grid-item-card} Jupyter Book

Adding the following to your `_config.yml` file:

```yaml
sphinx:
  config:
    jb_load_imgconverter: false
```
:::
::::

## jb_load_imgconverter

| Values |
|--------|
| *True* |
| False  |

Loads the [sphinx.ext.imgconverter](https://www.sphinx-doc.org/en/master/usage/extensions/imgconverter.html) extension which converts images in your document to an appropriate format for the builder (in this case when targeting `latex`)

```{warning}
This extension uses [ImageMagick](https://www.imagemagick.org/script/index.php) which needs to be installed on your system
```

## jblatex_show_tocs

| Values |
|--------|
| *True* |
| False  |
| 'list' |

This option enables the use of a `list` based implementation when building the `table of contents` for inclusion in the `pdf` document. This produces a clean looking table of contents for your project.

```{note}
This option is setup to enable `table of content` styles to be introduced in the future. Currently `True` is interpreted as `list` as the default behavior when building the `table of contents` in the `tex` file.
```


## jblatex_captions_parts

| Values |
|--------|
| *True* |
| False  |

This is an **override option** that ensures that `sphinx` is configured with:

```python
latex_toplevel_sectioning = 'part'
```

with behavior that is documented [here](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-latex_toplevel_sectioning). This `sphinx` option can be set to `part`, `chapter`, or `section`.

```{note}
This option is mainly useful when using this extension directly by a `sphinx`.
The value of this option is typically inferred when using `jupyter-book` from the `sitemap` and set automatically
```
