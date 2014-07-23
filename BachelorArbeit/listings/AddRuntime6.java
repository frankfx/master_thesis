  // transform the ctClass to java class
  dynamiqueBeanClass = Class.forName(className);
  classFile = cc.toBytecode();
  hs.reload(className, classFile);

  // instanciating the updated class
  imgP = (StreamProcessor) dynamiqueBeanClass.newInstance();
