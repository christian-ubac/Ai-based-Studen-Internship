<template>
  <div class="recommendations-container">
    <div class="header">
      <h2>Your AI-Powered Internship Matches</h2>
      <p class="subtitle">Matches are ranked by skill alignment and updated regularly</p>
    </div>

    <!-- Loading State with Animation -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner">
        <svg class="animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
      <div class="loading-text">
        <p class="primary">Analyzing your resume...</p>
        <p class="secondary">Matching with our AI internship database</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Oops! Something went wrong</h3>
      <p>{{ error }}</p>
      <button @click="fetchRecommendations" class="retry-button">
        Try Again
      </button>
    </div>

    <!-- Results List -->
    <div v-if="!isLoading && !error && recommendations.length > 0" class="recommendations-list">
      <div class="match-stats">
        <p>Found {{ recommendations.length }} matches based on your profile</p>
      </div>
      
      <div v-for="job in recommendations" 
           :key="job.id" 
           class="job-card"
           :class="{ 'high-match': job.match_score >= 85 }"
      >
        <div class="job-header">
          <div class="job-title-section">
            <h3>{{ job.title }}</h3>
            <span class="match-score" :style="{ '--score': job.match_score + '%' }">
              {{ job.match_score }}% Match
            </span>
          </div>
          <h4>{{ job.company_name }}</h4>
          <div class="job-meta">
            <span class="location">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
              </svg>
              {{ job.location }}
            </span>
            <span class="posted-date">Posted {{ formatDate(job.posted_date) }}</span>
          </div>
        </div>
        
        <div class="skills-section">
          <h5>Matching Skills</h5>
          <div class="skills-match">
            <span v-for="skill in job.matched_skills" 
                  :key="skill" 
                  class="skill-tag"
            >
              {{ skill }}
            </span>
          </div>
        </div>
        
        <div class="job-footer">
          <p class="description">{{ truncate(job.description, 150) }}</p>
          <div class="actions">
            <a :href="job.posting_url" 
               target="_blank" 
               class="apply-button"
            >
              View Details & Apply
            </a>
            <button class="save-button" 
                    @click="toggleSaved(job)"
                    :class="{ 'saved': savedJobs.includes(job.id) }"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/>
              </svg>
              {{ savedJobs.includes(job.id) ? 'Saved' : 'Save' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!isLoading && !error && recommendations.length === 0" class="empty-state">
      <div class="empty-icon">🔍</div>
      <h3>No matches found yet</h3>
      <p>We're actively searching for internships matching your profile. Check back soon or try updating your resume with more details about your skills and interests.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const recommendations = ref([]);
const isLoading = ref(true);
const error = ref(null);
const savedJobs = ref([]);
const route = useRoute();

// Helper function to format dates
function formatDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// Helper function to truncate text
function truncate(text, length) {
  if (text.length <= length) return text;
  return text.substring(0, length).trim() + '...';
}

// Toggle job saved state
function toggleSaved(job) {
  const index = savedJobs.value.indexOf(job.id);
  if (index === -1) {
    savedJobs.value.push(job.id);
  } else {
    savedJobs.value.splice(index, 1);
  }
  // You could persist this to localStorage or your backend
  localStorage.setItem('savedJobs', JSON.stringify(savedJobs.value));
}

async function fetchRecommendations() {
  isLoading.value = true;
  error.value = null;
  
  try {
    // Get the resume ID from the route if available
    const resumeId = route.query.resumeId;
    // If upload just returned recommendations and stored them in localStorage, use that first
    if (resumeId) {
      try {
        const cached = localStorage.getItem(`recommendations_for_resume_${resumeId}`);
        if (cached) {
          const parsed = JSON.parse(cached);
          recommendations.value = parsed.map(job => ({
            ...job,
            match_score: typeof job.match_score === 'number' ? job.match_score : 50,
            posted_date: job.posted_date || new Date().toISOString()
          }));
          // sort and return early
          recommendations.value.sort((a, b) => b.match_score - a.match_score);
          // remove cache now that we've consumed it
          localStorage.removeItem(`recommendations_for_resume_${resumeId}`);
          isLoading.value = false;
          return;
        }
      } catch (e) {
        console.warn('Failed to read cached recommendations', e);
      }
    }
    
    const response = await fetch(`/api/get-recommendations${resumeId ? `?resumeId=${resumeId}` : ''}`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Failed to fetch recommendations');
    }
    
    const data = await response.json();
    
    // Transform the data to ensure match_score and posted_date exist
    recommendations.value = data.map(job => ({
      ...job,
      match_score: typeof job.match_score === 'number' ? job.match_score : 50,
      posted_date: job.posted_date || new Date().toISOString(),
    }));
    
    // Sort by match score
    recommendations.value.sort((a, b) => b.match_score - a.match_score);
    
  } catch (err) {
    console.error('Recommendation fetch error:', err);
    error.value = 'Unable to load recommendations. Please try again later.';
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  // Load saved jobs from localStorage
  const saved = localStorage.getItem('savedJobs');
  if (saved) {
    savedJobs.value = JSON.parse(saved);
  }
  
  fetchRecommendations();
});
</script>
 
<style src="../style.css"></style>

<style scoped>
.recommendations-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h2 {
  font-size: 32px;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.subtitle {
  color: #6b7280;
  font-size: 16px;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 0;
}

.loading-spinner {
  margin: 0 auto 24px;
  width: 48px;
  height: 48px;
  color: #6366f1;
}

.loading-spinner svg {
  animation: spin 1s linear infinite;
}

.loading-text .primary {
  font-size: 18px;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.loading-text .secondary {
  color: #6b7280;
}

/* Error State */
.error-state {
  text-align: center;
  padding: 40px;
  background: #fee2e2;
  border-radius: 12px;
  margin: 20px 0;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.retry-button {
  margin-top: 20px;
  padding: 10px 24px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-button:hover {
  background: #b91c1c;
}

/* Results List */
.match-stats {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  color: #1a1a1a;
}

.job-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.job-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px -2px rgba(0, 0, 0, 0.1);
}

.job-card.high-match {
  border-left: 4px solid #6366f1;
}

.job-header {
  margin-bottom: 20px;
}

.job-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.job-title-section h3 {
  font-size: 20px;
  color: #1a1a1a;
  margin: 0;
}

.match-score {
  background: linear-gradient(90deg, #6366f1 var(--score), #e5e7eb var(--score));
  -webkit-background-clip: text;
  color: transparent;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.job-meta {
  display: flex;
  gap: 16px;
  color: #6b7280;
  font-size: 14px;
  margin-top: 8px;
}

.location {
  display: flex;
  align-items: center;
  gap: 4px;
}

.skills-section {
  margin: 20px 0;
}

.skills-section h5 {
  color: #4b5563;
  margin-bottom: 12px;
}

.skills-match {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  background: #f3f4f6;
  color: #4b5563;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
}

.job-footer {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.description {
  color: #4b5563;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.actions {
  display: flex;
  gap: 12px;
}

.apply-button {
  flex: 1;
  padding: 10px 24px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  text-align: center;
  text-decoration: none;
  transition: background 0.2s;
}

.apply-button:hover {
  background: #4f46e5;
}

.save-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.save-button:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.save-button.saved {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: #f8fafc;
  border-radius: 12px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state h3 {
  color: #1a1a1a;
  margin-bottom: 12px;
}

.empty-state p {
  color: #6b7280;
  max-width: 500px;
  margin: 0 auto;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .recommendations-container {
    padding: 20px;
  }
  
  .header h2 {
    font-size: 24px;
  }
  
  .job-card {
    padding: 16px;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .save-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
