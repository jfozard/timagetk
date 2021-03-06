# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       Copyright 2016 INRIA
#
#       File author(s):
#           Guillaume Baty <guillaume.baty@inria.fr>
#           Sophie Ribes <sophie.ribes@inria.fr>
#           Gregoire Malandain <gregoire.malandain@inria.fr>
#
#       See accompanying file LICENSE.txt
#------------------------------------------------------------------------------

#--- Aug. 2016
try:
    from timagetk.wrapping.clib import libvtexec, add_doc, return_value
    from timagetk.wrapping.vt_image import vt_image, new_vt_image
    from timagetk.components import SpatialImage
except ImportError:
    raise ImportError('Import Error')

__all__ = ['WATERSHED_DEFAULT', 'watershed']
WATERSHED_DEFAULT = '-labelchoice most'
WATERSHED_DEFAULT = ''


def watershed(image, seeds, param_str_1=WATERSHED_DEFAULT, param_str_2=None, dtype=None):
    """
    Seeded watershed algorithm.

    Parameters
    ----------
    :param *SpatialImage* image: *SpatialImage*, input image

    :param *SpatialImage* seeds: *SpatialImage*, seeds image, each marker have an unique value

    :param str param_str_1: WATERSHED_DEFAULT

    :param str param_str_2: optional, optional parameters

    :param *np.dtype* dtype: optional, output image type. By default, the output type is equal to the input type.

    Returns
    ----------
    :return: ``SpatialImage`` instance -- output image and metadata

    Example
    -------
    >>> from timagetk.util import data_path
    >>> from timagetk.components import imread
    >>> from timagetk.algorithms import linearfilter, regionalext, connexe, watershed
    >>> img_path = data_path('time_0_cut.inr')
    >>> input_image = imread(img_path)
    >>> smooth_img = linearfilter(input_image)
    >>> regext_img = regionalext(smooth_img)
    >>> conn_img = connexe(regext_img)
    >>> output_image = watershed(smooth_img, conn_img)
    """
    if isinstance(image, SpatialImage) and isinstance(seeds, SpatialImage):
        if dtype is None:
            dtype = seeds.dtype
        vt_img, vt_seeds, vt_res = vt_image(image), vt_image(seeds), new_vt_image(seeds, dtype=dtype)
        rvalue = libvtexec.API_watershed(vt_img.c_ptr, vt_seeds.c_ptr, vt_res.c_ptr,
                                         param_str_1, param_str_2)
        out_sp_img = return_value(vt_res.get_spatial_image(), rvalue)
        vt_img.free(), vt_seeds.free(), vt_res.free()
        return out_sp_img
    else:
        raise TypeError('Input images must be a SpatialImage')
        return
add_doc(watershed, libvtexec.API_Help_watershed)