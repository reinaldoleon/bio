document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle Logic
  const themeToggleBtn = document.getElementById('theme-toggle');
  const currentTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  
  // Set initial theme
  if (currentTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  themeToggleBtn.addEventListener('click', () => {
    let theme = document.documentElement.getAttribute('data-theme');
    let targetTheme = 'dark';
    
    if (theme === 'dark') {
      targetTheme = 'light';
    }
    
    document.documentElement.setAttribute('data-theme', targetTheme);
    localStorage.setItem('theme', targetTheme);
  });

  // Language Toggle Logic
  const langButtons = document.querySelectorAll('.lang-btn');
  const initialLang = localStorage.getItem('lang') || 'en';
  
  const setLanguage = (lang) => {
    document.documentElement.setAttribute('data-lang', lang);
    localStorage.setItem('lang', lang);
    langButtons.forEach(btn => {
      if (btn.getAttribute('data-lang-set') === lang) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  };

  // Set initial language
  setLanguage(initialLang);

  langButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetLang = btn.getAttribute('data-lang-set');
      setLanguage(targetLang);
    });
  });

  // Mobile Menu Logic
  const mobileToggle = document.getElementById('mobile-toggle');
  const navLinks = document.getElementById('nav-links');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      const isExpanded = navLinks.classList.contains('active');
      mobileToggle.setAttribute('aria-expanded', isExpanded);
    });

    // Close menu when link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        mobileToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Skills Filtering & Progression Animation
  const filterButtons = document.querySelectorAll('.filter-btn');
  const skillCards = document.querySelectorAll('.skill-card');

  // Trigger animation for visible progress bars
  const animateSkillBars = () => {
    skillCards.forEach(card => {
      if (card.style.display !== 'none') {
        const progressBar = card.querySelector('.skill-bar-progress');
        if (progressBar) {
          const val = progressBar.getAttribute('data-level');
          progressBar.style.width = val + '%';
        }
      }
    });
  };

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      // Remove active class from all buttons
      filterButtons.forEach(b => b.classList.remove('active'));
      // Add active class to current button
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      skillCards.forEach(card => {
        const categories = card.getAttribute('data-categories').split(' ');
        
        // Reset progress bar width first to re-trigger transition
        const progressBar = card.querySelector('.skill-bar-progress');
        if (progressBar) {
          progressBar.style.width = '0';
        }

        if (filterValue === 'all' || categories.includes(filterValue)) {
          card.style.display = 'block';
          // Force reflow
          void card.offsetWidth;
        } else {
          card.style.display = 'none';
        }
      });

      // Animate the newly filtered progress bars
      setTimeout(animateSkillBars, 50);
    });
  });

  // Initial animation trigger
  setTimeout(animateSkillBars, 150);

  // Scroll active link highlight
  const sections = document.querySelectorAll('section');
  const navItems = document.querySelectorAll('.nav-links a');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollPos = window.scrollY + 100; // Offset for header

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navItems.forEach(item => {
      item.classList.remove('active');
      if (item.getAttribute('href').slice(1) === current) {
        item.classList.add('active');
      }
    });
  });
});
