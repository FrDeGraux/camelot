#  ============================================================================
#
#  Copyright (C) 2007-2016 Conceptive Engineering bvba.
#  www.conceptive.be / info@conceptive.be
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of Conceptive Engineering nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  ============================================================================

import six

from ....core.item_model import PreviewRole
from ....core.qt import py_to_variant
from .customdelegate import CustomDelegate

from .. import editors

class ManyToOneChoicesDelegate( CustomDelegate ):
    """Display a ManyToOne or a relationship field as a ComboBox, filling the 
  list of choices with the objects of the target class.   This delegate will
  not work on non relationship fields.
  
  .. image:: /_static/enumeration.png
  
  The items in the ComboBox are the unicode representation of the related objects.
  So these classes need an implementation of their __unicode__ method to show
  up in a human readable way in the ComboBox.
  """
  
    editor = editors.OneToManyChoicesEditor

    @classmethod
    def get_standard_item(cls, locale, value, fa_values):
        item = super(ManyToOneChoicesDelegate, cls).get_standard_item(locale, value, fa_values)
        if value is not None:
            item.setData(py_to_variant(six.text_type(value)), PreviewRole)
        return item