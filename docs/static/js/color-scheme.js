// color-scheme.js
fetch('/static/color-scheme.json')
  .then(response => response.json())
  .then(colors => {
    const root = document.documentElement;

    // Set CSS variables dynamically
    Object.entries(colors).forEach(([key, value]) => {
      root.style.setProperty(`--${key}`, value);
    });
  })
  .catch(error => {
    console.error('Error loading color scheme:', error);
  });
