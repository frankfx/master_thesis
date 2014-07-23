	@FaultInj(id="OutputTEST", type="LOSS", rate=1, blocksize=1024)
	private InputStream test;
	
	// =================================================
	
	@FaultInjects({	
		@FaultInj(id="OutputBAOS", type="ZERO", rate=0.01, blocksize=8),	
		@FaultInj(id="OutputBAOS2", type="LOSS", rate=0.001, blocksize=8)
	})
	private InputStream fis;
	
	...
