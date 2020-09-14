import os
import sys

cur_dir = os.path.dirname(__file__)
# /opt/trex/v2.75/automation/trex_control_plane/interactive
# /opt/trex/v2.75/trex_client/stf/examples
#
try:  # example is being run as "python -m trex.examples.stl.<example>"
    import trex.stl.api
except:  # run as standalone script "python <example>"
    trex_path = os.path.join(cur_dir, os.pardir, os.pardir, os.pardir)
    sys.path.insert(0, os.path.abspath(trex_path))

try:  # our usual repo
    # scripts_path = os.path.abspath(os.path.join(cur_dir, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir))
    # STL_PROFILES_PATH = os.path.join(scripts_path, 'stl')
    # EXT_LIBS_PATH = os.path.join(scripts_path, 'external_libs')
    #
    # assert os.path.isdir(STL_PROFILES_PATH)
    # assert os.path.isdir(EXT_LIBS_PATH)
    stl_path = os.path.join(0, '/opt/trex/v2.75/automation/trex_control_plane/interactive')
    sys.path.insert(0, os.path.abspath(stl_path))
    script_path = os.path.join(0, '/opt/trex/v2.75/trex_client/stf')
    sys.path.insert(0, os.path.abspath(script_path))
except:  # in client package
    # STL_PROFILES_PATH = os.path.abspath(os.path.join(cur_dir, os.pardir, os.pardir, os.pardir, 'profiles', 'stl'))
    # EXT_LIBS_PATH = os.path.join(cur_dir, os.pardir, os.pardir, os.pardir, os.pardir, 'external_libs')
    # client package path
    print('Error occurs when setting python environment variables')
#
# assert os.path.isdir(STL_PROFILES_PATH), 'Could not determine STL profiles path'
# assert os.path.isdir(EXT_LIBS_PATH), 'Could not determine external_libs path'
finally:
    # import sys
    # print sys.path
    pass
