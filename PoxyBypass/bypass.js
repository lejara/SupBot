
Object.defineProperty(navigator, 'webdriver', { get: () => false,})
Object.defineProperty(navigator, 'mediaDevices', { get: () => false,})
Object.defineProperty(navigator, 'webkitGetUserMedia', { get: () => false,})
Object.defineProperty(navigator, 'mozGetUserMedia', { get: () => false,})
Object.defineProperty(navigator, 'getUserMedia', { get: () => false,})
Object.defineProperty(navigator, 'webkitRTCPeerConnection', { get: () => false,})


Object.defineProperty(navigator, 'languages', {
  get: function() {
    return ['en-US', 'en'];
  },
});


Object.defineProperty(navigator, 'plugins', {
  get: function() {
    return [1, 2, 3, 4, 5];
  },
});


const getParameter = WebGLRenderingContext.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
  if (parameter === 37445) {
    return 'Intel Open Source Technology Center';
  }
  if (parameter === 37446) {
    return 'Mesa DRI Intel(R) Ivybridge Mobile ';
  }

  return getParameter(parameter);
};


['height', 'width'].forEach(property => {

  const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);

  Object.defineProperty(HTMLImageElement.prototype, property, {
    ...imageDescriptor,
    get: function() {

      if (this.complete && this.naturalHeight == 0) {
        return 20;
      }
      // otherwise, return the actual dimension
      return imageDescriptor.get.apply(this);
    },
  });
});





const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');

Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
  ...elementDescriptor,
  get: function() {
    if (this.id === 'modernizr') {
        return 1;
    }
    return elementDescriptor.get.apply(this);
  },
});
