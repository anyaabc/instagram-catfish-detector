const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];

const uploadInput = document.getElementById('imageUpload');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const form = document.getElementById('uploadForm');
const spinner = document.getElementById('spinner');
const resultsDiv = document.getElementById('results');
const resultsList = document.getElementById('resultsList');

uploadInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file || !ALLOWED_TYPES.includes(file.type)) {
    alert('Please select a JPG,PNG,JPEG image.');
    previewContainer.classList.add('hidden');
    return;
  }
  if (file.size > MAX_FILE_SIZE) {
    alert('File too large. Max 5 MB.');
    previewContainer.classList.add('hidden');
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.src = e.target.result;
    previewContainer.classList.remove('hidden');
  };
  reader.readAsDataURL(file);
});

form.addEventListener('submit', async e => {
  e.preventDefault();
  const file = uploadInput.files[0];
  if (!file) return;

  // Show spinner, hide previous results
  spinner.classList.remove('hidden');
  resultsDiv.classList.add('hidden');
  resultsList.innerHTML = '';

  const formData = new FormData();
  formData.append('image', file);

  try {
    const res = await fetch('/api/match', { method: 'POST', body: formData });
    const payload = await res.json();

    spinner.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    resultsList.innerHTML = '';

    if (res.ok && Array.isArray(payload.matches) && payload.matches.length) {
      const header = document.createElement('p');
      header.className = 'text-green-600 font-semibold mb-4';
      header.textContent = `✅ We found ${payload.matches.length} potential match(es):\n`;
      resultsList.appendChild(header);

      payload.matches.forEach(m => {
        const sumber = m.source_type === 'profile' ? 'dari foto profil' : 'dari postingan';
        const tanggal = m.date_posted || 'N/A';
        const similarity = (m.similarity * 100).toFixed(2);
        const imageFile = m.image_path.split('/').pop();
        const imageFolder = m.username;

        const card = document.createElement('div');
        card.className = 'p-4 mb-4 rounded-lg border bg-gray-50 shadow-sm';

        card.innerHTML = `
          <div class="flex items-start gap-4">
            <img src="/images/${m.username}/${imageFile}" alt="match" class="w-24 h-24 object-cover rounded-md border">
            <div class="text-sm">
              <p><strong>👤 Username:</strong> ${m.username}</p>
              <p><strong>📍 Source:</strong> ${sumber}</p>
              <p><strong>📅 Date Posted:</strong> ${tanggal}</p>
              <p><strong>🔍 Similarity Score:</strong> ${similarity}%</p>
            </div>
          </div>
        `;
        resultsList.appendChild(card);
      });
    } else {
      resultsList.innerHTML = '<p class="text-red-600 font-semibold">❌ We cannot find anyone similar at the moment.</p>';
    }
  } catch (err) {
    spinner.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    resultsList.innerHTML = `<p class="text-red-600">❌ Mistake: ${err.message}</p>`;
  }
});
