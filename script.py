import unreal

def set_static_mesh_for_blueprint(bp, mesh):
	bp_asset = unreal.load_asset(bp.package_name)
	mesh_asset = unreal.load_asset(mesh.package_name)

	subsystem: unreal.SubobjectDataSubsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
	root_data_handle: unreal.SubobjectDataHandle = subsystem.k2_gather_subobject_data_for_blueprint(context=bp_asset)

	objects = []
	#get components in blueprint
	for handle in root_data_handle:
		subobject = subsystem.k2_find_subobject_data_from_handle( handle )
		objects.append( unreal.SubobjectDataBlueprintFunctionLibrary.get_object( subobject ) )


	#print(objects)
	#check if StaticMeshComponent and check the static_mesh parameter
	for object in objects:
		if "StaticMeshComponent" in str(object):
			static_mesh = object.get_editor_property("static_mesh")
			#print(static_mesh)
			
			if str(static_mesh) == "None":
				print( "StaticMeshComponent: " + str(object) + " has no static_mesh" )
				break

			object.set_editor_property("static_mesh", mesh_asset)


asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
prefabs = asset_registry.get_assets_by_path("/Game/Blueprints/Actors")
meshes = asset_registry.get_assets_by_path("/Game/Meshes/TargetMeshes")


i = 0
for prefab in prefabs:
	set_static_mesh_for_blueprint(prefab, meshes[i])
	i = i + 1
