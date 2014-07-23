	private void loadStream(InputStream src, Context<Byte> context) {
		
		stream = src;
		context.write(0L,readStream(stream));
		
		setFaultsToContext(context);
		//setFaultsByIDToContext(context, 
		//	new String[]{"OutputBAOS","OutputBAOS2"},0L);
	}
	
	private List<Byte> readStream(InputStream src) {
		List<Byte> list = new ArrayList<Byte>();
		int i;
		while((i=src.read())!=-1)
			list.add((byte)i);
		return list;
	}
