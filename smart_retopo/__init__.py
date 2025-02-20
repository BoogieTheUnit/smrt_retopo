bl_info = {
    "name": "SMRT Retopo",
    "author": "BoogieTheUnit",
    "version": (1, 1, 0),
    "blender": (4, 2, 4),
    "location": "View3D > Tool Shelf",
    "description": "Automatic even retopology with preprocessing and quad reduction",
    "category": "Mesh",
}

import bpy
from .retopo import (
    SmartRetopoQuadriFlowOperator,
    SmartRetopoVoxelRemeshOperator,
    ResetSmartRetopoSettingsOperator,
    preprocess_mesh,
    apply_symmetry,
    enhance_curvature,
)
from .ui import SmartRetopoPanel


# Property Group for Addon Settings
class SmartRetopoSettings(bpy.types.PropertyGroup):
    target_count: bpy.props.IntProperty(
        name="Target Quad Count",
        default=5000,
        min=100,
        max=100000,
        description="Desired number of quads for retopology"
    )
    adaptive_size: bpy.props.FloatProperty(
        name="Adaptive Size",
        default=50.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE',
        description="Control local quad size adaptation based on mesh curvature"
    )
    quad_density: bpy.props.FloatProperty(
        name="Quad Density",
        default=1.0,
        min=0.1,
        max=5.0,
        description="Adjust the density of quads in painted regions"
    )
    detect_hard_edges: bpy.props.BoolProperty(
        name="Detect Hard Edges",
        default=False,
        description="Automatically detect and preserve hard edges"
    )
    hard_edge_angle: bpy.props.FloatProperty(
        name="Hard Edge Angle",
        default=30.0,
        min=0.0,
        max=180.0,
        description="Angle threshold for detecting hard edges"
    )
    symmetry_x: bpy.props.BoolProperty(
        name="Symmetry X",
        default=False,
        description="Enable symmetry along the X axis"
    )
    symmetry_y: bpy.props.BoolProperty(
        name="Symmetry Y",
        default=False,
        description="Enable symmetry along the Y axis"
    )
    symmetry_z: bpy.props.BoolProperty(
        name="Symmetry Z",
        default=False,
        description="Enable symmetry along the Z axis"
    )


# Registration Functions
def register():
    bpy.utils.register_class(SmartRetopoSettings)
    bpy.types.Scene.smart_retopo = bpy.props.PointerProperty(type=SmartRetopoSettings)
    bpy.utils.register_class(SmartRetopoQuadriFlowOperator)
    bpy.utils.register_class(SmartRetopoVoxelRemeshOperator)
    bpy.utils.register_class(ResetSmartRetopoSettingsOperator)
    bpy.utils.register_class(SmartRetopoPanel)


def unregister():
    del bpy.types.Scene.smart_retopo
    bpy.utils.unregister_class(SmartRetopoSettings)
    bpy.utils.unregister_class(SmartRetopoQuadriFlowOperator)
    bpy.utils.unregister_class(SmartRetopoVoxelRemeshOperator)
    bpy.utils.unregister_class(ResetSmartRetopoSettingsOperator)
    bpy.utils.unregister_class(SmartRetopoPanel)


# Main Entry Point
if __name__ == "__main__":
    register()
