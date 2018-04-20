import xarray as xr
import glob

class Simulation(object):

	def __init__(self):
		pass

class NemoSim(Simulation):

	def __init__(self, path, grid_path="./", grids=['T', 'U', 'V', 'W'],
                 decode_times=True,
	             chunks=None, autoclose=False):
		"""
		Build and read a Nemo simulation under `xarray.DataSet` objects. The files
		 'coordinates.nc', 'mask.nc', 'mesh_hgr.nc' and 'mesh_zgr.nc' are required.

		Parameters
		----------
		path : str
			Path of the simulation where to find the different files, it may 
            usefully defined using unix wildcards
        grid_path : str, optional
            The path of the grid files associated with the simulation
        grids : list, optional 
            The list of grids to open containing {'U', 'V', 'T', 'F'}
		decode_times : bool, optional
			See xarray.Dataset
        chunks : int, tuple or dict, optional
            Chunk sizes along each dimension, e.g., ``5``, ``(5, 5)`` or
            ``{'x': 5, 'y': 5}``
		"""
		self.open_grid_files(grid_path)
		def open_files(filenames):
			ds = (xr.open_mfdataset(filenames,
			                        decode_times=decode_times,
			                        autoclose=autoclose,
			                        data_vars='minimal',
			                        chunks=chunks)
                    .set_coords(['nav_lon', 'nav_lat'])
			     )
			return ds
		if glob.glob(path + "/*gridT.nc") and ('T' in grids):
			self.gridT = open_files(path + "/*gridT.nc")
		if glob.glob(path + "/*gridU.nc") and ('U' in grids):
			self.gridU = open_files(path + "/*gridU.nc")
		if glob.glob(path + "/*gridV.nc") and ('V' in grids):
			self.gridV = open_files(path + "/*gridV.nc")
		if glob.glob(path + "/*gridW.nc") and ('W' in grids):
			self.gridW = open_files(path + "/*gridW.nc")
		if glob.glob(path + "/*flxT.nc") and ('T' in grids):
			self.flxT = open_files(path + "/*flxT.nc")

	def open_grid_files(self, grid_path):
		if glob.glob(grid_path + "/*coordinates.nc"):
			self.coordinates = (xr.open_mfdataset(grid_path +
			                                      "/*coordinates.nc",
			                                      decode_times=False).
			                    squeeze().drop(('time', 'z', 'nav_lev')).
			                    set_coords(('nav_lon', 'nav_lat'))
			                    )

		if glob.glob(grid_path + "/*mask.nc"):
			self.mask = (xr.open_mfdataset(grid_path + "/*mask.nc",
			                               decode_times=False).
			             squeeze().
			             set_coords(('nav_lon', 'nav_lat', 'nav_lev'))
			             )

		if glob.glob(grid_path + "/*mesh_hgr.nc"):
			self.mesh_hgr = (xr.open_mfdataset(grid_path + "/*mesh_hgr.nc",
			                                   decode_times=False).
			                 squeeze().drop(('nav_lev')).
			                 set_coords(('nav_lon', 'nav_lat'))
			                 )
		if glob.glob(grid_path + "/*mesh_zgr.nc"):
			self.mesh_zgr = (xr.open_mfdataset(grid_path + "/*mesh_zgr.nc",
			                                   decode_times=False).
			                 squeeze().
			                 set_coords(('nav_lon', 'nav_lat', 'nav_lev'))
			                 )


class NemoEns(NemoSim):

	def __init__(self, path, grid_path, chunks=None):
		simlist = []
		self.open_grid_files(grid_path)
		for simpath in glob.glob(path):
			simlist.append(NemoSim(simpath, grid_path=grid_path,
			                                chunks=chunks,
			                                autoclose=True)
			               )
		try:
			self.gridT = xr.concat([sim.gridT for sim in simlist], dim='n')
		except:
			pass
		try:
			self.gridU = xr.concat([sim.gridU for sim in simlist], dim='n')
		except:
			pass
		try:
			self.gridV = xr.concat([sim.gridV for sim in simlist], dim='n')
		except:
			pass
		try:
			self.gridW = xr.concat([sim.gridW for sim in simlist], dim='n')
		except:
			pass
		try:
			self.flxT = xr.concat([sim.flxT for sim in simlist], dim='n')
		except:
			pass