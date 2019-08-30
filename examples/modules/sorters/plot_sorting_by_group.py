"""
Run spike sorting by property
=============================


"""

# TODO fix import
import spikeextractors as se
import spikeinterface.sorters as ss
import time

##############################################################################
# First, let's create a toy example:

##############################################################################
#  5) Spike sort by property
#  -------------------------
#  Sometimes, you might want to sort your data depending on a specific
#  property of your recording channels.
#  
#  For example, when using multiple tetrodes, a good idea is to sort each
#  tetrode separately. In this case, channels belonging to the same tetrode
#  will be in the same 'group'. Alternatively, for long silicon probes,
#  such as Neuropixels, you could sort different areas separately, for
#  example hippocampus and thalamus.
#  
#  All this can be done by sorting by 'property'. Properties can be loaded
#  to the recording channels either manually (using the
#  ``set_channel_property`` method, or by using a probe file. In this
#  example we will create a 16 channel recording and split it in four
#  tetrodes.


recording_tetrodes, sorting_true = se.example_datasets.toy_example(duration=60, num_channels=16)

# initially there is no group information
print(recording_tetrodes.get_shared_channel_property_names())

##############################################################################
# The file tetrode_16.prb contain the channel group description
# 
# .. parsed-literal::
# 
#     channel_groups = {
#         0: {
#             'channels': [0,1,2,3],
#         },
#         1: {
#             'channels': [4,5,6,7],
#         },
#         2: {
#             'channels': [8,9,10,11],
#         },
#         3: {
#             'channels': [12,13,14,15],
#         }
#     }

# load probe file to add group information
recording_tetrodes = se.load_probe_file(recording_tetrodes, 'tetrode_16.prb')
print(recording_tetrodes.get_shared_channel_property_names())

##############################################################################
# We can now use the launcher to spike sort by the property 'group'. The
# different groups can also be sorted in parallel, and the output sorting
# extractor will have the same property used for sorting. Running in
# parallel (in thread) can speed up the computations.

t_start = time.time()
sorting_tetrodes = ss.run_sorter('klusta', recording_tetrodes, output_folder='tmp_tetrodes',
                                 grouping_property='group', parallel=False)
print('Elapsed time: ', time.time() - t_start)

##############################################################################


t_start = time.time()
sorting_tetrodes_p = ss.run_sorter('klusta', recording_tetrodes, output_folder='tmp_tetrodes',
                                   grouping_property='group', parallel=True)
print('Elapsed time parallel: ', time.time() - t_start)

##############################################################################

print('Units non parallel: ', sorting_tetrodes.get_unit_ids())
print('Units parallel: ', sorting_tetrodes_p.get_unit_ids())

##############################################################################
#  Now that spike sorting is done, it's time to do some postprocessing,
#  comparison, and validation of the results!