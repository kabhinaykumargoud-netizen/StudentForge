document.addEventListener('DOMContentLoaded', () => {
  // Simple SPA Router
  function switchView(viewId) {
    document.querySelectorAll('.spa-view').forEach(view => {
      view.classList.remove('active');
    });
    
    const targetView = document.getElementById(viewId);
    if (targetView) {
      targetView.classList.add('active');
      window.scrollTo(0, 0);
    }
  }

  // Handle routing based on path
  function handleRoute(path) {
    let viewId = 'view-landing'; // Default
    
    if (path === '/' || path === '/home' || path === '') {
      viewId = 'view-landing';
    } else if (path.startsWith('/courses')) {
      viewId = 'view-courses';
    } else if (path.startsWith('/intern/signin')) {
      viewId = 'view-signin';
    } else if (path.startsWith('/signup')) {
      // If we don't have it yet, just show signin or landing
      viewId = 'view-signin';
    } else {
      // Try to match path to a view id directly, else default
      const id = 'view-' + path.replace(/^\//, '').replace(/\//g, '-');
      if (document.getElementById(id)) {
        viewId = id;
      }
    }
    
    switchView(viewId);
  }

  // Intercept link clicks
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link && link.href && link.origin === window.location.origin) {
      const path = link.pathname;
      e.preventDefault();
      history.pushState(null, '', path);
      handleRoute(path);
    }
  });

  // Handle back/forward buttons
  window.addEventListener('popstate', () => {
    handleRoute(window.location.pathname);
  });

  // Initial route
  handleRoute(window.location.pathname);

  // Signin form handler (Simulation)
  const signinForm = document.querySelector('.modern-signin-form');
  if (signinForm) {
    signinForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = signinForm.querySelector('button[type="submit"]');
      const origText = btn.innerHTML;
      btn.innerHTML = 'Signing in...';
      btn.style.opacity = '0.7';
      btn.disabled = true;
      
      setTimeout(() => {
        btn.innerHTML = 'Success!';
        btn.style.backgroundColor = '#10b981'; // emerald-500
        btn.style.borderColor = '#059669'; // emerald-600
        
        setTimeout(() => {
          // Reset form and go to courses (or dashboard)
          btn.innerHTML = origText;
          btn.style.backgroundColor = '';
          btn.style.borderColor = '';
          btn.style.opacity = '';
          btn.disabled = false;
          signinForm.reset();
          
          history.pushState(null, '', '/courses');
          handleRoute('/courses');
        }, 1000);
      }, 1500);
    });
  }
});
