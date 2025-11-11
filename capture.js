// capture.js
async function sendFrame(voterDbId) {
  const video = document.querySelector('video');
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth; canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d'); ctx.drawImage(video,0,0);
  const blob = await new Promise(res=>canvas.toBlob(res,'image/jpeg'));
  const fd = new FormData();
  fd.append('voter_db_id', voterDbId);
  fd.append('image', blob, 'frame.jpg');
  const r = await fetch('/face/recognize', { method:'POST', body:fd });
  const result = await r.json();
  console.log(result);
}
