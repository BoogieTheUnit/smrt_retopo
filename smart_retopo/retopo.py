import bpy

def preprocess_mesh(obj):
    """Prepares the mesh for remeshing."""
    if obj.type != 'MESH':
        return

    # Ensure Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Clean Up: Remove loose geometry
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.delete_loose()
    bpy.ops.object.editmode_toggle()

    # Merge by Distance (collapses nearby vertices)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.editmode_toggle()

    # Fill Holes (Optional): Repairs open areas
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.fill_holes(sides=16)
    bpy.ops.object.editmode_toggle()

    # Recalculate Normals
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

    # Select and Remove Non-Manifold Geometry
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.mesh.delete(type='EDGE_FACE')
    bpy.ops.object.editmode_toggle()

    print("Preprocessing completed for Blender 4.2.4: Mesh should now be manifold and consistent.")

def apply_symmetry(obj, settings):
    """Apply symmetry to the mesh based on settings."""
    bpy.ops.object.mode_set(mode='EDIT')

    # Apply symmetry along enabled axes
    if settings.symmetry_x:
        bpy.ops.mesh.symmetrize(direction='POSITIVE_X')  # Use the correct enum
    if settings.symmetry_y:
        bpy.ops.mesh.symmetrize(direction='POSITIVE_Y')  # Use the correct enum
    if settings.symmetry_z:
        bpy.ops.mesh.symmetrize(direction='POSITIVE_Z')  # Use the correct enum

    bpy.ops.object.mode_set(mode='OBJECT')
    print("Symmetry applied.")


def enhance_curvature(obj):
    """Enhance mesh curvature during retopology."""
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.mark_sharp()
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Curvature preservation applied.")

def voxel_remesh(obj, size=0.1):
    """Uses Blender's Voxel Remesher for remeshing."""
    if obj.type != 'MESH':
        return

    # Ensure Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Set Voxel Remesh Properties
    obj.data.remesh_voxel_size = size
    obj.data.use_remesh_fix_poles = True

    # Execute Voxel Remesh
    bpy.ops.object.voxel_remesh()
    print(f"Voxel remesh completed with voxel size: {size}.")

def reset_settings(context):
    """Reset Smart Retopo settings to defaults."""
    settings = context.scene.smart_retopo
    settings.target_count = 5000
    settings.adaptive_size = 50.0
    settings.quad_density = 1.0
    settings.use_materials = False
    settings.use_normals_splitting = False
    settings.detect_hard_edges = False
    settings.hard_edge_angle = 30.0
    settings.symmetry_x = False
    settings.symmetry_y = False
    settings.symmetry_z = False
    print("Settings reset to defaults.")

class SmartRetopoQuadriFlowOperator(bpy.types.Operator):
    """Run QuadriFlow Remesh with Adaptive Features."""
    bl_idname = "smart_retopo.quadri_remesh"
    bl_label = "QuadriFlow Remesh"

    def execute(self, context):
        settings = context.scene.smart_retopo
        obj = context.object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected.")
            return {'CANCELLED'}

        try:
            # Preprocess the mesh
            preprocess_mesh(obj)

            # Calculate dynamic target face count
            base_quad_count = settings.target_count
            adaptive_factor = settings.adaptive_size / 100.0
            density_factor = settings.quad_density
            target_face_count = int(base_quad_count * adaptive_factor * density_factor)

            # Clamp face count to safe limits
            target_face_count = max(100, min(target_face_count, 100000))

            print(f"QuadriFlow Target Faces: {target_face_count}")

            # Apply symmetry if enabled
            apply_symmetry(obj, settings)

            # Run QuadriFlow Remesh (directly using operator without extra properties)
            bpy.ops.object.quadriflow_remesh()

            # Optionally enhance curvature
            if settings.detect_hard_edges:
                enhance_curvature(obj)

            self.report({'INFO'}, "QuadriFlow remeshing completed successfully.")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"QuadriFlow failed: {str(e)}")
            return {'CANCELLED'}



class SmartRetopoVoxelRemeshOperator(bpy.types.Operator):
    """Run Voxel Remesh."""
    bl_idname = "smart_retopo.voxel_remesh"
    bl_label = "Voxel Remesh"

    def execute(self, context):
        obj = context.object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected.")
            return {'CANCELLED'}

        try:
            voxel_remesh(obj, size=0.1)
            self.report({'INFO'}, "Voxel remesh completed successfully.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Voxel remesh failed: {str(e)}")
            return {'CANCELLED'}

class ResetSmartRetopoSettingsOperator(bpy.types.Operator):
    """Reset all Smart Retopo settings to default values."""
    bl_idname = "smart_retopo.reset_settings"
    bl_label = "Reset Settings"

    def execute(self, context):
        reset_settings(context)
        self.report({'INFO'}, "Settings reset to defaults.")
        return {'FINISHED'}
