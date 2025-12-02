(function () {
  // Fix 100vh
  const setVH = () => {
    document.documentElement.style.setProperty(
      '--vh',
      `${window.innerHeight * 0.01}px`
    );
  };
  setVH();
  window.addEventListener('resize', setVH);

  // Prevent zoom
  document.addEventListener('touchmove', e => {
    if (e.scale !== 1) e.preventDefault();
  }, { passive:false });

  // Prevent overscroll
  document.body.style.overscrollBehavior = 'none';
})();