import bpy

class SmartRetopoPanel(bpy.types.Panel):
    """Smart Retopology Panel"""
    bl_label = "Smart Retopology"
    bl_idname = "VIEW3D_PT_smart_retopo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Smart Retopo"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.smart_retopo

        layout.operator("smart_retopo.quadri_remesh", text="OPERATE")

        layout.label(text="Quad Size Settings:")
        layout.prop(settings, "target_count")
        layout.prop(settings, "adaptive_size")
        layout.prop(settings, "quad_density")

        layout.label(text="Edge Loop Control:")
        layout.prop(settings, "detect_hard_edges")
        layout.prop(settings, "hard_edge_angle")

        layout.label(text="Symmetry:")
        layout.prop(settings, "symmetry_x")
        layout.prop(settings, "symmetry_y")
        layout.prop(settings, "symmetry_z")

        layout.operator("smart_retopo.voxel_remesh", text="Voxel Remesh")
        layout.operator("smart_retopo.reset_settings", text="Reset Settings")
