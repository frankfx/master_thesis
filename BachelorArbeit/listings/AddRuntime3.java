	// create the annotation
	ClassFile ccFile = cc.getClassFile();
	ConstPool constpool = ccFile.getConstPool();

	AnnotationsAttribute[] attr = new AnnotationsAttribute[faults.length];
	Annotation[] annotations = new Annotation[faults.length];
	Annotation[] subAnnotations;
