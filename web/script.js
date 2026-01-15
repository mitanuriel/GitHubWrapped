// GitHub Team Wrapped - Main Script
let currentSlide = 0;
let stats = null;
const totalSlides = 10;

// Load stats from JSON file
async function loadStats() {
  try {
    const response = await fetch('stats.json');
    stats = await response.json();
    console.log('Stats loaded:', stats);
    return stats;
  } catch (error) {
    console.error('Error loading stats:', error);
    // Use dummy data if file not found
    stats = {
      team_size: 8,
      repo_count: 2,
      total_prs: 30,
      top_contributor: "mitanuriel",
      top_contributor_prs: 13,
      total_additions: 125983,
      total_deletions: 29891,
      total_commits: 443,
      total_comments: 261,
      busiest_month: "December",
      busiest_month_prs: 20,
      most_active_repo: "tracking",
      most_active_repo_prs: 30
    };
    return stats;
  }
}

// Update progress bar
function updateProgress() {
  const progress = ((currentSlide) / (totalSlides - 1)) * 100;
  document.getElementById('progress-fill').style.width = `${progress}%`;
}

// Navigate to specific slide
function goToSlide(slideIndex) {
  const slides = document.querySelectorAll('.slide');

  if (slideIndex < 0 || slideIndex >= slides.length) return;

  // Remove active class from all slides
  slides.forEach((slide, index) => {
    slide.classList.remove('active', 'prev');
    if (index < slideIndex) {
      slide.classList.add('prev');
    }
  });

  // Add active class to current slide
  slides[slideIndex].classList.add('active');

  currentSlide = slideIndex;
  updateProgress();
  updateNavigation();

  // Populate data when entering slide - with a small delay for animation
  setTimeout(() => {
    populateSlideData(slideIndex);
  }, 300);
}

// Populate slide with actual data
function populateSlideData(slideIndex) {
  if (!stats) {
    console.error('Stats not loaded yet');
    return;
  }

  console.log('Populating slide', slideIndex, 'with stats:', stats);

  switch (slideIndex) {
    case 1: // Team Overview
      animateNumber('team-size', stats.team_size, ' Developers');
      animateNumber('repo-count', stats.repo_count, ' Repositories');
      break;
    case 2: // Pull Requests
      animateNumber('total-prs', stats.total_prs, '');
      break;
    case 3: // Top Contributor
      const topContribElement = document.getElementById('top-contributor');
      if (topContribElement) {
        topContribElement.textContent = stats.top_contributor;
      }
      animateNumber('top-contributor-prs', stats.top_contributor_prs, ' PRs');
      break;
    case 4: // Code Changes
      animateNumber('total-additions', stats.total_additions, '');
      animateNumber('total-deletions', stats.total_deletions, '');
      break;
    case 5: // Commits
      animateNumber('total-commits', stats.total_commits, '');
      break;
    case 6: // Comments
      animateNumber('total-comments', stats.total_comments, '');
      break;
    case 7: // Busiest Month
      const monthElement = document.getElementById('busiest-month');
      if (monthElement) {
        monthElement.textContent = stats.busiest_month;
      }
      animateNumber('busiest-month-prs', stats.busiest_month_prs, ' PRs');
      break;
    case 8: // Most Active Repo
      const repoElement = document.getElementById('most-active-repo');
      if (repoElement) {
        repoElement.textContent = stats.most_active_repo;
      }
      animateNumber('most-active-repo-prs', stats.most_active_repo_prs, ' PRs');
      break;
    case 9: // Summary
      animateNumber('summary-prs', stats.total_prs, '');
      animateNumber('summary-commits', stats.total_commits, '');
      animateNumber('summary-comments', stats.total_comments, '');
      animateNumber('summary-changes', stats.total_additions + stats.total_deletions, '');
      break;
  }
}

// Animate number counting up with smooth progress
function animateNumber(elementId, targetValue, suffix = '') {
  const element = document.getElementById(elementId);
  if (!element) {
    console.error('Element not found:', elementId);
    return;
  }

  // Reset element
  element.textContent = '0' + suffix;

  const duration = 2000; // 2 seconds
  const frameRate = 60; // 60 FPS
  const totalFrames = (duration / 1000) * frameRate;
  const increment = targetValue / totalFrames;

  let currentValue = 0;
  let frame = 0;

  const animation = setInterval(() => {
    frame++;
    currentValue += increment;

    if (frame >= totalFrames || currentValue >= targetValue) {
      currentValue = targetValue;
      clearInterval(animation);
    }

    // Format number with commas
    const displayValue = Math.round(currentValue).toLocaleString();
    element.textContent = displayValue + suffix;
  }, 1000 / frameRate);
}

// Update navigation buttons
function updateNavigation() {
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const counter = document.getElementById('slide-counter');

  prevBtn.disabled = currentSlide === 0;
  nextBtn.disabled = currentSlide === totalSlides - 1;
  counter.textContent = `${currentSlide + 1} / ${totalSlides}`;
}

// Navigation handlers
function nextSlide() {
  if (currentSlide < totalSlides - 1) {
    goToSlide(currentSlide + 1);
  }
}

function prevSlide() {
  if (currentSlide > 0) {
    goToSlide(currentSlide - 1);
  }
}

// Auto-advance option (optional)
function startAutoPlay(interval = 3000) {
  return setInterval(() => {
    if (currentSlide < totalSlides - 1) {
      nextSlide();
    } else {
      clearInterval(autoPlayInterval);
    }
  }, interval);
}

// Initialize
let autoPlayInterval = null;

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Page loaded, loading stats...');

  // Load stats first
  await loadStats();
  console.log('Stats loaded successfully:', stats);

  // Start button
  const startBtn = document.getElementById('start-btn');
  if (startBtn) {
    startBtn.addEventListener('click', () => {
      console.log('Start button clicked');
      goToSlide(1);
      // Optionally start auto-play
      // autoPlayInterval = startAutoPlay(4000);
    });
  }

  // Navigation buttons
  document.getElementById('next-btn').addEventListener('click', nextSlide);
  document.getElementById('prev-btn').addEventListener('click', prevSlide);

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault();
      nextSlide();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      prevSlide();
    }
  });

  // Touch swipe support
  let touchStartX = 0;
  let touchEndX = 0;

  document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  });

  document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  });

  function handleSwipe() {
    if (touchEndX < touchStartX - 50) {
      nextSlide();
    }
    if (touchEndX > touchStartX + 50) {
      prevSlide();
    }
  }

  // Initialize first slide
  updateNavigation();
  updateProgress();

  console.log('Initialization complete');
});
