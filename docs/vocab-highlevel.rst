High-Level Vocabulary
=====================

These methods abstract all of the API details from the interface, making it simple
to get and set the information you require. If you need more fine-grained control
of the calls, use the :doc:`vocab-lowerlevel` (of course, these
can be used interchangeably).

"Pull/Retrieve" Methods
-----------------------

.. automethod:: pyPrintful.pyPrintful.get_countries_list

.. automethod:: pyPrintful.pyPrintful.get_file_info

.. automethod:: pyPrintful.pyPrintful.get_file_list

.. automethod:: pyPrintful.pyPrintful.get_order_info

.. automethod:: pyPrintful.pyPrintful.get_order_list

.. automethod:: pyPrintful.pyPrintful.get_product_info

.. automethod:: pyPrintful.pyPrintful.get_product_list

.. automethod:: pyPrintful.pyPrintful.get_shippingrate_calc

.. automethod:: pyPrintful.pyPrintful.get_store_info

.. automethod:: pyPrintful.pyPrintful.get_syncproduct_info

.. automethod:: pyPrintful.pyPrintful.get_syncproduct_list

.. automethod:: pyPrintful.pyPrintful.get_syncvariant_info

.. automethod:: pyPrintful.pyPrintful.get_tax_calc

.. automethod:: pyPrintful.pyPrintful.get_tax_geos

.. automethod:: pyPrintful.pyPrintful.get_variant_info

.. automethod:: pyPrintful.pyPrintful.get_webhooks_info


"Push/Save" Methods
-------------------

.. automethod:: pyPrintful.pyPrintful.put_file_new

.. automethod:: pyPrintful.pyPrintful.put_order_cancel

.. automethod:: pyPrintful.pyPrintful.put_order_confirm

.. automethod:: pyPrintful.pyPrintful.put_order_new

.. automethod:: pyPrintful.pyPrintful.put_order_update

.. automethod:: pyPrintful.pyPrintful.put_store_packingslip

.. automethod:: pyPrintful.pyPrintful.put_syncproduct_remove

.. automethod:: pyPrintful.pyPrintful.put_webhooks_disable

.. automethod:: pyPrintful.pyPrintful.put_webhooks_update
