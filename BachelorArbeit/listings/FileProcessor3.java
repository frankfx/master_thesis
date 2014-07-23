	public void processData(String filename) {
		startprocessData(new FileInputStream(filename),filename);
	}
	
	public void processData(InputStream src) {
		startprocessData(src,"");
	}
			
	private void startprocessData(InputStream src ,String filename) ...
		Context<Byte> ctx = new Context<Byte>();

		loadStream(src, ctx);
		
		ctx.injectFaults();
		
		Reducer reducer = new Reducer();
		for (long i = 0; i < ctx.getEntries().size(); i++) {
			reducer.setFileName(filename);
			reducer.reduce(ctx.getEntries().get(i));
		}
	}
