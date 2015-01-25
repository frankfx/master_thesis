#!/bin/bash
CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CURDIR/lib64/
export CSF_GraphicShr=$CURDIR/lib64/libTKOpenGl.so.7
$CURDIR/bin/TIGLViewer
