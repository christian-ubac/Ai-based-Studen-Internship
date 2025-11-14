<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// Reactive state
const isDragging = ref(false);
const selectedFile = ref(null);
const errorMessage = ref('');
const isLoading = ref(false);

const allowedTypes = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
];
const allowedExtensions = ['.pdf', '.doc', '.docx'];

// Template ref for the file input so we don't touch the DOM directly
const fileInput = ref(null);

const router = useRouter();

function validateFile(file) {
  errorMessage.value = '';
  if (!file) return false;

  const fileTypeIsValid = allowedTypes.includes(file.type);
  const fileName = file.name || '';
  const dotIdx = fileName.lastIndexOf('.');
  const fileExtension = dotIdx !== -1 ? fileName.slice(dotIdx).toLowerCase() : '';
  const fileExtensionIsValid = allowedExtensions.includes(fileExtension);

  if (fileTypeIsValid || fileExtensionIsValid) {
    selectedFile.value = file;
    return true;
  }

  errorMessage.value = 'Invalid file type. Please upload a PDF, DOC, or DOCX file.';
  return false;
}

function onFileSelect(event) {
  const file = event.target.files && event.target.files[0];
  validateFile(file);
}

function onDragOver() {
  isDragging.value = true;
}

function onDragLeave() {
  isDragging.value = false;
}

function onDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer?.files?.[0];
  validateFile(file);
}

function removeFile() {
  selectedFile.value = null;
  errorMessage.value = '';
  if (fileInput.value) fileInput.value.value = null;
}

async function handleUpload() {
  if (!selectedFile.value) {
    errorMessage.value = 'Please select a file first.';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  const formData = new FormData();
  // The backend expects the file field name to be 'file'
  formData.append('file', selectedFile.value);

  try {
    const response = await fetch('/api/upload-resume', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const text = await response.text().catch(() => '');
      throw new Error(`Upload failed: ${text || response.status}`);
    }

    // On success navigate to the Recommendations page and pass resumeId
    const result = await response.json();
    const resumeId = result?.resume_id;
    // If backend returned recommendations immediately, cache them so Recommendations page can read them
    if (result?.recommendations && resumeId) {
      try {
        const key = `recommendations_for_resume_${resumeId}`;
        localStorage.setItem(key, JSON.stringify(result.recommendations));
      } catch (e) {
        console.warn('Failed to cache recommendations locally', e);
      }
    }
    if (resumeId) {
      // Optionally trigger a quick scrape to ensure DB has recent listings (lightweight)
      try {
        await fetch('/scrape/internships?query=internship&limit=20');
      } catch (e) {
        // ignore scraper failures, recommendations will still run on existing data
        console.warn('Scraper trigger failed', e);
      }
      // Pass resume id as query so recommendations endpoint can use it
      await router.push({ name: 'Recommendations', query: { resumeId } });
    } else {
      try { await fetch('/scrape/internships?query=internship&limit=20'); } catch (e) { /* ignore */ }
      await router.push({ name: 'Recommendations' });
    }
  } catch (err) {
    console.error(err);
    errorMessage.value = 'An error occurred during upload. Please try again.';
    isLoading.value = false;
  }
}

function handleCancel() {
  // Reset selected file and navigate back one step if possible
  removeFile();
  try { router.back(); } catch (e) { /* ignore if not available */ }
}
</script>
<template>
  <div class="upload-page">
    <div class="upload-card">
      <h3>Upload Your Resume</h3>
      <p>We'll match you with the best AI internships. (PDF, DOC, or DOCX only)</p>

    <div 
      class="drop-zone"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      :class="{ 'drag-over': isDragging }"
    >
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M14 11V17H10V11H7L12 6L17 11H14ZM19.35 10.0391C18.67 6.59906 15.64 4 12 4C9.11 4 6.6 5.64 5.35 8.03906C2.34 8.35906 0 10.9091 0 13.9991C0 17.3091 2.69 19.9991 6 19.9991H19C21.76 19.9991 24 17.7591 24 14.9991C24 12.4591 22.09 10.4091 19.35 10.0391Z" 
        fill="#6366f1" 
        opacity="0.8"/>
      </svg>
      <p class="upload-text" v-if="!selectedFile">
        <span class="primary-text">Drag and drop your resume here</span>
        <span class="secondary-text">Supported formats: PDF, DOC, or DOCX</span>
      </p>
      <label for="file-input" class="browse-button">Choose File</label>
      <input 
        type="file" 
        id="file-input" 
        ref="fileInput"
        @change="onFileSelect" 
        accept=".pdf,.doc,.docx"
        hidden
      />
      <div v-if="selectedFile" class="file-info">
        <span>{{ selectedFile.name }}</span>
        <button @click="removeFile" class="remove-btn" title="Remove file">&times;</button>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div class="actions">
      <button class="btn-cancel" @click="handleCancel">Cancel</button>
      <button 
        class="btn-upload" 
        @click="handleUpload" 
        :disabled="!selectedFile || isLoading"
      >
        {{ isLoading ? 'Uploading...' : 'Upload & Find Internships' }}
      </button>
    </div>

  </div>
  </div>
</template>

<style src="../style.css"></style>

<style>
.upload-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f3e7ff 0%, #e5f0ff 100%);
}

.upload-card {
  max-width: 600px;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(8px);
}

.upload-card h3 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #1a1a1a;
}

.upload-card p {
  color: #666;
  font-size: 15px;
  margin-bottom: 32px;
}

.drop-zone {
  border: 2px dashed #6366f1;
  background: rgba(99, 102, 241, 0.03);
  border-radius: 12px;
  padding: 40px 20px;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.upload-text {
  text-align: center;
  margin: 0;
}

.upload-text .primary-text {
  display: block;
  font-size: 16px;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.upload-text .secondary-text {
  display: block;
  font-size: 14px;
  color: #6b7280;
}

.drop-zone.drag-over {
  border-color: #4f46e5;
  background: rgba(99, 102, 241, 0.08);
  transform: scale(1.01);
}

.browse-button {
  display: inline-block;
  background: #6366f1;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
  margin-top: 16px;
  transition: all 0.2s ease;
}

.browse-button:hover {
  background: #4f46e5;
  transform: translateY(-1px);
}

.file-info {
  margin-top: 16px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-info span {
  flex: 1;
  font-size: 14px;
  color: #1a1a1a;
}

.remove-btn {
  background: #fee2e2;
  color: #ef4444;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 12px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: #fecaca;
  transform: scale(1.05);
}

.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background: #fee2e2;
  color: #dc2626;
  border-radius: 8px;
  font-size: 14px;
}

.actions {
  margin-top: 32px;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.btn-cancel {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #4b5563;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.btn-upload {
  padding: 10px 24px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-upload:hover:not(:disabled) {
  background: #4f46e5;
  transform: translateY(-1px);
}

.btn-upload:disabled {
  background: #e5e7eb;
  cursor: not-allowed;
}
</style>