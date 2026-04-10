Recipe Vault Documentation
==========================

Welcome to the **Recipe Vault** technical documentation.  This site is
generated automatically from the source code using `Sphinx
<https://www.sphinx-doc.org>`_ and published on `GitHub Pages
<https://pages.github.com>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   modules

Project Overview
----------------

Recipe Vault is a lightweight Flask web application that lets you store and
browse personal recipes.  Recipes are persisted to a local ``data.json`` file
so no database setup is required.

* **Home** ``/`` – browse all recipes sorted newest-first.
* **Add Recipe** ``/add`` – submit a new recipe via a web form.
* **Recipe Detail** ``/recipe/<id>`` – view the full details of a recipe.
* **Swagger UI** ``/apidocs/`` – interactive API documentation powered by
  Flasgger.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
