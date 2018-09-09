import angr

project = angr.Project("GuessTheString", load_options={'auto_load_libs': False})

path_group = project.factory.simulation_manager()

path_group.explore(find=0x400dfe, avoid=0x400590)

print path_group.found[0].state.posix.dumps(1)
