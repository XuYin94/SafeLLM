"""Ravens cliport.tasks."""


from  cliport.tasks.packing_boxes import PackingBoxes
from  cliport.tasks.packing_shapes import PackingShapes
from  cliport.tasks.packing_boxes_pairs import PackingBoxesPairsSeenColors
from  cliport.tasks.packing_boxes_pairs import PackingBoxesPairsUnseenColors
from  cliport.tasks.packing_boxes_pairs import PackingBoxesPairsFull
from  cliport.tasks.packing_google_objects import PackingSeenGoogleObjectsSeq
from  cliport.tasks.packing_google_objects import PackingUnseenGoogleObjectsSeq
from  cliport.tasks.packing_google_objects import PackingSeenGoogleObjectsGroup
from  cliport.tasks.packing_google_objects import PackingUnseenGoogleObjectsGroup
from  cliport.tasks.place_red_in_green import PlaceRedInGreen
from  cliport.tasks.pick_and_place_primitive import PickAndPlacePrimitive
from  cliport.tasks.pick_and_place_primitive import PickAndPlacePrimitiveWithRelativePickPosition
from cliport.tasks.pack_google_object_primitive import PackingGoogleObjectsPrimitive,PackingGoogleObjectsRelativePrimitive
from cliport.tasks.pack_box_primitive import PackBoxPrimitive,PackBoxwithRelativePickPosition,PackBoxPrimitiveaAnomaly
from  cliport.tasks.put_block_in_bowl import PutBlockInBowlSeenColors
from  cliport.tasks.put_block_in_bowl import PutBlockInBowlUnseenColors
from  cliport.tasks.put_block_in_bowl import PutBlockInBowlFull
from  cliport.tasks.put_block_in_bowl import PutBlockInMatchingBowl
from  cliport.tasks.put_block_in_bowl import PutBlockInMismatchingBowl
from  cliport.tasks.put_block_in_bowl import PutAllBlockInABowl
from  cliport.tasks.put_block_in_bowl import PutAllBlockOnCorner
from  cliport.tasks.put_block_in_bowl import PutAllBlockInAZone
from  cliport.tasks.put_block_in_bowl import PickAndPlace
from  cliport.tasks.stack_block_pyramid import StackBlockPyramid
from  cliport.tasks.stack_block_pyramid_seq import StackBlockPyramidSeqSeenColors
from  cliport.tasks.stack_block_pyramid_seq import StackBlockPyramidSeqUnseenColors,StackBlockPyramidSeqUnseenColorswithrelativepickposition,StackBlockPyramidSeqUnseenColorsPrimitive
from  cliport.tasks.stack_block_pyramid_seq import StackBlockPyramidSeqFull
from  cliport.tasks.stack_block_pyramid_seq import StackBlockPyramidWithoutSeq
from  cliport.tasks.stack_block_pyramid_seq import StackAllBlock
from  cliport.tasks.stack_block_pyramid_seq import StackAllBlockInAZone
from  cliport.tasks.stack_block_pyramid_seq import StackAllBlockOfSameColor
from  cliport.tasks.stack_block_pyramid_seq import StackBlockWithAlternateColor
names = {
    # demo conditioned
    'packing-boxes': PackingBoxes,
    'place-red-in-green': PlaceRedInGreen,
    'stack-block-pyramid': StackBlockPyramid,
    'stack-block-pyramid-seq-seen-colors-relative-position':StackBlockPyramidSeqUnseenColorswithrelativepickposition,
    'stack-block-pyramid-seq-seen-colors-primitive': StackBlockPyramidSeqUnseenColorsPrimitive,
    'packing-shapes': PackingShapes,
    'packing-boxes-pairs-seen-colors': PackingBoxesPairsSeenColors,
    'packing-boxes-pairs-unseen-colors': PackingBoxesPairsUnseenColors,
    'packing-boxes-pairs-full': PackingBoxesPairsFull,
    'packing-seen-google-objects-seq': PackingSeenGoogleObjectsSeq,
    'packing-unseen-google-objects-seq': PackingUnseenGoogleObjectsSeq,
    'packing-seen-google-objects-group': PackingSeenGoogleObjectsGroup,
    'packing-unseen-google-objects-group': PackingUnseenGoogleObjectsGroup,
    'put-block-in-bowl-seen-colors': PutBlockInBowlSeenColors,
    'put-block-in-bowl-unseen-colors': PutBlockInBowlUnseenColors,
    'put-block-in-bowl-full': PutBlockInBowlFull,
    'put-block-in-matching-bowl': PutBlockInMatchingBowl,
    'put-block-in-mismatching-bowl': PutBlockInMismatchingBowl,
    'put-all-block-in-a-bowl': PutAllBlockInABowl,
    'put-all-block-on-corner': PutAllBlockOnCorner,
    'put-all-block-in-a-zone': PutAllBlockInAZone,
    'pick-and-place': PickAndPlace,
    'pick-and-place-primitive': PickAndPlacePrimitive,
    'pick-and-place-primitive-relative-pick-position':PickAndPlacePrimitiveWithRelativePickPosition,

    'stack-block-pyramid-seq-seen-colors': StackBlockPyramidSeqSeenColors,
    'stack-block-pyramid-seq-unseen-colors': StackBlockPyramidSeqUnseenColors,
    'stack-block-pyramid-seq-full': StackBlockPyramidSeqFull,
    'stack-block-pyramid-without-seq': StackBlockPyramidWithoutSeq,
    'stack-all-block': StackAllBlock,
    'stack-all-block-in-a-zone': StackAllBlockInAZone,
    'stack-all-block-of-same-color': StackAllBlockOfSameColor,
    'stack-block-with-alternate-color': StackBlockWithAlternateColor,
    'pack-box-primitive':PackBoxPrimitive,
    'pack-box-anomaly': PackBoxPrimitiveaAnomaly,
    'pack-box-primitive-relative-pick-position': PackBoxwithRelativePickPosition,
    'pack-google-object-primitive':PackingGoogleObjectsPrimitive,
    'pack-google-object-relative-primitive':PackingGoogleObjectsRelativePrimitive
}
