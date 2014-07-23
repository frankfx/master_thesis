	private void loadStream(InputStream src, Context<Byte> context) {
		
		stream = src;
		context.write(0L,readStream(stream));
		
		setFaultsToContext(context);
	...

